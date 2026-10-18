# ============================================================
# predict.py : prédiction sur un dessin fait à la souris
# Utilisation par les autres (dans src/app.py) :
#     from predict import predict_drawing
#     classe, score = predict_drawing(image_du_canvas)
# ============================================================

import os
import json

import cv2                       # prétraitement de l'image
import numpy as np
from tensorflow import keras

# ------------------------------------------------------------
# CHEMINS (calculés à partir de l'emplacement de ce fichier)
# ------------------------------------------------------------
# Racine du projet = dossier parent de src/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "models", "ai_sketch.keras")
CLASSES_PATH = os.path.join(ROOT_DIR, "models", "class_names.json")

# On charge le modèle UNE SEULE FOIS, au démarrage du programme.
# (le recharger à chaque prédiction serait très lent)
MODEL = keras.models.load_model(MODEL_PATH)

# On charge la liste des classes dans l'ordre de l'entraînement
with open(CLASSES_PATH) as f:
    CLASSES = json.load(f)


def preprocess(img):
    """
    Transforme le dessin de l'utilisateur au format Quick, Draw! :
    28x28 pixels, niveaux de gris, trait BLANC sur fond NOIR, dessin centré.

    Paramètre : img = tableau NumPy (couleur BGR ou gris)
    Retourne  : tableau de forme (1, 28, 28, 1) normalisé entre 0 et 1,
                ou None si le canvas est vide.
    """
    # Étape 1 : passer en niveaux de gris si l'image est en couleur
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Étape 2 : mettre le trait en blanc sur fond noir.
    # Si la moyenne est claire, le fond est blanc : on inverse les couleurs.
    if img.mean() > 127:
        img = 255 - img

    # Étape 3 : trouver où se trouve le trait (pixels assez clairs)
    ys, xs = np.where(img > 30)
    if len(xs) == 0:
        return None            # rien n'a été dessiné

    # Étape 4 : recadrer l'image autour du dessin (supprime les marges vides)
    img = img[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    # Étape 5 : placer le dessin au centre d'un carré noir (avec 20 % de marge).
    # Un carré évite de déformer le dessin quand on le réduit.
    h, w = img.shape
    side = int(max(h, w) * 1.2)
    canvas = np.zeros((side, side), dtype=np.uint8)
    oy, ox = (side - h) // 2, (side - w) // 2
    canvas[oy:oy + h, ox:ox + w] = img

    # Étape 6 : réduire à 28x28 (INTER_AREA = meilleure méthode pour réduire)
    canvas = cv2.resize(canvas, (28, 28), interpolation=cv2.INTER_AREA)

    # Étape 7 : normaliser (0-255 vers 0-1) et mettre la forme attendue
    # par Keras : (1 image, 28, 28, 1 canal)
    return canvas.astype("float32").reshape(1, 28, 28, 1) / 255.0


def predict_drawing(img):
    """
    Prédit la catégorie d'un dessin.

    Paramètre : img = image du canvas (tableau NumPy)
    Retourne  : (nom_de_la_classe, score entre 0 et 1)
                ou (None, 0.0) si le canvas est vide.
    """
    x = preprocess(img)
    if x is None:
        return None, 0.0

    # Le modèle renvoie 5 probabilités (une par classe)
    probs = MODEL.predict(x, verbose=0)[0]

    # On garde la plus grande : c'est la classe prédite
    i = int(np.argmax(probs))
    return CLASSES[i], float(probs[i])