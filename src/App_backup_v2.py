# ============================================================
# PROJET AI SKETCH
# Interface graphique de dessin avec Tkinter et Pillow
# ============================================================

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw


class AISketchApp:
    """Interface graphique de dessin pour le projet AI Sketch."""

    def __init__(self, root):
        # Configuration de la fenêtre principale
        self.root = root
        self.root.title("AI Sketch | Dessin intelligent")
        self.root.geometry("1100x750")
        self.root.minsize(800, 600)
        self.root.configure(bg="#F1F5F9")

        # Palette de couleurs
        self.couleur_fond = "#F1F5F9"
        self.couleur_nuit = "#172554"
        self.couleur_bleu = "#2563EB"
        self.couleur_bleu_fonce = "#1D4ED8"
        self.couleur_vert = "#059669"
        self.couleur_rouge = "#DC2626"
        self.couleur_texte = "#1E293B"
        self.couleur_secondaire = "#64748B"
        self.couleur_bordure = "#E2E8F0"

        # Variables du pinceau
        self.taille_pinceau = tk.IntVar(value=5)
        self.couleur_pinceau = "#172554"

        # Position précédente de la souris
        self.x_precedent = None
        self.y_precedent = None

        # Image Pillow utilisée pour enregistrer le dessin
        self.image = None
        self.dessin = None

        # Création de l'interface
        self.creer_interface()

    def creer_interface(self):
        """Construit les différentes parties de l'interface."""

        # ----------------------------------------------------
        # 1. EN-TÊTE
        # ----------------------------------------------------
        entete = tk.Frame(
            self.root,
            bg=self.couleur_nuit,
            height=100
        )
        entete.pack(fill="x")
        entete.pack_propagate(False)

        bloc_titre = tk.Frame(entete, bg=self.couleur_nuit)
        bloc_titre.pack(side="left", padx=30, pady=15)

        titre = tk.Label(
            bloc_titre,
            text="AI SKETCH",
            font=("Segoe UI", 23, "bold"),
            bg=self.couleur_nuit,
            fg="white"
        )
        titre.pack(anchor="w")

        sous_titre = tk.Label(
            bloc_titre,
            text="Dessine. Enregistre. Prépare la reconnaissance.",
            font=("Segoe UI", 10),
            bg=self.couleur_nuit,
            fg="#CBD5E1"
        )
        sous_titre.pack(anchor="w", pady=(2, 0))

        # Petit badge décoratif
        badge = tk.Label(
            entete,
            text="ESPACE CRÉATIF",
            font=("Segoe UI", 9, "bold"),
            bg="#1E3A8A",
            fg="white",
            padx=14,
            pady=8
        )
        badge.pack(side="right", padx=30)

        # ----------------------------------------------------
        # 2. CONTENU PRINCIPAL
        # ----------------------------------------------------
        contenu = tk.Frame(self.root, bg=self.couleur_fond)
        contenu.pack(fill="both", expand=True, padx=24, pady=20)

        # Titre de la section de dessin
        titre_section = tk.Label(
            contenu,
            text="Ma zone de dessin",
            font=("Segoe UI", 16, "bold"),
            bg=self.couleur_fond,
            fg=self.couleur_texte
        )
        titre_section.pack(anchor="w")

        description = tk.Label(
            contenu,
            text="Utilise ta souris pour dessiner librement dans la zone blanche.",
            font=("Segoe UI", 10),
            bg=self.couleur_fond,
            fg=self.couleur_secondaire
        )
        description.pack(anchor="w", pady=(4, 14))

        # ----------------------------------------------------
        # 3. BARRE D'OUTILS
        # ----------------------------------------------------
        barre_outils = tk.Frame(
            contenu,
            bg="white",
            highlightbackground=self.couleur_bordure,
            highlightthickness=1
        )
        barre_outils.pack(fill="x", pady=(0, 14))

        # Réglage de la taille du pinceau
        cadre_pinceau = tk.Frame(barre_outils, bg="white")
        cadre_pinceau.pack(side="left", padx=16, pady=12)

        label_pinceau = tk.Label(
            cadre_pinceau,
            text="ÉPAISSEUR DU TRAIT",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg=self.couleur_secondaire
        )
        label_pinceau.pack(anchor="w")

        curseur = tk.Scale(
            cadre_pinceau,
            from_=1,
            to=25,
            orient="horizontal",
            variable=self.taille_pinceau,
            length=150,
            showvalue=True,
            resolution=1,
            bg="white",
            fg=self.couleur_texte,
            troughcolor="#DBEAFE",
            activebackground=self.couleur_bleu,
            highlightthickness=0,
            bd=0
        )
        curseur.pack(anchor="w")

        # Séparateur visuel
        separateur = tk.Frame(
            barre_outils,
            bg=self.couleur_bordure,
            width=1
        )
        separateur.pack(side="left", fill="y", pady=12, padx=5)

        # Boutons d'action
        cadre_boutons = tk.Frame(barre_outils, bg="white")
        cadre_boutons.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=18
        )

        bouton_effacer = tk.Button(
            cadre_boutons,
            text="Effacer",
            command=self.effacer_dessin,
            font=("Segoe UI", 10, "bold"),
            bg="#FEE2E2",
            fg="#991B1B",
            activebackground="#FECACA",
            activeforeground="#7F1D1D",
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2"
        )
        bouton_effacer.pack(side="left", padx=5)

        bouton_enregistrer = tk.Button(
            cadre_boutons,
            text="Enregistrer",
            command=self.enregistrer_dessin,
            font=("Segoe UI", 10, "bold"),
            bg="#D1FAE5",
            fg="#065F46",
            activebackground="#A7F3D0",
            activeforeground="#064E3B",
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2"
        )
        bouton_enregistrer.pack(side="left", padx=5)

        bouton_reconnaitre = tk.Button(
            cadre_boutons,
            text="Reconnaître",
            command=self.reconnaitre_dessin,
            font=("Segoe UI", 10, "bold"),
            bg=self.couleur_bleu,
            fg="white",
            activebackground=self.couleur_bleu_fonce,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        )
        bouton_reconnaitre.pack(side="left", padx=5)

        # ----------------------------------------------------
        # 4. ZONE DE DESSIN
        # ----------------------------------------------------
        cadre_dessin = tk.Frame(
            contenu,
            bg="white",
            highlightbackground=self.couleur_bordure,
            highlightthickness=1
        )
        cadre_dessin.pack(fill="both", expand=True)

        # Canevas sur lequel l'utilisateur dessine
        self.canvas = tk.Canvas(
            cadre_dessin,
            bg="white",
            cursor="cross",
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        # Création et adaptation de l'image Pillow
        self.canvas.bind("<Configure>", self.ajuster_image)

        # Événements de la souris
        self.canvas.bind("<Button-1>", self.commencer_dessin)
        self.canvas.bind("<B1-Motion>", self.dessiner)
        self.canvas.bind("<ButtonRelease-1>", self.terminer_dessin)

        # ----------------------------------------------------
        # 5. PANNEAU DE RÉSULTAT
        # ----------------------------------------------------
        panneau_resultat = tk.Frame(
            contenu,
            bg="#EFF6FF",
            highlightbackground="#BFDBFE",
            highlightthickness=1
        )
        panneau_resultat.pack(fill="x", pady=(14, 0))

        icone = tk.Label(
            panneau_resultat,
            text="IA",
            font=("Segoe UI", 12, "bold"),
            bg="#DBEAFE",
            fg=self.couleur_bleu,
            padx=12,
            pady=8
        )
        icone.pack(side="left", padx=12, pady=10)

        cadre_resultat = tk.Frame(
            panneau_resultat,
            bg="#EFF6FF"
        )
        cadre_resultat.pack(
            side="left",
            fill="both",
            expand=True,
            pady=10
        )

        label_resultat = tk.Label(
            cadre_resultat,
            text="RÉSULTAT DE LA RECONNAISSANCE",
            font=("Segoe UI", 9, "bold"),
            bg="#EFF6FF",
            fg=self.couleur_secondaire
        )
        label_resultat.pack(anchor="w")

        self.resultat = tk.Label(
            cadre_resultat,
            text="Ton dessin apparaîtra ici après la reconnaissance.",
            font=("Segoe UI", 10),
            bg="#EFF6FF",
            fg=self.couleur_texte,
            anchor="w"
        )
        self.resultat.pack(anchor="w", pady=(3, 0))

        # Barre d'état située en bas de la fenêtre
        self.statut = tk.Label(
            self.root,
            text="Prêt à dessiner",
            font=("Segoe UI", 9),
            bg=self.couleur_fond,
            fg=self.couleur_secondaire,
            anchor="w"
        )
        self.statut.pack(fill="x", padx=26, pady=(0, 8))

    def ajuster_image(self, evenement):
        """Adapte l'image Pillow à la taille du canevas."""

        largeur = max(1, evenement.width)
        hauteur = max(1, evenement.height)

        # Évite de recréer inutilement une image de même taille
        if (
            self.image is not None
            and self.image.size == (largeur, hauteur)
        ):
            return

        nouvelle_image = Image.new(
            "RGB",
            (largeur, hauteur),
            "white"
        )

        # Conserve la partie du dessin qui entre dans la nouvelle image
        if self.image is not None:
            nouvelle_image.paste(self.image, (0, 0))

        self.image = nouvelle_image
        self.dessin = ImageDraw.Draw(self.image)

    def commencer_dessin(self, evenement):
        """Commence un nouveau trait à la position de la souris."""

        self.x_precedent = evenement.x
        self.y_precedent = evenement.y

        # Vérifie que l'image est prête
        if self.dessin is None:
            self.ajuster_image(evenement)

        taille = self.taille_pinceau.get()
        rayon = taille / 2

        # Dessine un point pour les clics simples
        self.canvas.create_oval(
            evenement.x - rayon,
            evenement.y - rayon,
            evenement.x + rayon,
            evenement.y + rayon,
            fill=self.couleur_pinceau,
            outline=self.couleur_pinceau
        )

        self.dessin.ellipse(
            (
                evenement.x - rayon,
                evenement.y - rayon,
                evenement.x + rayon,
                evenement.y + rayon
            ),
            fill=self.couleur_pinceau
        )

        self.statut.config(text="Dessin en cours...")

    def dessiner(self, evenement):
        """Trace une ligne entre deux positions successives."""

        if self.x_precedent is None or self.y_precedent is None:
            return

        taille = self.taille_pinceau.get()

        # Dessin visuel sur le canevas
        self.canvas.create_line(
            self.x_precedent,
            self.y_precedent,
            evenement.x,
            evenement.y,
            fill=self.couleur_pinceau,
            width=taille,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
            smooth=True,
            splinesteps=24
        )

        # Enregistrement du même trait dans l'image Pillow
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

        # Arrondit les extrémités du trait dans l'image
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

        # Mémorise la position actuelle pour le prochain segment
        self.x_precedent = evenement.x
        self.y_precedent = evenement.y

    def terminer_dessin(self, evenement):
        """Termine le trait lorsque le bouton de la souris est relâché."""

        self.x_precedent = None
        self.y_precedent = None

        self.statut.config(text="Dessin prêt à être enregistré.")

    def effacer_dessin(self):
        """Efface le canevas et réinitialise l'image."""

        self.canvas.delete("all")

        # Recrée une image blanche de la taille du canevas
        largeur = max(1, self.canvas.winfo_width())
        hauteur = max(1, self.canvas.winfo_height())

        self.image = Image.new(
            "RGB",
            (largeur, hauteur),
            "white"
        )
        self.dessin = ImageDraw.Draw(self.image)

        # Réinitialise la position de la souris
        self.x_precedent = None
        self.y_precedent = None

        # Réinitialise les messages
        self.resultat.config(
            text="Ton dessin apparaîtra ici après la reconnaissance."
        )
        self.statut.config(text="Zone de dessin effacée.")

    def enregistrer_dessin(self):
        """Enregistre le dessin dans un fichier PNG."""

        chemin = filedialog.asksaveasfilename(
            title="Enregistrer mon dessin",
            defaultextension=".png",
            filetypes=[
                ("Image PNG", "*.png"),
                ("Tous les fichiers", "*.*")
            ],
            initialfile="mon_dessin.png"
        )

        # L'utilisateur peut annuler la boîte de dialogue
        if not chemin:
            return

        try:
            # Vérifie que l'image existe avant de l'enregistrer
            if self.image is None:
                messagebox.showwarning(
                    "Aucun dessin",
                    "La zone de dessin n'est pas encore prête."
                )
                return

            self.image.save(chemin, format="PNG")

            # Affiche le résultat dans l'interface
            self.statut.config(
                text=f"Dessin enregistré : {chemin}"
            )

            messagebox.showinfo(
                "Enregistrement réussi",
                "Ton dessin a été enregistré au format PNG."
            )

        except (OSError, ValueError) as erreur:
            messagebox.showerror(
                "Erreur d'enregistrement",
                f"Impossible d'enregistrer le dessin.\n\n{erreur}"
            )

    def reconnaitre_dessin(self):
        """Prépare le bouton de reconnaissance sans appeler le modèle."""

        self.resultat.config(
            text=(
                "Le modèle de reconnaissance n'est pas encore connecté."
            )
        )

        self.statut.config(
            text="Interface prête ; reconnaissance en attente du modèle."
        )


# ============================================================
# POINT D'ENTRÉE DU PROGRAMME
# ============================================================

if __name__ == "__main__":
    # Crée la fenêtre principale de Tkinter
    fenetre = tk.Tk()

    # Initialise l'application
    application = AISketchApp(fenetre)

    # Lance la boucle d'événements de Tkinter
    fenetre.mainloop()

