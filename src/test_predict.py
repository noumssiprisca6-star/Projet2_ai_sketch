# ============================================================
# test_predict.py : tester le modèle sur un vrai dessin
# 
#
# Ce fichier est un PROGRAMME DE TEST (on le lance).
# Il utilise predict.py, qui est un MODULE (on ne le lance pas).
#
# Avant de lancer :
#   1. avoir exécuté "python src/train.py" (il crée le modèle)
#   2. avoir dessiné un objet dans Paint (fond blanc, trait noir épais)
#      et l'avoir enregistré en maison.png dans le dossier src/
#
# Lancer depuis la racine du projet, avec (venv) visible :
#   python src/test_predict.py
# ============================================================

import os                               # pour construire le chemin du fichier
import cv2                              # pour lire l'image
from predict import predict_drawing     # notre fonction de prédiction (predict.py)

# ------------------------------------------------------------
# 1. CHEMIN DE L'IMAGE À TESTER
# ------------------------------------------------------------
# __file__ = l'emplacement de ce fichier (src/test_predict.py).
# On cherche maison.png dans le MÊME dossier que ce fichier,
# donc ça marche même si on lance la commande depuis un autre dossier.
# Pour tester un autre dessin, change simplement le nom ici
# (par exemple "soleil.png", "arbre.png", "voiture.png", "chat.png").
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maison.png")

# ------------------------------------------------------------
# 2. LECTURE DE L'IMAGE
# ------------------------------------------------------------
# cv2.imread lit l'image. Attention : si le fichier n'existe pas
# ou si le nom est faux, elle ne plante pas : elle renvoie None.
img = cv2.imread(path)

# ------------------------------------------------------------
# 3. VÉRIFICATION, PUIS PRÉDICTION
# ------------------------------------------------------------
if img is None:
    # Filet de sécurité : message clair au lieu d'un plantage.
    # Causes fréquentes : mauvais nom, mauvais dossier, ou extension
    # cachée sous Windows (maison.png.png).
    print("Image introuvable, vérifie le nom et l'emplacement :", path)
else:
    # predict_drawing fait tout le travail :
    #   - passage en niveaux de gris
    #   - inversion (trait blanc sur fond noir)
    #   - recadrage autour du dessin
    #   - réduction à 28x28 pixels
    #   - prédiction par le CNN
    # Elle renvoie le nom de la classe et un score entre 0 et 1.
    classe, score = predict_drawing(img)

    # Si le canvas est vide, predict_drawing renvoie (None, 0.0)
    if classe is None:
        print("Aucun dessin détecté dans l'image (image vide).")
    else:
        # score * 100 : on transforme 0.943 en 94.3 %
        # :.1f = une seule décimale
        print(f"Prédiction : {classe} ({score * 100:.1f} %)") 