# -*- coding: utf-8 -*-
"""
Modul pentru widget-ul reutilizabil care afișează și permite
editarea detaliilor unei singure victime.
"""

import tkinter as tk
import customtkinter as ctk

class VictimFrame(ctk.CTkFrame):
    """
    Un widget care afișează și permite editarea detaliilor
    unei singure victime, cu secțiune de declarație colapsabilă.
    """
    def get_data(self):
        """Colectează toate datele din variabilele UI ale victimei."""
        data = {}
        for key, var in self.vars.items():
            data[key] = var.get()
        return data
    
    def __init__(self, parent, victim_number, remedy_func):
        super().__init__(parent, border_width=1, corner_radius=10)
        self.remedy_func = remedy_func # Funcția de corectare a diacriticelor

        # Configurarea grilei interne
        self.columnconfigure((1, 3, 5), weight=1)

        # Crearea variabilelor Tkinter cu chei specifice pentru template-ul docx
        self.vars = {
            f'nume_v{victim_number}': tk.StringVar(),
            f'cnp_v{victim_number}': tk.StringVar(),
            f'adresa_v{victim_number}': tk.StringVar(),
            f'cetatenie_v{victim_number}': tk.StringVar(),
            f'tel_v{victim_number}': tk.StringVar(),
            f'calitate_v{victim_number}': tk.StringVar(value='Pasager auto'),
            f'diagnostic_v{victim_number}': tk.StringVar(),
            f'prezent_cfl_v{victim_number}': tk.StringVar(value='NU'),
            f'nota_vinovatie_v{victim_number}': tk.IntVar(value=0),
            f'articol_v{victim_number}': tk.StringVar(),
            f'declaratie_v{victim_number}': tk.StringVar()
        }

        # --- Titlu ---
        title_label = ctk.CTkLabel(self, text=f" VICTIMA NR. {victim_number} ", font=ctk.CTkFont(weight="bold"))
        title_label.grid(row=0, column=0, columnspan=6, pady=(5, 10), padx=10, sticky="ew")

        # --- Interfața Grafică ---
        ctk.CTkLabel(self, text="Nume, prenume:").grid(row=1, column=0, padx=(10,2), pady=2, sticky="w")
        entry_nume = ctk.CTkEntry(self, textvariable=self.vars[f'nume_v{victim_number}'])
        entry_nume.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        entry_nume.bind("<KeyPress>", self.remedy_func)

        ctk.CTkLabel(self, text="CNP:").grid(row=1, column=2, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(self, textvariable=self.vars[f'cnp_v{victim_number}']).grid(row=1, column=3, padx=2, pady=2, sticky="ew")
        ctk.CTkLabel(self, text="cu domiciliul în:").grid(row=1, column=4, padx=(10,0), pady=2, sticky="w")

        entry_adresa = ctk.CTkEntry(self, placeholder_text="Adresa...", textvariable=self.vars[f'adresa_v{victim_number}'])
        entry_adresa.grid(row=2, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
        entry_adresa.bind("<KeyPress>", self.remedy_func)

        ctk.CTkLabel(self, text="Cetățenie:").grid(row=2, column=4, padx=(10,2), pady=2, sticky="w")
        entry_cetatenie = ctk.CTkEntry(self, textvariable=self.vars[f'cetatenie_v{victim_number}'])
        entry_cetatenie.grid(row=2, column=5, padx=(0,10), pady=2, sticky="ew")
        entry_cetatenie.bind("<KeyPress>", self.remedy_func)

        ctk.CTkLabel(self, text="Telefon:").grid(row=3, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(self, textvariable=self.vars[f'tel_v{victim_number}']).grid(row=3, column=1, padx=2, pady=2, sticky="w")

        ctk.CTkLabel(self, text="în calitate de:").grid(row=3, column=2, padx=(10,2), pady=2, sticky="w")
        ctk.CTkComboBox(self, state="readonly", variable=self.vars[f'calitate_v{victim_number}'],
                        values=['Pasager auto', 'Pieton', 'Conducător auto', 'Conducător bicicletă', 'Conducător trotinetă electrică']
                        ).grid(row=3, column=3, padx=2, pady=2, sticky="w")

        ctk.CTkLabel(self, text="Diagnostic:").grid(row=4, column=0, padx=(10,2), pady=2, sticky="nw")
        textbox_diagnostic = ctk.CTkTextbox(self, height=100, wrap=tk.WORD)
        textbox_diagnostic.grid(row=4, column=1, columnspan=3, padx=2, pady=2, sticky="nsew")
        textbox_diagnostic.bind("<KeyPress>", self.remedy_func)
        textbox_diagnostic.bind("<FocusOut>", lambda e, v=f'diagnostic_v{victim_number}', w=textbox_diagnostic: self.vars[v].set(w.get("1.0", "end-1c")))

        frame_prezent = ctk.CTkFrame(self, fg_color="transparent")
        frame_prezent.grid(row=4, column=4, columnspan=2, padx=10, pady=2, sticky="nw")
        ctk.CTkLabel(frame_prezent, text="PREZENT LA FAȚA LOCULUI:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkRadioButton(frame_prezent, text="DA", value="DA", variable=self.vars[f'prezent_cfl_v{victim_number}']).pack(side=tk.LEFT, anchor="w", padx=(0, 10), pady=5)
        ctk.CTkRadioButton(frame_prezent, text="NU", value="NU", variable=self.vars[f'prezent_cfl_v{victim_number}']).pack(side=tk.LEFT, anchor="w", pady=5)

        ctk.CTkCheckBox(self, text="Notă vinovăție", variable=self.vars[f'nota_vinovatie_v{victim_number}'], onvalue=1, offvalue=0).grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(self, text="Articol:").grid(row=5, column=2, padx=(10,2), pady=10, sticky="w")
        ctk.CTkEntry(self, textvariable=self.vars[f'articol_v{victim_number}']).grid(row=5, column=3, padx=2, pady=10, sticky="w")

        self.label_declaratie = ctk.CTkLabel(self, text="Declaratie victimă:", font=ctk.CTkFont(weight="bold"))
        self.textbox_declaratie = ctk.CTkTextbox(self, height=80, wrap=tk.WORD)
        self.textbox_declaratie.bind("<KeyPress>", self.remedy_func)
        self.textbox_declaratie.bind("<FocusOut>", lambda e, v=f'declaratie_v{victim_number}', w=self.textbox_declaratie: self.vars[v].set(w.get("1.0", "end-1c")))

        self.vars[f'prezent_cfl_v{victim_number}'].trace_add("write", self.toggle_declaratie_visibility)
        self.toggle_declaratie_visibility()

    def toggle_declaratie_visibility(self, *args):
        """Afișează sau ascunde câmpul de declarație."""
        if self.vars[list(self.vars.keys())[7]].get() == "DA": # Verifică 'prezent_cfl_vX'
            self.label_declaratie.grid(row=6, column=0, columnspan=6, padx=10, pady=(10, 2), sticky="w")
            self.textbox_declaratie.grid(row=7, column=0, columnspan=6, padx=10, pady=(0,10), sticky="ew")
        else:
            self.label_declaratie.grid_remove()
            self.textbox_declaratie.grid_remove()
            self.vars[list(self.vars.keys())[10]].set("") # Golește 'declaratie_vX'
