import customtkinter as ctk
import datetime
import tkinter as tk
from tkinter import messagebox
# Importăm fereastra complexă care va gestiona detaliile dosarului
from src.accident_rutier.interfaces.base_accident_window import BaseAccidentWindow
from src.utils.data_manager import load_settings

class AccidentMainPage(ctk.CTkToplevel):
    """
    Fereastra inițială pentru introducerea datelor de bază ale unui accident.
    Determină numărul de tab-uri de vehicule și victime ce vor fi create.
    """
    def __init__(self, master, current_user):
        super().__init__(master)
        self.master = master
        self.current_user = current_user
        self.new_window = None

        # Configurare fereastră
        self.title("Inițializare Dosar Accident Rutier")
        self.geometry("550x700")
        self.resizable(False, False)
        
        # Comportament modal
        self.transient(master)
        self.grab_set()

        # Încărcăm setările pentru a popula listele (agenți, etc.)
        self.app_settings = load_settings()

        # --- LAYOUT ---
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            self.main_container, 
            text="Date Eveniment", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(pady=(10, 20))

        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, label_text="Informații Obligatorii")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # --- CÂMPURI FORMULAR ---
        
        # Agent Constatator
        self.create_label("Agent constatator:")
        # Combinăm utilizatorul curent cu lista de agenți din setări
        lista_agenti = self.app_settings.get('lista_agent2', [])
        if self.current_user not in lista_agenti:
            lista_agenti.insert(0, self.current_user)
            
        self.agent_combobox = ctk.CTkComboBox(self.scroll_frame, values=lista_agenti, width=400)
        self.agent_combobox.pack(fill="x", padx=15, pady=(0, 15))
        self.agent_combobox.set(self.current_user)

        # Data și Ora (Default: Acum)
        now = datetime.datetime.now()
        
        self.create_label("Data eveniment (ZZ-LL-AAAA):")
        self.data_entry = ctk.CTkEntry(self.scroll_frame)
        self.data_entry.insert(0, now.strftime("%d-%m-%Y"))
        self.data_entry.pack(fill="x", padx=15, pady=(0, 15))

        self.create_label("Ora eveniment (HH:MM):")
        self.ora_entry = ctk.CTkEntry(self.scroll_frame)
        self.ora_entry.insert(0, now.strftime("%H:%M"))
        self.ora_entry.pack(fill="x", padx=15, pady=(0, 15))

        # Identificare Dosar
        self.create_label("Număr lucrare / Dosar penal:")
        self.lucrare_entry = ctk.CTkEntry(self.scroll_frame, placeholder_text="ex: 1234567")
        self.lucrare_entry.pack(fill="x", padx=15, pady=(0, 15))

        self.create_label("Locul producerii accidentului:")
        self.locul_entry = ctk.CTkEntry(self.scroll_frame, placeholder_text="Strada / Intersecția / Numărul")
        self.locul_entry.pack(fill="x", padx=15, pady=(0, 15))

        # Configurație Dinamică
        self.create_label("Număr vehicule implicate:")
        self.vehicule_entry = ctk.CTkEntry(self.scroll_frame)
        self.vehicule_entry.insert(0, "2")
        self.vehicule_entry.pack(fill="x", padx=15, pady=(0, 15))

        self.create_label("Număr victime:")
        self.victime_entry = ctk.CTkEntry(self.scroll_frame)
        self.victime_entry.insert(0, "0")
        self.victime_entry.pack(fill="x", padx=15, pady=(0, 15))

        # Autor Necunoscut
        self.an_var = ctk.StringVar(value="Nu")
        an_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        an_frame.pack(fill="x", padx=15, pady=(5, 15))
        ctk.CTkLabel(an_frame, text="Autor necunoscut (Părăsire loc):").pack(side="left")
        ctk.CTkRadioButton(an_frame, text="Da", variable=self.an_var, value="Da").pack(side="left", padx=15)
        ctk.CTkRadioButton(an_frame, text="Nu", variable=self.an_var, value="Nu").pack(side="left", padx=5)

        # --- BUTON ACȚIUNE ---
        self.continue_button = ctk.CTkButton(
            self.main_container, 
            text="INIȚIALIZEAZĂ DOSAR", 
            command=self.process_and_open_interface, 
            height=45,
            font=ctk.CTkFont(weight="bold")
        )
        self.continue_button.pack(fill="x", padx=5, pady=(15, 5))

    def create_label(self, text):
        """Metodă utilitară pentru etichete."""
        lbl = ctk.CTkLabel(self.scroll_frame, text=text, font=ctk.CTkFont(size=13, weight="bold"))
        lbl.pack(anchor="w", padx=15, pady=(5, 2))

    def process_and_open_interface(self):
        """Validează datele și deschide interfața principală de lucru."""
        
        # Colectare date
        data_accident = {
            "agent": self.agent_combobox.get(),
            "data": self.data_entry.get(),
            "ora": self.ora_entry.get(),
            "numar_lucrare": self.lucrare_entry.get(),
            "locul": self.locul_entry.get(),
            "num_vehicule": self.vehicule_entry.get(),
            "num_victime": self.victime_entry.get(),
            "autor_necunoscut": self.an_var.get()
        }

        # Validări
        if not data_accident["numar_lucrare"] or not data_accident["locul"]:
            messagebox.showwarning("Atenție", "Vă rugăm să completați numărul lucrării și locul accidentului.")
            return

        try:
            v_count = int(data_accident["num_vehicule"])
            vic_count = int(data_accident["num_victime"])
            if v_count < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Eroare", "Numărul de vehicule și victime trebuie să fie valori numerice valide (minim 1 vehicul).")
            return

        # Verificăm dacă o fereastră de lucru este deja deschisă
        if self.new_window is None or not self.new_window.winfo_exists():
            # Închidem această fereastră de inițializare
            self.withdraw()
            
            # Deschidem fereastra mare de gestionare a accidentului
            self.new_window = BaseAccidentWindow(master=self.master, data=data_accident)
            
            # Aplicăm patch-urile pe fereastra nouă prin controller-ul principal
            if hasattr(self.master, 'apply_global_patches'):
                self.master.apply_global_patches(self.new_window)
            
            # Distrugem definitiv această fereastră de input primar
            self.destroy()
        else:
            self.new_window.focus()