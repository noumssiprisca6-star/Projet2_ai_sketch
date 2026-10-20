# 🎨 AI Sketch — Système Interactif de Reconnaissance de Dessins Manuscrits par Vision Artificielle



---

## 📌 Contextualisation & Présentation du Projet

**AI Sketch** est un système applicatif interactif développé dans le cadre académique du module **Intelligence Artificielle & Vision par Ordinateur**. 

L'objectif principal de ce travail est de concevoir, implémenter et déployer une chaîne de traitement complète (*pipeline end-to-end*) combinant de la **Vision par Ordinateur** classique et du **Deep Learning (Apprentissage Profond)**. L'application permet à un utilisateur de réaliser un dessin à main levée sur une zone d'interaction numérique, puis d'obtenir en temps réel une classification automatique de l'esquisse.

### 🎯 Objectifs Pédagogiques et Techniques
- **Ingénierie des données :** Extraction, nettoyage et structuration d'un dataset volumineux d'esquisses au format vectoriel/matriciel.
- **Modélisation Deep Learning :** Conception et entraînement d'un réseau de neurones convolutif (**CNN**) optimisé pour la reconnaissance de formes simples.
- **Traitement d'Image en Temps Réel :** Implémentation de pipelines de normalisation, binarisation et transformations géométriques via **OpenCV**.
- **Co-conception Logicielle :** Intégration du modèle entraîné au sein d'une interface graphique interactive (**GUI**) réactive et intuitive.

---

## 👥 Équipe de Développement & Organisation du Travail

Le projet a été mené de manière collaborative selon la répartition des responsabilités suivantes :

| Membre | Rôle principal & Domaine d'expertise | Responsabilités & Livrables Techniques |
| :--- | :--- | :--- |
| **Noumssi & Aroon** | **Chefs d'Intégration & Pipeline Computer Vision** | • Conception de l'architecture logicielle globale.<br>• Implémentation du pipeline de prétraitement d'images sous OpenCV.<br>• Moteur d'inférence en temps réel et intégration des filtres visuels.<br>• Maintien des dépendances (`requirements.txt`) et documentation (`README.md`). |
| **Bias** | **Data Engineer / Gestionnaire de Données** | • Collecte, nettoyage et extraction du sous-ensemble de données.<br>• Structuration des matrices `.npy` issues du dataset *Quick, Draw!*.<br>• Équilibrage des classes et découpage Train/Validation/Test. |
| **Elisabeth** | **Machine / Deep Learning Engineer** | • Conception de l'architecture du réseau convolutif (CNN).<br>• Entraînement, réglage des hyperparamètres et régularisation.<br>• Exportation et sérialisation des poids du modèle (`sketch_model.h5`). |
| **Aristide** | **Développeur Software & Designer UI/UX** | • Développement de l'interface graphique de bureau (GUI).<br>• Gestion des événements d'entrée utilisateur (Canvas interactif, pinceau, gomme).<br>• Raccordement réactif de l'interface avec les prédictions du modèle. |

---

## 🧠 Architecture du Modèle CNN & Traitement des Données

### 📊 1. Jeu de Données (Dataset)
Le modèle s'appuie sur un sous-ensemble du jeu de données international **Quick, Draw!** fourni par Google Creative Lab.
- **Classes ciblées (5) :** `Maison` *(House)*, `Arbre` *(Tree)*, `Chat` *(Cat)*, `Soleil` *(Sun)*, `Voiture` *(Car)*.
- **Format des données :** Fichiers binaires NumPy (`.npy`) contenant des images en niveaux de gris normalisées de dimension $28 \times 28$ pixels.

### 📐 2. Pipeline de Prétraitement de la Zone de Dessin
Avant d'être soumise au modèle, la capture de la zone de dessin subit la séquence de transformations OpenCV suivante :
1. **Extraction de la région d'intérêt (ROI) :** Isolement de la zone du canvas.
2. **Conversion en niveaux de gris :** Réduction à un canal unique.
3. **Inversion chromatique :** Passage d'un fond blanc avec trait noir à un fond noir avec trait blanc (pour correspondre au standard d'apprentissage).
4. **Redimensionnement & Centrage :** Traitement de l'image pour atteindre une résolution stricte de $28 \times 28$ pixels.
5. **Normalisation matricielle :** Divison des valeurs de pixels $[0, 255]$ par $255.0$ pour obtenir un tenseur normalisé dans $[0.0, 1.0]$.

### 🏗️ 3. Architecture du Réseau Convolutif (CNN)
Le modèle est structuré pour offrir un compromis optimal entre précision de classification et légèreté d'exécution en temps réel :
- **Couche d'entrée :** Tenseur de forme $(28, 28, 1)$.
- **Blocs Convolutifs :** Couches `Conv2D` associées à des fonctions d'activation `ReLU`, suivies de couches de sous-échantillonnage `MaxPooling2D` pour l'extraction de motifs spatiaux (lignes, courbes, formes géométriques).
- **Régularisation :** Couches `Dropout` pour prévenir le surapprentissage (*overfitting*).
- **Bloc Dense (Classification) :** Couche `Flatten` suivie d'une couche entièrement connectée (`Dense`), se terminant par une couche de sortie à 5 neurones activée par la fonction **Softmax** pour générer une distribution de probabilités.

---

## 🛠️ Spécifications Métier & Fonctionnalités

- **Zone de Dessin Interactive :** 
  - Traceur à faible latence gérant l'épaisseur du trait.
  - Outils d'effacement partiel (gomme) et de réinitialisation complète du canvas.
- **Inférence en Temps Réel :**
  - Prédiction continue ou à la demande du modèle au fur et à mesure que l'utilisateur dessine.
  - Affichage visuel du score de confiance (probabilité exprimée en %) pour la catégorie dominante ainsi que pour les catégories secondaires.
- **Filtres de Computer Vision (Module Bonus) :**
  - Application en direct de filtres de traitement du signal visuel pour analyser la géométrie du dessin :
    - **Flou Gaussien (*Gaussian Blur*) :** Lissage des bruits de tracé.
    - **Détection de Contours Canny (*Canny Edge Detection*) :** Extraction des gradients d'intensité pour visualiser la structure vectorielle du dessin.

---

## 📂 Architecture Générale du Dépôt

```text
Projet2_ai_sketch/
├── dataset/                  # Fichiers de données binaires (.npy) pour chaque classe
│   ├── maison.npy
│   ├── arbre.npy
│   ├── chat.npy
│   ├── soleil.npy
│   └── voiture.npy
├── models/                   # Poids sérialisés et artefacts du modèle CNN
│   └── sketch_model.h5       # Modèle TensorFlow/Keras entraîné
├── src/                      # Code source de l'application (les fichiers au complet  sont dans le repository nous avons relever les moteurs)
│   ├── app.py                # Point d'entrée : UI Canvas, Inférence OpenCV & Keras
│   └── train.py              # Script d'apprentissage, d'évaluation et d'export du CNN
├── .gitignore                # Exclusion des environnements virtuels et fichiers temporaires
├── README.md                 # Documentation technique et guide d'utilisation
└── requirements.txt          # Spécification stricte des dépendances et versions
