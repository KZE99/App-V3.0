import customtkinter as ctk
# Importăm punctul de intrare pentru modulul de accidente
from src.accident_rutier.accident_main_page import AccidentMainPage

class MainPage(ctk.CTkFrame):
    """
    Pagina principală a aplicației (Dashboard).
    Permite utilizatorului să aleagă modulul de lucru dorit.
    """
    def __init__(self, master, current_user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.current_user = current_user
        
        # Referințe pentru ferestrele secundare
        self.accident_window = None

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(40, 20))

        self.welcome_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Salutare, {self.current_user}!", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.welcome_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Selectați modulul pe care doriți să îl accesați astăzi:", 
            font=ctk.CTkFont(size=16),
            text_color=("gray60", "gray70")
        )
        self.subtitle_label.pack(anchor="w", padx=40, pady=(0, 30))

        # --- GRID OPȚIUNI ---
        self.options_container = ctk.CTkFrame(self, fg_color="transparent")
        self.options_container.pack(fill="both", expand=True, padx=20)
        
        # Configurare coloane (3 module principale)
        self.options_container.grid_columnconfigure((0, 1, 2), weight=1, pad=20)

        # Crearea modulelor
        self.create_module_card(
            "Accident Rutier", 
            "Gestiune completă dosare,\nvehicule și victime.", 
            self.open_accident_rutier, 
            0
        )
        
        self.create_module_card(
            "Deplasare Eveniment", 
            "Culegere date rapidă\nla fața locului.", 
            self.open_deplasare, 
            1
        )
        
        self.create_module_card(
            "Declarație Simplă", 
            "Generare rapidă de\ndeclarații martor/victimă.", 
            self.open_declaratie, 
            2
        )

    def create_module_card(self, title, description, command, column):
        """Creează un card vizual pentru un modul al aplicației."""
        card = ctk.CTkFrame(self.options_container, corner_radius=15, border_width=1, border_color=("gray80", "gray20"))
        card.grid(row=0, column=column, sticky="nsew", padx=15, pady=15)
        
        # Placeholder pentru Iconiță (Poate fi înlocuit cu ctk.CTkImage)
        icon_label = ctk.CTkLabel(
            card, 
            text="📂", 
            font=ctk.CTkFont(size=50),
            height=100
        )
        icon_label.pack(pady=(25, 10))

        title_label = ctk.CTkLabel(
            card, 
            text=title, 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=5)

        desc_label = ctk.CTkLabel(
            card, 
            text=description, 
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray60")
        )
        desc_label.pack(pady=(0, 20), padx=10)

        action_btn = ctk.CTkButton(
            card, 
            text="Lansează Modul", 
            command=command,
            corner_radius=10,
            height=35
        )
        action_btn.pack(pady=(0, 25), padx=20, fill="x")

    def open_accident_rutier(self):
        """Deschide fereastra de date primare pentru accident rutier."""
        if self.accident_window is None or not self.accident_window.winfo_exists():
            # Cream fereastra Toplevel pentru accident
            self.accident_window = AccidentMainPage(master=self.master, current_user=self.current_user)
            
            # Deoarece este o fereastră nouă, trebuie să aplicăm manual patch-urile de diacritice
            # (main.py are funcția apply_global_patches disponibilă via self.master)
            if hasattr(self.master, 'apply_global_patches'):
                self.master.apply_global_patches(self.accident_window)
        else:
            self.accident_window.focus()

    def open_deplasare(self):
        """Funcționalitate în dezvoltare."""
        # Aici se poate implementa o notificare personalizată mai târziu
        print("Modulul 'Deplasare Eveniment' va fi implementat curând.")

    def open_declaratie(self):
        """Funcționalitate în dezvoltare."""
        print("Modulul 'Declarație' va fi implementat curând.")