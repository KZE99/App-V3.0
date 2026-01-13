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
        self.title("BARSV APP V1.0 2026")
        self.geometry("900x700")
        self.resizable(True, True)

        # Asigurăm că fereastra apare deasupra și blochează interacțiunea cu restul app
        self.transient(master)
        self.grab_set()

        # Layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Card central
        main_frame = ctk.CTkFrame(self, corner_radius=15, width=400, height=450)
        main_frame.grid(row=0, column=0, padx=20, pady=20)
        main_frame.grid_propagate(False) # Force size
        main_frame.grid_columnconfigure(0, weight=1)

        # Elemente UI
        title_label = ctk.CTkLabel(
            main_frame,
            text="Autentificare",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title_label.pack(pady=(50, 30))

        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="user_01",
            width=300,
            height=40,
            corner_radius=10
        )
        self.username_entry.pack(pady=(10, 10))

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="*********",
            width=300,
            height=40,
            show="*",
            corner_radius=10
        )
        self.password_entry.pack(pady=(10, 10))

        # Show/Hide Password Button
        self.show_password_button = ctk.CTkButton(
            self.password_entry,
            text="👁",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            text_color=("gray10", "gray90"),
            command=self.toggle_password_visibility
        )
        # Place button inside the entry
        self.show_password_button.place(relx=0.9, rely=0.5, anchor="center")

        # Opțiune salvare utilizator
        self.save_user_var = ctk.StringVar(value="off")
        self.save_user_checkbox = ctk.CTkCheckBox(
            main_frame,
            text="Ține-mă minte",
            variable=self.save_user_var,
            onvalue="on",
            offvalue="off",
            font=ctk.CTkFont(size=14)
        )
        self.save_user_checkbox.pack(pady=(15, 20))

        self.login_button = ctk.CTkButton(
            main_frame,
            text="Logare",
            command=self.attempt_login,
            height=40,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.login_button.pack(pady=(10, 30))

        # Bind taste
        self.bind('<Return>', lambda e: self.attempt_login())

        # Încărcare automată dacă există date salvate
        self.load_and_set_user()

        # Focus pe câmpul de text la deschidere
        self.username_entry.focus_set()

    def toggle_password_visibility(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def load_and_set_user(self):
        """Încarcă ultimul nume de utilizator din data_manager."""
        saved_username = load_login_data()
        if saved_username:
            self.username_entry.insert(0, saved_username)
            self.save_user_var.set("on")

    def attempt_login(self):
        """Validarea numelui și declanșarea callback-ului de succes."""
        username = self.username_entry.get().strip()
        # Password is read but not currently validated against a backend
        password = self.password_entry.get().strip()

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
