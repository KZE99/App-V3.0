import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog, messagebox

# Importăm componentele modulare și utilitarele
from src.accident_rutier.interfaces.victim_frame import VictimFrame
from src.accident_rutier.interfaces.vehicle_tabs import VehicleTabs
from src.utils.doc_generator import DocGenerator
from src.utils.data_manager import save_excel_backup

class BaseAccidentWindow(ctk.CTkToplevel):
    """
    Interfața principală de gestionare a unui accident rutier.
    Organizează datele în tab-uri și oferă instrumente de export/backup.
    """
    def __init__(self, master, data):
        super().__init__(master)
        self.master = master
        self.initial_data = data

        # Configurare fereastră (dimensiuni generoase pentru fluxul de lucru)
        self.title(f"Dosar Lucrare: {self.initial_data.get('numar_lucrare', 'N/A')}")
        self.geometry("1300x850")
        
        # Comportament modal pentru a păstra focusul pe dosarul curent
        self.transient(master)
        self.grab_set()
        
        # Variabile locale pentru datele de bază
        self.agent_var = ctk.StringVar(value=self.initial_data.get('agent', ''))
        self.data_var = ctk.StringVar(value=self.initial_data.get('data', ''))
        self.ora_var = ctk.StringVar(value=self.initial_data.get('ora', ''))
        self.locul_var = ctk.StringVar(value=self.initial_data.get('locul', ''))

        self.numar_victime = 0
        self.victime_frames = [] 
        self.vehicle_tabs_manager = None

        # --- GRID LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Zona stângă: Tabview pentru date
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 5), pady=15)

        # Zona dreaptă: Panou Info și Acțiuni
        self.right_frame = ctk.CTkFrame(self, width=300, corner_radius=15)
        self.right_frame.grid(row=0, column=1, sticky="ns", padx=(5, 15), pady=15)
        self.right_frame.pack_propagate(False)

        self.creeaza_taburi()
        self.creeaza_panou_lateral()
        self.actualizeaza_context_actiuni()

    def creeaza_taburi(self):
        """Inițializează sistemul de tab-uri."""
        self.tabview = ctk.CTkTabview(self.left_frame, command=self.actualizeaza_context_actiuni)
        self.tabview.pack(fill="both", expand=True)

        self.tabview.add("Date Principale")
        self.tabview.add("Vehicule Implicate")
        self.tabview.add("Victime")
        self.tabview.add("CFL / Telex")
        self.tabview.add("Documente / Export")

        self.setup_tab_principal(self.tabview.tab("Date Principale"))
        self.setup_tab_vehicule(self.tabview.tab("Vehicule Implicate"))
        self.setup_tab_victime(self.tabview.tab("Victime"))
        self.setup_tab_documente(self.tabview.tab("Documente / Export"))

    def setup_tab_principal(self, tab):
        """Tab pentru revizuirea datelor inițiale ale accidentului."""
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll, text="Informații de Identificare Eveniment", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Câmpuri de editare rapidă
        fields = [
            ("Agent Constatator:", self.agent_var),
            ("Data Eveniment:", self.data_var),
            ("Ora Eveniment:", self.ora_var),
            ("Locul Accidentului:", self.locul_var)
        ]

        for label_text, var in fields:
            ctk.CTkLabel(scroll, text=label_text, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10)
            entry = ctk.CTkEntry(scroll, textvariable=var, width=500)
            entry.pack(fill="x", padx=10, pady=(0, 15))

    def setup_tab_vehicule(self, tab):
        """Integrează managerul complex de vehicule."""
        self.vehicle_tabs_manager = VehicleTabs(
            master=tab,
            remedy_func=self.master.on_key_press_remedy if hasattr(self.master, 'on_key_press_remedy') else None,
            initial_data=self.initial_data
        )
        self.vehicle_tabs_manager.pack(fill="both", expand=True)

    def setup_tab_victime(self, tab):
        """Tab pentru gestionarea listei de victime."""
        self.victime_scroll = ctk.CTkScrollableFrame(tab, label_text="Lista Persoanelor Vătămate / Decedate")
        self.victime_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        num_initial = int(self.initial_data.get('num_victime', 0))
        for _ in range(num_initial):
            self.adauga_victima()

    def adauga_victima(self):
        """Metodă pentru adăugarea dinamică a unui nou frame de victimă."""
        self.numar_victime += 1
        remedy = self.master.on_key_press_remedy if hasattr(self.master, 'on_key_press_remedy') else None
        
        frame_vic = VictimFrame(self.victime_scroll, self.numar_victime, remedy)
        frame_vic.pack(fill="x", padx=10, pady=10)
        self.victime_frames.append(frame_vic)

    def setup_tab_documente(self, tab):
        """Tab dedicat acțiunilor de finalizare și export."""
        ctk.CTkLabel(tab, text="Centralizator Documente", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        frame_btns = ctk.CTkFrame(tab, fg_color="transparent")
        frame_btns.pack(pady=10)

        ctk.CTkButton(
            frame_btns, 
            text="Generează Proces-Verbal CFL", 
            width=250, 
            height=40,
            command=self.export_to_word
        ).pack(pady=10)

        ctk.CTkButton(
            frame_btns, 
            text="Generează Anexa 2", 
            width=250, 
            height=40,
            fg_color="gray40"
        ).pack(pady=10)

    def creeaza_panou_lateral(self):
        """Construiește panoul din dreapta cu info și acțiuni globale."""
        # Info Fixe
        info_box = ctk.CTkFrame(self.right_frame, fg_color=("gray85", "gray17"))
        info_box.pack(fill="x", padx=15, pady=20)
        
        ctk.CTkLabel(info_box, text="STATUS DOSAR", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=5)
        
        self.lbl_status = ctk.CTkLabel(
            info_box, 
            text=f"Lucrare: {self.initial_data.get('numar_lucrare', '---')}",
            text_color="orange"
        )
        self.lbl_status.pack(pady=5)

        # Secțiune Acțiuni Contextuale
        ctk.CTkLabel(self.right_frame, text="ACȚIUNI DISPONIBILE", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        self.context_actions_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.context_actions_frame.pack(fill="x", padx=15, pady=5)

        # Acțiuni Globale (Always visible)
        spacer = ctk.CTkLabel(self.right_frame, text="")
        spacer.pack(expand=True)

        global_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        global_frame.pack(fill="x", padx=15, pady=20)

        ctk.CTkButton(
            global_frame, 
            text="SALVEAZĂ BACKUP EXCEL", 
            fg_color="#2ecc71", 
            hover_color="#27ae60",
            command=self.execute_excel_backup
        ).pack(fill="x", pady=5)

        ctk.CTkButton(
            global_frame, 
            text="ÎNCHIDE DOSAR", 
            fg_color="#e74c3c", 
            hover_color="#c0392b",
            command=self.destroy
        ).pack(fill="x", pady=5)

    def actualizeaza_context_actiuni(self):
        """Schimbă butoanele din panoul lateral în funcție de tab-ul activ."""
        for widget in self.context_actions_frame.winfo_children():
            widget.destroy()

        tab = self.tabview.get()
        if tab == "Vehicule Implicate":
            ctk.CTkButton(
                self.context_actions_frame, 
                text="+ Adaugă Vehicul", 
                command=self.vehicle_tabs_manager.add_new_auto_tab
            ).pack(fill="x", pady=5)
        elif tab == "Victime":
            ctk.CTkButton(
                self.context_actions_frame, 
                text="+ Adaugă Victimă", 
                command=self.adauga_victima
            ).pack(fill="x", pady=5)

    def get_all_data(self):
        """Colectează absolut toate datele din toate sub-componentele."""
        data = {
            'numar_lucrare': self.initial_data.get('numar_lucrare', ''),
            'agent': self.agent_var.get(),
            'data': self.data_var.get(),
            'ora': self.ora_var.get(),
            'locul': self.locul_var.get(),
            'autor_necunoscut': self.initial_data.get('autor_necunoscut', 'Nu')
        }
        
        # Date vehicule
        if self.vehicle_tabs_manager:
            data.update(self.vehicle_tabs_manager.get_data())
        
        # Date victime
        data['victime'] = [f.get_data() for f in self.victime_frames]
        
        return data

    def export_to_word(self):
        """Declanșează procesul de generare document Word."""
        full_context = self.get_all_data()
        
        output_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx")],
            initialfile=f"PV_CFL_{full_context['numar_lucrare']}.docx"
        )
        
        if output_path:
            success, msg = DocGenerator.generate_docx(full_context, "template_accident.docx", output_path)
            if success:
                messagebox.showinfo("Succes", msg)
            else:
                messagebox.showerror("Eroare", msg)

    def execute_excel_backup(self):
        """Realizează salvarea stării curente în folderul de Backup."""
        data = self.get_all_data()
        success, path = save_excel_backup(data)
        if success:
            messagebox.showinfo("Backup Realizat", f"Datele au fost salvate în:\n{path}")
        else:
            messagebox.showerror("Eroare Backup", f"Nu s-a putut salva backup-ul:\n{path}")