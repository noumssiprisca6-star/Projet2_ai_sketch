# ============================================================
# integration.py : liaison entre l'interface (app.py) et le modèle (predict.py)
#
# Rôle de ce module (partie Backend / Intégration) :
#   1. recevoir l'image Pillow du canvas d'Aristide (app.py) ;
#   2. la convertir en tableau NumPy exploitable par OpenCV ;
#   3. la nettoyer (trait blanc sur fond noir, trait suffisamment épais) ;
#   4. appeler predict_drawing() d'Élisabeth (predict.py) ;
#   5. renvoyer un texte prêt à afficher dans le panneau « Résultat ».
#
# IMPORTANT : le redimensionnement en 28x28, le centrage et la
# normalisation (0-1) sont DÉJÀ faits dans predict.preprocess().
# On ne les refait donc PAS ici (sinon le dessin serait traité deux fois).
#
# Ce fichier ne dépend pas de Tkinter : on peut le tester seul.
# ============================================================

import os
import sys

import cv2
import numpy as np

# ------------------------------------------------------------
# RÉGLAGES (à ajuster avec Élisabeth après les premiers tests)
# ------------------------------------------------------------

# En dessous de ce score, on affiche « je ne suis pas sûr » au lieu d'affirmer.
SEUIL_CONFIANCE = 0.50

# Les images Quick, Draw! ont un trait fin mais bien visible une fois réduites
# à 28x28 (environ 1/12 du plus grand côté du dessin). Un trait de souris trop
# fin disparaît presque à la réduction : on l'épaissit jusqu'à ce rapport.
RATIO_TRAIT_CIBLE = 12

# Dossier src/ : permet d'importer predict.py même si on lance le programme
# depuis un autre dossier.
DOSSIER_SRC = os.path.dirname(os.path.abspath(__file__))
if DOSSIER_SRC not in sys.path:
    sys.path.insert(0, DOSSIER_SRC)


class ErreurModele(Exception):
    """Levée quand le modèle ne peut pas être chargé (message lisible en français)."""


# ------------------------------------------------------------
# ÉTAPES DE PRÉTRAITEMENT (fonctions simples, testables séparément)
# ------------------------------------------------------------

def image_pil_vers_gris_inverse(image_pil):
    """
    Convertit l'image Pillow du canvas en niveaux de gris, trait CLAIR sur fond NOIR.

    Le canvas d'Aristide est un fond blanc avec un trait bleu foncé :
    on passe en gris puis on inverse (255 - gris) pour obtenir le format
    attendu par le modèle (comme les images Quick, Draw!).

    Paramètre : image_pil = Image Pillow (self.image de app.py)
    Retourne  : tableau NumPy 2D de type uint8
    """
    # Pillow travaille en RGB (OpenCV en BGR) : on précise donc RGB2GRAY.
    rgb = np.array(image_pil.convert("RGB"))
    gris = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return 255 - gris


def epaissir_trait(img, epaisseur_actuelle):
    """
    Épaissit le trait pour qu'il reste visible après la réduction en 28x28.

    Paramètres :
        img                = image grise, trait clair sur fond noir
        epaisseur_actuelle = épaisseur du pinceau choisie par l'utilisateur (en pixels)
    Retourne : l'image, épaissie si nécessaire (sinon inchangée).
    """
    ys, xs = np.where(img > 30)
    if len(xs) == 0:
        return img                      # canvas vide : rien à faire

    # Taille du dessin = plus grand côté de la boîte englobante
    hauteur = ys.max() - ys.min() + 1
    largeur = xs.max() - xs.min() + 1
    plus_grand_cote = max(hauteur, largeur)

    # Épaisseur à atteindre, et épaisseur à AJOUTER par rapport à l'actuelle
    epaisseur_cible = plus_grand_cote // RATIO_TRAIT_CIBLE
    a_ajouter = epaisseur_cible - int(epaisseur_actuelle)
    if a_ajouter < 1:
        return img                      # trait déjà assez épais

    # Dilatation : un noyau de diamètre (a_ajouter + 1) ajoute a_ajouter pixels
    noyau = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (a_ajouter + 1, a_ajouter + 1)
    )
    return cv2.dilate(img, noyau)


def preparer_image(image_pil, epaisseur_trait=1):
    """
    Chaîne complète de prétraitement côté intégration.
    Le résultat est ensuite donné à predict_drawing(), qui fait le 28x28.
    """
    img = image_pil_vers_gris_inverse(image_pil)
    img = epaissir_trait(img, epaisseur_trait)
    return img


def formater_resultat(classe, score):
    """
    Construit le texte affiché dans le panneau de résultat.

    Retourne : (texte, est_sur) où est_sur vaut True si le score dépasse le seuil.
    """
    if classe is None:
        return "Le dessin est vide : dessine quelque chose puis clique sur Reconnaître.", False

    pourcentage = round(score * 100)
    if score >= SEUIL_CONFIANCE:
        return f"Je pense que c'est : {classe}  ({pourcentage} % de confiance)", True
    return (
        f"Je ne suis pas sûr... peut-être : {classe}  ({pourcentage} % de confiance). "
        "Essaie de dessiner plus grand ou plus clairement.",
        False,
    )


# ------------------------------------------------------------
# CLASSE PRINCIPALE : celle que app.py utilise
# ------------------------------------------------------------

class Reconnaisseur:
    """
    Fait le lien entre l'interface et predict.py.

    Le modèle est chargé UNE SEULE FOIS, au premier clic sur « Reconnaître »
    (predict.py charge le modèle dès son import : on retarde donc cet import
    pour que l'interface s'ouvre vite, même si le modèle n'existe pas encore).
    """

    def __init__(self):
        self._predict = None            # module predict, une fois importé

    def _charger(self):
        """Importe predict.py (et donc charge le modèle) si ce n'est pas déjà fait."""
        if self._predict is not None:
            return
        try:
            import predict              # fichier d'Élisabeth : src/predict.py
        except ModuleNotFoundError as e:
            if e.name == "predict":
                # Le fichier d'Élisabeth n'est pas dans src/ (pull request non fusionnée ?)
                raise ErreurModele(
                    "Le fichier src/predict.py est introuvable.\n"
                    "Récupère la version d'Élisabeth (git pull) et vérifie son emplacement."
                ) from e
            raise ErreurModele(
                f"Bibliothèque manquante : {e.name}.\n"
                "Installe-la avec : pip install tensorflow opencv-python numpy"
            ) from e
        except (OSError, ValueError) as e:
            # Fichier .keras ou class_names.json introuvable / illisible
            raise ErreurModele(
                "Impossible de charger le modèle.\n"
                "Lance d'abord l'entraînement : python src/train.py\n"
                "(il doit créer models/ai_sketch.keras et models/class_names.json)\n\n"
                f"Détail : {e}"
            ) from e
        self._predict = predict

    def predire(self, image_pil, epaisseur_trait=1):
        """
        Prédit la catégorie du dessin.

        Paramètres :
            image_pil       = image Pillow du canvas (self.image dans app.py)
            epaisseur_trait = valeur du curseur d'épaisseur (self.taille_pinceau.get())
        Retourne : (nom_de_la_classe, score) ou (None, 0.0) si le canvas est vide.
        """
        self._charger()
        img = preparer_image(image_pil, epaisseur_trait)
        return self._predict.predict_drawing(img)

    def sauver_apercu(self, image_pil, chemin="debug_28x28.png", epaisseur_trait=1):
        """
        OUTIL DE DEBUG : enregistre ce que le réseau « voit » réellement (28x28,
        agrandi x10). Pratique pour vérifier le centrage et l'épaisseur du trait.
        """
        self._charger()
        x = self._predict.preprocess(preparer_image(image_pil, epaisseur_trait))
        if x is None:
            return False
        petit = (x[0, :, :, 0] * 255).astype("uint8")
        grand = cv2.resize(petit, (280, 280), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(chemin, grand)
        return True
