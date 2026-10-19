import numpy as np
import cv2
from PIL import Image

class ImageProcessor:
    """Gère les pré-traitements de l'image et les filtres artistiques OpenCV ."""

    @staticmethod
    def preparer_image_pour_ia(image_pil):
        """
        Prépare l'image du dessin pour le modèle CNN (28x28, normalisée).
        """
        if image_pil is None:
            return None

        image_np = np.array(image_pil)
        gris = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        gris_inverse = cv2.bitwise_not(gris)
        image_reduite = cv2.resize(gris_inverse, (28, 28), interpolation=cv2.INTER_AREA)
        image_normalisee = image_reduite.astype("float32") / 255.0
        image_prete = np.expand_dims(image_normalisee, axis=(0, -1))

        return image_prete

    @staticmethod
    def appliquer_filtre_artistique(image_pil, type_filtre="contours"):
        """
        Applique un effet visuel OpenCV sur l'image du dessin.
        - 'contours' : Extrait les traits nets (Canny).
        - 'flou' : Adoucit l'image (GaussianBlur).
        - 'croquis' : Effet esquisse au crayon (pencilSketch).
        Retourne une nouvelle image au format PIL.
        """
        if image_pil is None:
            return None

        # Convertir l'image PIL en tableau NumPy (RGB)
        image_np = np.array(image_pil)

        if type_filtre == "contours":
            # 1. Détection de contours de Canny
            gris = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            trait_contours = cv2.Canny(gris, 100, 200)
            # Inverser pour garder un fond blanc propre (optionnel) et repasser en 3 canaux RGB
            trait_contours_inv = cv2.bitwise_not(trait_contours)
            resultat_np = cv2.cvtColor(trait_contours_inv, cv2.COLOR_GRAY2RGB)

        elif type_filtre == "flou":
            # 2. Flou gaussien pour adoucir le tracé
            resultat_np = cv2.GaussianBlur(image_np, (15, 15), 0)

        elif type_filtre == "croquis":
            # 3. Effet esquisse/crayon artistique d'OpenCV
            croquis_gris, _ = cv2.pencilSketch(image_np, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            resultat_np = cv2.cvtColor(croquis_gris, cv2.COLOR_GRAY2RGB)

        else:
            resultat_np = image_np

        # Reconvertir le tableau NumPy filtré en objet Image de Pillow
        return Image.fromarray(resultat_np)