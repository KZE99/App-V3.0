# -*- coding: utf-8 -*-
"""
Modul pentru widget-ul reutilizabil care afișează și permite
editarea detaliilor unei singure victime (Versiune CustomTkinter - Declarație Colapsabilă).
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

    def _update_var_from_text(self, text_widget, string_var):
        """Actualizează StringVar-ul asociat cu conținutul din CTkTextbox."""
        try:
            current_var_value = string_var.get()
            new_widget_value = text_widget.get("0.0", "end")
            if new_widget_value.endswith('\n'):
                new_widget_value = new_widget_value[:-1]
            if current_var_value != new_widget_value:
                string_var.set(new_widget_value)
        except Exception as e:
            print(f"Eroare în _update_var_from_text: {e}")

    def __init__(self, parent, victim_number, remedy_func):
        super().__init__(parent, border_width=1, corner_radius=10)
        self.remedy_func = remedy_func # Funcția de corectare a diacriticelor
        self.victim_number = victim_number

        # Configurarea grilei interne
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(5, weight=1)

        # Crearea variabilelor Tkinter cu chei specifice pentru template-ul docx
        # ATENȚIE: Key-urile trebuie să corespundă EXACT cu cele din codul utilizatorului
        self.vars = {
            f'nume_victimax{victim_number}': tk.StringVar(),
            f'cnp_victimax{victim_number}': tk.StringVar(),
            f'adresa_victimax{victim_number}': tk.StringVar(),
            f'cetatenie_victimax{victim_number}': tk.StringVar(),
            f'tel_victimax{victim_number}': tk.StringVar(),
            f'calitate_victimax{victim_number}': tk.StringVar(value='Pasager auto'),
            f'diagnostic_victimax{victim_number}': tk.StringVar(),
            f'radio_prezent_cfl_group{victim_number}': tk.StringVar(value='NU'), # Default NU
            f'nota_vinovatie_victimax{victim_number}': tk.IntVar(value=0),
            f'articol_victimax{victim_number}': tk.StringVar(),
            f'declaratie_victimax{victim_number}': tk.StringVar()
        }

        # --- Titlu ---
        title_label = ctk.CTkLabel(self, text=f" VICTIMA NR. {victim_number} ", font=ctk.CTkFont(weight="bold"))
        title_label.grid(row=0, column=0, columnspan=6, pady=(5, 10), padx=10, sticky="ew")

        # --- Rând 1: Nume, CNP, Domiciliu Label ---
        ctk.CTkLabel(self, text="Nume, prenume:").grid(row=1, column=0, padx=(10,2), pady=2, sticky="w")
        entry_nume = ctk.CTkEntry(self, width=230, textvariable=self.vars[f'nume_victimax{victim_number}'])
        entry_nume.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        entry_nume.bind("<KeyPress>", self.remedy_func)

        ctk.CTkLabel(self, text="CNP:").grid(row=1, column=2, padx=(10,2), pady=2, sticky="w")
        entry_cnp = ctk.CTkEntry(self, width=140, textvariable=self.vars[f'cnp_victimax{victim_number}'])
        entry_cnp.grid(row=1, column=3, padx=2, pady=2, sticky="ew")

        ctk.CTkLabel(self, text="cu domiciliul/ sediul în:").grid(row=1, column=4, padx=(10,0), pady=2, sticky="w")

        # --- Rând 2: Adresa, Cetățenie ---
        entry_adresa = ctk.CTkEntry(self, placeholder_text="Adresa...", textvariable=self.vars[f'adresa_victimax{victim_number}'])
        entry_adresa.grid(row=2, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
        entry_adresa.bind("<KeyPress>", self.remedy_func)

        ctk.CTkLabel(self, text="Cetățenie:").grid(row=2, column=4, padx=(10,2), pady=2, sticky="w")
        entry_cetatenie = ctk.CTkEntry(self, width=140, textvariable=self.vars[f'cetatenie_victimax{victim_number}'])
        entry_cetatenie.grid(row=2, column=5, padx=(0,10), pady=2, sticky="ew")
        entry_cetatenie.bind("<KeyPress>", self.remedy_func)

        # --- Rând 3: Telefon, Calitate ---
        ctk.CTkLabel(self, text="Telefon:").grid(row=3, column=0, padx=(10,2), pady=2, sticky="w")
        entry_tel = ctk.CTkEntry(self, width=150, textvariable=self.vars[f'tel_victimax{victim_number}'])
        entry_tel.grid(row=3, column=1, padx=2, pady=2, sticky="w")

        ctk.CTkLabel(self, text="în calitate de:").grid(row=3, column=2, padx=(10,2), pady=2, sticky="w")
        combo_calitate = ctk.CTkComboBox(self, width=200, state="readonly",
                                         variable=self.vars[f'calitate_victimax{victim_number}'],
                                         values=['Pasager auto', 'Pieton', 'Conducător auto',
                                                 'Conducător bicicletă', 'Conducător trotinetă electrică'])
        combo_calitate.grid(row=3, column=3, padx=2, pady=2, sticky="w")

        # --- Rând 4: Diagnostic și Prezent CFL ---
        ctk.CTkLabel(self, text="Diagnostic:").grid(row=4, column=0, padx=(10,2), pady=2, sticky="nw")

        # Textbox Diagnostic
        textbox_diagnostic = ctk.CTkTextbox(self, height=100, width=300, wrap=tk.WORD)
        textbox_diagnostic.grid(row=4, column=1, columnspan=3, padx=2, pady=2, sticky="nsew")
        textbox_diagnostic.bind("<KeyPress>", self.remedy_func)

        # Init value if exists (usually empty on new)
        diag_var = self.vars[f'diagnostic_victimax{victim_number}']
        if diag_var.get():
            textbox_diagnostic.insert("1.0", diag_var.get())

        # Bind FocusOut to update var
        textbox_diagnostic.bind("<FocusOut>", lambda event, w=textbox_diagnostic, v=diag_var: self._update_var_from_text(w, v))

        # Prezent CFL
        frame_prezent = ctk.CTkFrame(self, fg_color="transparent")
        frame_prezent.grid(row=4, column=4, columnspan=2, padx=10, pady=2, sticky="nw")

        ctk.CTkLabel(frame_prezent, text="PREZENT LA FAȚA LOCULUI:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        radio_var = self.vars[f'radio_prezent_cfl_group{victim_number}']
        ctk.CTkRadioButton(frame_prezent, text="DA", value="DA", variable=radio_var).pack(side=tk.LEFT, anchor="w", padx=(0, 10), pady=5)
        ctk.CTkRadioButton(frame_prezent, text="NU", value="NU", variable=radio_var).pack(side=tk.LEFT, anchor="w", pady=5)

        # --- Rând 5: Notă Vinovăție ---
        chk_nota = ctk.CTkCheckBox(self, text="Notă vinovăție",
                                   variable=self.vars[f'nota_vinovatie_victimax{victim_number}'],
                                   onvalue=1, offvalue=0)
        chk_nota.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self, text="Articol:").grid(row=5, column=2, padx=(10,2), pady=10, sticky="w")
        entry_articol = ctk.CTkEntry(self, width=150, textvariable=self.vars[f'articol_victimax{victim_number}'])
        entry_articol.grid(row=5, column=3, padx=2, pady=10, sticky="w")

        # --- Rând 6 & 7: Declarație (gestionată dinamic) ---
        self.label_declaratie = ctk.CTkLabel(self, text="Declaratie victimă - dacă este prezent la CFL:", font=ctk.CTkFont(weight="bold"))

        self.textbox_declaratie = ctk.CTkTextbox(self, height=80, wrap=tk.WORD)
        self.textbox_declaratie.bind("<KeyPress>", self.remedy_func)

        decl_var = self.vars[f'declaratie_victimax{victim_number}']
        if decl_var.get():
            self.textbox_declaratie.insert("1.0", decl_var.get())

        self.textbox_declaratie.bind("<FocusOut>", lambda event, w=self.textbox_declaratie, v=decl_var: self._update_var_from_text(w, v))

        # Setup Toggle Logic
        radio_var.trace_add("write", self.toggle_declaratie_visibility)
        self.toggle_declaratie_visibility()

    def toggle_declaratie_visibility(self, *args):
        """Afișează sau ascunde câmpul de declarație."""
        # Key specific pentru toggle
        radio_key = f'radio_prezent_cfl_group{self.victim_number}'

        if self.vars[radio_key].get() == "DA":
            self.label_declaratie.grid(row=6, column=0, columnspan=6, padx=10, pady=(10, 2), sticky="w")
            self.textbox_declaratie.grid(row=7, column=0, columnspan=6, padx=10, pady=(0,10), sticky="ew")
            self.rowconfigure(7, weight=1)
        else:
            self.label_declaratie.grid_remove()
            self.textbox_declaratie.grid_remove()
            self.rowconfigure(7, weight=0)
            # Opțional: Golește declarația dacă e ascunsă? Userul nu a specificat, dar codul anterior golea.
            # Codul nou al userului NU golea explicit în snippet, doar făcea hide.
            # Vom păstra comportamentul de a NU șterge automat ca să nu piardă date accidental la toggle rapid.
