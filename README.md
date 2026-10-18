```markdown
# 🎨 AI Sketch — Reconnaissance Interactive de Dessins

> **Projet Académique — Intelligence Artificielle et Vision par Ordinateur**

Application de bureau interactive permettant de classifier des dessins réalisés à la main en temps réel grâce à un Réseau de Neurones Convolutif (CNN) entraîné sur des données de type *Quick, Draw!*.

---

## 👥 Équipe et Répartition des Rôles

| Membre | Rôle Principal | Dossier / Fichiers Clés |
| :--- | :--- | :--- |
| **Noumssi  & Aroon** | Intégration globale, pipeline de prétraitement OpenCV, inférence IA et filtres bonus | `src/app.py`, `requirements.txt`, `README.md` |
| **Bias** | Collecte, structuration et préparation du Dataset des 5 catégories | `dataset/` |
| **Elisabeth** | Conception, entraînement et exportation du modèle de classification CNN | `src/train.py`, `models/sketch_model.h5` |
| **Aristide** | Développement de l'interface graphique (GUI) et de la zone de dessin interactive | `src/app.py` |

---

## 🛠️ Fonctionnalités de l'Application

* **Zone de Dessin Interactive :** Interface fluide pour dessiner au curseur (pinceau, effacement, réinitialisation).
* **Prétraitement d'Image Avancé (OpenCV) :** Conversion en niveaux de gris, inversion des couleurs (fond noir / trait blanc), redimensionnement normalisé à 28x28 pixels pour correspondre aux attentes du modèle.
* **Inférence en Temps Réel :** Classification instantanée parmi les 5 catégories cibles (Maison, Arbre, Chat, Soleil, Voiture) avec affichage du score de confiance.
* **Filtres Artistiques (Bonus) :** Application dynamique de traitements d'images (Flou gaussien, détection de contours de Canny).

---

## 📂 Arborescence du Projet

```text
Projet2_ai_sketch/
├── dataset/                  # Stockage des fichiers de données (.npy)
├── models/                   # Poids et architectures du modèle entraîné
├── src/                      
│   ├── app.py                # Interface graphique & moteur de prédiction
│   └── train.py              # Script d'entraînement du modèle CNN
├── .gitignore                # Exclusion des fichiers temporaires et de l'environnement
├── README.md                 # Documentation du projet
└── requirements.txt          # Dépendances du projet

```

---

## 🚀 Guide d'Installation et de Lancement

### 1. Cloner le dépôt et se placer dans le dossier

```bash
git clone code du repo
cd Projet2_ai_sketch

```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
# Sur Windows (PowerShell) :
.\venv\Scripts\activate
# Sur Mac / Linux :
source venv/bin/activate

```

### 3. Installer les dépendances requises

```bash
pip install -r requirements.txt

```

### 4. Entraîner le modèle (si nécessaire)

Si le fichier `models/sketch_model.h5` n'est pas encore généré :

```bash
python src/train.py

```

### 5. Lancer l'application

```bash
python src/app.py

```

---

## 📌 Licence & Contexte

Projet réalisé dans le cadre du cursus académique en informatique et intelligence artificielle. Tous droits réservés à l'équipe de développement.

```

```
