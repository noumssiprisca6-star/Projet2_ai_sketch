# ============================================================
# train.py : entraînement du CNN pour AI Sketch
# Rôle : apprendre à reconnaître 5 dessins (Quick, Draw!)
# Lancer depuis la racine du projet : python src/train.py
# ============================================================

import os
import json

import numpy as np                  # calcul sur les tableaux (les images)
import matplotlib.pyplot as plt     # tracer les graphiques du rapport

# scikit-learn : séparation des données et mesure de la qualité
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, classification_report,
                             ConfusionMatrixDisplay)

# TensorFlow / Keras : construction et entraînement du réseau
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ------------------------------------------------------------
# CHEMINS (calculés à partir de l'emplacement de ce fichier)
# ------------------------------------------------------------
# Racine du projet = dossier parent de src/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(ROOT_DIR, "dataset")      # fichiers .npy
MODELS_DIR = os.path.join(ROOT_DIR, "models")     # modèle entraîné
RESULTS_DIR = os.path.join(ROOT_DIR, "results")   # graphiques du rapport

# ------------------------------------------------------------
# PARAMÈTRES (modifie-les ici, pas dans le reste du code)
# ------------------------------------------------------------
CLASSES = ["car", "cat", "house", "sun"]  # tree retiré temporairement (fichier incomplet)
N_PER_CLASS = 10000                               # dessins utilisés par catégorie
SEED = 42                                         # rend les résultats reproductibles

# ------------------------------------------------------------
# 1. CHARGEMENT DES DONNÉES
# ------------------------------------------------------------
# X contiendra les images, y contiendra les étiquettes (0, 1, 2, 3, 4)
X, y = [], []

for idx, name in enumerate(CLASSES):
    # Chaque fichier .npy contient des dizaines de milliers de dessins.
    # Chaque dessin est une ligne de 784 valeurs (28 x 28 pixels).
    arr = np.load(os.path.join(DATA_DIR, f"{name}.npy"))[:N_PER_CLASS]
    X.append(arr)
    # Étiquette : tous les dessins de "car" reçoivent 0,
    # ceux de "cat" reçoivent 1, etc.
    y.append(np.full(len(arr), idx))

# On colle les 5 catégories dans un seul grand tableau
X = np.concatenate(X).astype("float32") / 255.0   # pixels de 0-255 vers 0-1
y = np.concatenate(y)

# Keras attend des images de forme (nombre, hauteur, largeur, canaux).
# Ici 1 canal car l'image est en niveaux de gris.
X = X.reshape(-1, 28, 28, 1)
print("Données :", X.shape, "| classes :", CLASSES)

# Vérification visuelle : on doit voir un dessin BLANC sur fond NOIR.
# Ferme la fenêtre pour continuer l'entraînement.
plt.imshow(X[0].reshape(28, 28), cmap="gray")
plt.title(f"Classe : {CLASSES[y[0]]}")
plt.show()

# ------------------------------------------------------------
# 2. SÉPARATION TRAIN / VALIDATION / TEST
# ------------------------------------------------------------
# train      (70 %) : le modèle apprend dessus
# validation (15 %) : on surveille le modèle pendant l'entraînement
# test       (15 %) : note finale, sur des images JAMAIS vues
#
# stratify=y : garde la même proportion de chaque classe partout.
X_train, X_tmp, y_train, y_tmp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=SEED)
X_val, X_test, y_val, y_test = train_test_split(
    X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=SEED)

# ------------------------------------------------------------
# 3. CONSTRUCTION DU CNN
# ------------------------------------------------------------
model = keras.Sequential([
    # Entrée : une image 28x28 avec 1 canal (gris)
    layers.Input(shape=(28, 28, 1)),

    # Bloc 1 : 32 filtres 3x3 qui détectent des formes simples
    # (traits, courbes, angles). ReLU garde les valeurs positives.
    layers.Conv2D(32, 3, activation="relu"),
    # MaxPooling : divise la taille par 2 en gardant le plus important
    layers.MaxPooling2D(),

    # Bloc 2 : 64 filtres qui combinent les formes simples
    # en formes complexes (toit, roue, oreille...)
    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),

    # Flatten : transforme les images en une longue liste de nombres
    layers.Flatten(),
    # Dropout : éteint 30 % des neurones au hasard pendant l'entraînement,
    # pour éviter que le modèle apprenne par coeur (surapprentissage)
    layers.Dropout(0.3),

    # Couche dense : combine toutes les informations pour décider
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),

    # Sortie : 5 neurones (un par catégorie).
    # Softmax les transforme en probabilités dont la somme vaut 1.
    # La plus grande = classe prédite = score de confiance.
    layers.Dense(len(CLASSES), activation="softmax"),
])

# compile : on choisit comment le modèle va apprendre
model.compile(
    optimizer="adam",                        # algorithme qui ajuste le réseau
    loss="sparse_categorical_crossentropy",  # mesure l'erreur (étiquettes en entiers)
    metrics=["accuracy"],                    # pourcentage de bonnes réponses
)
model.summary()   # affiche l'architecture (à mettre dans le rapport)

# ------------------------------------------------------------
# 4. ENTRAÎNEMENT
# ------------------------------------------------------------
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),   # contrôle à chaque époque
    epochs=15,                        # nombre maximum de passages sur les données
    batch_size=128,                   # nombre d'images traitées à la fois
    callbacks=[
        # Arrête l'entraînement si la validation ne s'améliore plus
        # pendant 3 époques, et revient aux meilleurs poids.
        keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    ],
)

# ------------------------------------------------------------
# 5. ÉVALUATION SUR LE TEST (la vraie note du modèle)
# ------------------------------------------------------------
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Accuracy sur le test : {acc * 100:.2f} %")

# Prédictions : pour chaque image, on prend la classe de plus forte probabilité
y_pred = np.argmax(model.predict(X_test), axis=1)

# Rapport par classe : precision, recall, f1-score (à mettre dans le rapport)
print(classification_report(y_test, y_pred, target_names=CLASSES))

# Dossier pour ranger les graphiques
os.makedirs(RESULTS_DIR, exist_ok=True)

# Matrice de confusion : ligne = vraie classe, colonne = classe prédite.
# Les chiffres hors de la diagonale sont les erreurs (qui est confondu avec qui).
ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred),
                       display_labels=CLASSES).plot(cmap="Blues")
plt.savefig(os.path.join(RESULTS_DIR, "matrice_confusion.png"), dpi=150)

# Courbe d'accuracy : montre si le modèle apprend bien
# (si train monte mais validation baisse = surapprentissage)
plt.figure()
plt.plot(history.history["accuracy"], label="train")
plt.plot(history.history["val_accuracy"], label="validation")
plt.xlabel("Époque")
plt.ylabel("Accuracy")
plt.legend()
plt.savefig(os.path.join(RESULTS_DIR, "courbe_accuracy.png"), dpi=150)

# ------------------------------------------------------------
# 6. SAUVEGARDE (ce que les autres vont utiliser)
# ------------------------------------------------------------
os.makedirs(MODELS_DIR, exist_ok=True)
model.save(os.path.join(MODELS_DIR, "ai_sketch.keras"))   # le modèle entraîné

# On sauvegarde l'ordre des classes pour que la prédiction
# utilise EXACTEMENT le même ordre que l'entraînement
with open(os.path.join(MODELS_DIR, "class_names.json"), "w") as f:
    json.dump(CLASSES, f)

print("Modèle sauvegardé dans", os.path.join(MODELS_DIR, "ai_sketch.keras"))