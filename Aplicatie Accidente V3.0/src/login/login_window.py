import customtkinter as ctk
from src.utils.data_manager import save_login_data, load_login_data, clear_login_data

class LoginWindow(ctk.CTkToplevel):
    """
    Fereastra de login a aplicației.
    Gestionează autentificarea agentului și salvarea preferințelor de acces local.
    """
    def __init__(self, master, on_login_success_callback):
        super().__init__(master)
        self.on_login_success = on_login_success_callback

        # Configurare fereastră
        self.title("Autentificare BARSV")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Asigurăm că fereastra apare deasupra și blochează interacțiunea cu restul app
        self.transient(master)
        self.grab_set()

        # Layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        # Elemente UI
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Autentificare Agent", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(25, 20))

        self.username_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Introduceți numele complet (ex: Ag. Popescu Ion)",
            width=300,
            height=35
        )
        self.username_entry.pack(pady=10, padx=20)

        # Opțiune salvare utilizator
        self.save_user_var = ctk.StringVar(value="off")
        self.save_user_checkbox = ctk.CTkCheckBox(
            main_frame, 
            text="Memorare utilizator pe această stație", 
            variable=self.save_user_var, 
            onvalue="on", 
            offvalue="off"
        )
        self.save_user_checkbox.pack(pady=10)

        self.login_button = ctk.CTkButton(
            main_frame, 
            text="Acces Aplicație", 
            command=self.attempt_login,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.login_button.pack(pady=(20, 20), padx=20, fill="x")
        
        # Bind taste
        self.bind('<Return>', lambda e: self.attempt_login())
        
        # Încărcare automată dacă există date salvate
        self.load_and_set_user()
        
        # Focus pe câmpul de text la deschidere
        self.username_entry.focus_set()

    def load_and_set_user(self):
        """Încarcă ultimul nume de utilizator din data_manager."""
        saved_username = load_login_data()
        if saved_username:
            self.username_entry.insert(0, saved_username)
            self.save_user_var.set("on")

    def attempt_login(self):
        """Validarea numelui și declanșarea callback-ului de succes."""
        username = self.username_entry.get().strip()
        
        if not username:
            # Opțional: am putea adăuga un label roșu de eroare aici
            return

        # Gestionare salvare preferințe
        if self.save_user_var.get() == "on":
            save_login_data(username)
        else:
            clear_login_data()
        
        # Notificăm controller-ul (main.py) că logarea a reușit
        self.on_login_success(username)