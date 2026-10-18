 #pour l'application de reconnaissance et predictions de dessins en temps reels

# Importation des bibliothèques nécessaires
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw


class AISketchApp:
    """Interface graphique de dessin pour le projet AI Sketch."""

    def __init__(self, root):
        # Configuration de la fenêtre principale
        self.root = root
        self.root.title("AI Sketch - Dessin intelligent")
        self.root.geometry("1000x700")
        self.root.minsize(750, 500)

        # Couleurs de l'interface
        self.couleur_fond = "#F2F4F8"
        self.couleur_bouton = "#2563EB"

        self.root.configure(bg=self.couleur_fond)

        # Variables utilisées par le pinceau
        self.taille_pinceau = tk.IntVar(value=5)
        self.couleur_pinceau = "black"

        # Variables permettant de mémoriser la position précédente
        self.x_precedent = None
        self.y_precedent = None

     # Image Pillow associée au dessin pour l'enregistrement
        self.image = None
        self.dessin = None

        # Création de la structure de l'interface
        self.creer_interface()

    def creer_interface(self):
        """Crée les différents éléments de l'interface."""

        # En-tête de l'application
        entete = tk.Frame(self.root, bg=self.couleur_fond)
        entete.pack(fill="x", padx=20, pady=(15, 5))

        titre = tk.Label(
            entete,
            text="AI SKETCH",
            font=("Arial", 22, "bold"),
            bg=self.couleur_fond,
            fg="#1E293B"
        )
        titre.pack(anchor="w")

        sous_titre = tk.Label(
            entete,
            text="Dessine un objet et prépare sa reconnaissance par l'IA.",
            font=("Arial", 11),
            bg=self.couleur_fond,
            fg="#64748B"
        )
        sous_titre.pack(anchor="w", pady=(3, 0))

        # Barre d'outils
        barre_outils = tk.Frame(self.root, bg=self.couleur_fond)
        barre_outils.pack(fill="x", padx=20, pady=10)

        # Réglage de la taille du pinceau
        label_pinceau = tk.Label(
            barre_outils,
            text="Taille du pinceau :",
            font=("Arial", 10),
            bg=self.couleur_fond
        )
        label_pinceau.pack(side="left", padx=(0, 8))

        curseur = tk.Scale(
            barre_outils,
            from_=1,
            to=25,
            orient="horizontal",
            variable=self.taille_pinceau,
            length=150,
            bg=self.couleur_fond,
            highlightthickness=0
        )
        curseur.pack(side="left", padx=(0, 15))

        # Bouton permettant d'effacer le dessin
        bouton_effacer = tk.Button(
            barre_outils,
            text="Effacer",
            command=self.effacer_dessin,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6,
            cursor="hand2"
        )
        bouton_effacer.pack(side="left", padx=5)

        # Bouton permettant d'enregistrer le dessin
        bouton_enregistrer = tk.Button(
            barre_outils,
            text="Enregistrer",
            command=self.enregistrer_dessin,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6,
            cursor="hand2"
        )
        bouton_enregistrer.pack(side="left", padx=5)

        # Bouton de reconnaissance : le modèle n'est pas encore connecté
        bouton_reconnaitre = tk.Button(
            barre_outils,
            text="Reconnaître",
            command=self.reconnaitre_dessin,
            font=("Arial", 10, "bold"),
            bg=self.couleur_bouton,
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            padx=12,
            pady=6,
            cursor="hand2"
        )
        bouton_reconnaitre.pack(side="left", padx=5)

        # Conteneur de la zone de dessin
        cadre_dessin = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="groove"
        )
        cadre_dessin.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 10)
        )

        # Zone blanche où l'utilisateur dessine
        self.canvas = tk.Canvas(
            cadre_dessin,
            bg="white",
            cursor="cross",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
    
        # Prépare la création d'une image adaptée aux dimensions du canevas.
        self.canvas.bind("<Configure>", self.ajuster_image)

        # Association des événements de la souris
        self.canvas.bind("<Button-1>", self.commencer_dessin)
        self.canvas.bind("<B1-Motion>", self.dessiner)
        self.canvas.bind("<ButtonRelease-1>", self.terminer_dessin)

        # Zone affichant le résultat ou l'état de l'application
        self.resultat = tk.Label(
            self.root,
            text="Résultat : aucun dessin reconnu pour le moment.",
            font=("Arial", 11, "bold"),
            bg=self.couleur_fond,
            fg="#334155",
            anchor="w"
        )
        self.resultat.pack(fill="x", padx=20, pady=(0, 15))

    def ajuster_image(self, evenement):
        """Adapte l'image Pillow aux dimensions réelles du canevas."""

        largeur = max(1, evenement.width)
        hauteur = max(1, evenement.height)

        # Crée une image blanche aux dimensions du canevas.
        nouvelle_image = Image.new("RGB", (largeur, hauteur), "white")

        # Conserve le dessin existant lorsque la zone est redimensionnée.
        if self.image is not None:
            nouvelle_image.paste(self.image, (0, 0))

        self.image = nouvelle_image
        self.dessin = ImageDraw.Draw(self.image)
    
    def commencer_dessin(self, evenement):
        """Mémorise la position initiale du trait."""

        self.x_precedent = evenement.x
        self.y_precedent = evenement.y

        # Affiche un point pour que les clics simples soient visibles
        taille = self.taille_pinceau.get()

        self.canvas.create_oval(
            evenement.x - taille / 2,
            evenement.y - taille / 2,
            evenement.x + taille / 2,
            evenement.y + taille / 2,
            fill=self.couleur_pinceau,
            outline=self.couleur_pinceau
        )

        self.dessin.ellipse(
            (
                evenement.x - taille / 2,
                evenement.y - taille / 2,
                evenement.x + taille / 2,
                evenement.y + taille / 2
            ),
            fill=self.couleur_pinceau
        )

    def dessiner(self, evenement):
        """Dessine un trait en suivant le mouvement de la souris."""

        if self.x_precedent is not None and self.y_precedent is not None:
            taille = self.taille_pinceau.get()

            # Dessine le trait sur le Canvas de Tkinter
            self.canvas.create_line(
                self.x_precedent,
                self.y_precedent,
                evenement.x,
                evenement.y,
                fill=self.couleur_pinceau,
                width=taille,
                capstyle=tk.ROUND,
                smooth=True
            )

            # Dessine également le trait sur l'image Pillow
            self.dessin.line(
                (
                    self.x_precedent,
                    self.y_precedent,
                    evenement.x,
                    evenement.y
                ),
                fill=self.couleur_pinceau,
                width=taille
            )

            # Arrondit les extrémités pour améliorer le rendu
            rayon = taille / 2
            self.dessin.ellipse(
                (
                    evenement.x - rayon,
                    evenement.y - rayon,
                    evenement.x + rayon,
                    evenement.y + rayon
                ),
                fill=self.couleur_pinceau
            )

        # Actualise la position précédente
        self.x_precedent = evenement.x
        self.y_precedent = evenement.y

    def terminer_dessin(self, evenement):
        """Réinitialise la position mémorisée après le dessin."""

        self.x_precedent = None
        self.y_precedent = None

    def effacer_dessin(self):
        """Efface la zone de dessin et réinitialise l'image."""

        self.canvas.delete("all")

        # Réinitialise l'image en conservant les dimensions actuelles.
        largeur = max(1, self.canvas.winfo_width())
        hauteur = max(1, self.canvas.winfo_height())

        self.image = Image.new("RGB", (largeur, hauteur), "white")
        self.dessin = ImageDraw.Draw(self.image)
        # Réinitialise le message de résultat
        self.resultat.config(
            text="Résultat : aucun dessin reconnu pour le moment."
        )

    def enregistrer_dessin(self):
        """Ouvre une boîte de dialogue pour enregistrer le dessin."""

        chemin = filedialog.asksaveasfilename(
            title="Enregistrer le dessin",
            defaultextension=".png",
            filetypes=[("Image PNG", "*.png")]
        )

        # Vérifie si l'utilisateur a choisi un emplacement
        if chemin:
            try:
                self.image.save(chemin, format="PNG")
                messagebox.showinfo(
                    "Enregistrement réussi",
                    "Ton dessin a été enregistré avec succès."
                )
            except OSError as erreur:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'enregistrer le dessin :\n{erreur}"
                )

    def reconnaitre_dessin(self):
        """Prépare l'action de reconnaissance sans appeler le modèle IA."""

        self.resultat.config(
            text="Résultat : la reconnaissance sera disponible lorsque "
                 "le modèle d'IA sera connecté."
        )


# Point d'entrée du programme
if __name__ == "__main__":
    # Création de la fenêtre principale
    fenetre = tk.Tk()

    # Création de l'application
    application = AISketchApp(fenetre)

    # Lancement de la boucle principale de Tkinter
    fenetre.mainloop()
