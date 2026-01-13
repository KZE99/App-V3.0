# -*- coding: utf-8 -*-
"""
Modul pentru gestionarea tab-ului principal "Vehicule Implicate",
incluzând crearea dinamică a sub-tab-urilor pentru fiecare vehicul.
"""
import customtkinter as ctk
import tkinter as tk
import sys
import traceback

class VehicleTabs(ctk.CTkFrame):
    """
    Clasă container care gestionează sub-tab-uri pentru vehicule.
    """
    VAR_PREFIX = "auto_"

    # --- COREECȚIE DIACRITICE ---
    REMEDIED_CHARS = {
        ord(c): c for c in 'șțâîăȘȚÂÎĂ'
    }

    DATA_KEYS_PER_AUTO = [
        "tip_autox", "marca_autox", "nr_autox", "VIN_autox", "culoare_autox",
        "proprietar_autox", "sediu_autox", "utilizator_autox", "sediu_util_autox",
        "tara_autox", "an_fabricatie_autox", "itp_autox", "rca_autox",
        "serie_rca_autox", "inceput_rca_autox", "sfarsit_rca_autox",
        "bifa_vinovat_autox", "bifa_victima_autox",
        "nume_sofer_autox", "cnp_sofer_autox", "adresa_sofer_autox",
        "cetatenie_sofer_autox", "nrpc_sofer_autox", "catpc_sofer_autox",
        "vechime_pc_sofer_autox",
        "atestat_sofer_autox", "data_atestat_sofer_autox", "angajat_sofer_autox",
        "functie_sofer_autox", "tel_sofer_autox", "calitate_sofer_autox",
        "diagnostic_sofer_autox",
        "nota_vinovatie_sofer_autox", "articol_sofer_autox",
        "raport_retinere_sofer_autox", "bifa_pc_sofer_autox", "amenda_retinere_autox",
        "serie_pvcc_autox", "raport_retinere_itp_autox", "raport_retinere_rca_autox",
        "art_334_1_autox", "art_336_1_autox", "art_334_2_autox", "art_336_1ind1_autox",
        "art_334_3_autox", "art_336_2_autox", "art_334_4_autox", "art_337_autox",
        "art_335_1_autox", "art_338_1_autox", "art_335_2_autox", "art_338_2_autox",
        "etilo_autox", "serie_etilo_autox", "pozitie_etilo_autox",
        "rezultat_etilo_autox", "drugtest_autox", "serie_drugtest_autox",
        "pozitie_drugtest_autox", "rezultat_drugtest_autox",
        "droguri_drugtest_autox", "inml_autox", "sigiliu_inml_autox",
        "text_declaratie_sofer_autox", "text_pozitie_autox", "text_avarii_autox",
        "condus_stradax", "condus_directiax", "condus_catrex",
        # Chei noi pentru măsurători
        "masuratori_visiblex",
        "masuratori_strada_vehiculx", "masuratori_orientare_vehiculx",
        "masuratori_privind_dinsprex", "masuratori_privind_catrex",
        "masuratori_orientare_axx",
        "masuratori_dist_inaintex",
        "masuratori_dist_stg_fatax",
        "masuratori_dist_dr_fatax",
        "masuratori_dist_stg_spatex",
        "masuratori_dist_dr_spatex",
        "masuratori_dist_inapoix",
        "masuratori_dist_lateral_stgx",
        "masuratori_dist_lateral_drx",
        # Sfârșit chei noi
        "examinare_vehicul_visiblex", "utilizator_visiblex", "sofer_extra_visiblex", "drugtest_probe_visiblex",
        "examinare_anvelope_tipx", "examinare_anvelope_uzurax", "examinare_iluminare_functionalx",
        "examinare_stergatoare_existax", "examinare_stergatoare_functionalx",
        "examinare_portiere_starex", "examinare_portiere_asigurarex", "examinare_portiere_mecanismx",
        "examinare_maneta_vitezex", "examinare_frana_manax", "examinare_airbagurix",
        "examinare_ac_kilometrajx", "examinare_turometrux", "examinare_km_indicatix",
        "examinare_pedala_franax", "examinare_sistem_franarex",
        "examinare_incarcatura_persoanex", "examinare_incarcatura_tipx", "examinare_incarcatura_detaliix",
        "examinare_sig_centurix", "examinare_sig_scaun_copilx", "examinare_sig_reflectorizantex",
        "examinare_sig_cascax", "examinare_sig_geacax", "examinare_sig_pantalonix", "examinare_sig_altelex"
    ]


    def __init__(self, master, remedy_func, initial_data=None):
        super().__init__(master, fg_color="transparent")
        self.initial_data = initial_data if initial_data is not None else {}
        self.all_vehicle_data_vars = []
        self.data_vars = {}
        self._text_widget_updating = {}
        self.auto_number_counter = 0

        self.vehicle_tabview = ctk.CTkTabview(self)
        self.vehicle_tabview.pack(fill="both", expand=True)

        num_initial_vehicule = int(self.initial_data.get('num_vehicule', 0))
        if num_initial_vehicule > 0:
            for i in range(1, num_initial_vehicule + 1):
                self.add_new_auto_tab(auto_index=i)
        else:
            self.add_new_auto_tab()
            
        self._create_context_menu()

    def _create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.focus_get().event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.focus_get().event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=lambda: self.focus_get().event_generate("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=lambda: self.focus_get().event_generate("<<SelectAll>>"))

    def _show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def on_key_press_remedy(self, event):
        char_remedy = self.REMEDIED_CHARS.get(event.keysym_num)
        if char_remedy:
            event.widget.insert('insert', char_remedy)
            return 'break'

    def add_new_auto_tab(self, auto_index=None):
        self.auto_number_counter += 1
        auto_number = auto_index if auto_index is not None else self.auto_number_counter
        
        tab_name = f"Vehicul {auto_number}"
        try:
            if tab_name in self.vehicle_tabview._tab_dict:
                self.vehicle_tabview.set(tab_name)
                return

            new_tab = self.vehicle_tabview.add(tab_name)
            
            scroll_frame = ctk.CTkScrollableFrame(new_tab, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            vehicle_vars = {}
            for key_template in self.DATA_KEYS_PER_AUTO:
                base_key = key_template[:-1] if key_template.endswith('x') else key_template
                data_key = f"{base_key}{auto_number}"
                var_key = f"{self.VAR_PREFIX}{auto_number}_{base_key}"

                if key_template.startswith("bifa_") or key_template.startswith("art_") or "visible" in key_template or "sig" in key_template or key_template == "masuratori_orientare_axx":
                    var = tk.IntVar(value=self.initial_data.get(data_key, 0))
                else:
                    var = tk.StringVar(value=str(self.initial_data.get(data_key, "")))
                
                self.data_vars[var_key] = var
                vehicle_vars[data_key] = var

            self._create_vehicle_ui(scroll_frame, auto_number, vehicle_vars)
            self.all_vehicle_data_vars.append(vehicle_vars)
            self.vehicle_tabview.set(tab_name)

        except Exception as ex:
            print(f"Eroare Adăugare Tab: Nu s-a putut adăuga tab-ul '{tab_name}': {ex}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return

    def _update_var_from_text(self, text_widget, string_var):
        widget_id = str(text_widget)
        if self._text_widget_updating.get(widget_id): return
        try:
            self._text_widget_updating[widget_id] = True
            current_var_value = string_var.get()
            new_widget_value = text_widget.get("1.0", "end-1c")
            if current_var_value != new_widget_value:
                string_var.set(new_widget_value)
        except Exception as e:
            print(f"Eroare în _update_var_from_text pentru {text_widget}: {e}")
        finally:
            self._text_widget_updating[str(text_widget)] = False
            
    def _create_vehicle_ui(self, parent_scrollable_frame, auto_number, vehicle_vars):
        # --- Frame Vehicul ---
        frame_vehicul = ctk.CTkFrame(parent_scrollable_frame, border_width=1)
        frame_vehicul.pack(fill="x", padx=5, pady=5, expand=False)
        ctk.CTkLabel(frame_vehicul, text=f"VEHICUL NR. {auto_number}", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 10))
        
        def update_calitate_sofer(selected_tip):
            calitate_map = {
                'Autoturism': 'conducător auto',
                'Autospecială': 'conducător auto',
                'Autobuz': 'conducător autobuz',
                'Tramvai': 'conducător tramvai',
                'Troleibuz': 'conducător troleibuz',
                'Autoutilitară': 'conducător auto',
                'Motocicletă': 'conducător moto',
                'Moped': 'conducător moped',
                'Trotinetă electrică': 'conducător trotinetă electrică',
                'Bicicletă': 'conducător bicicletă',
                'Autorulotă': 'conducător auto',
                'Tractor': 'conducător auto',
                'Cap tractor': 'conducător auto',
                'Tracțiune animală': 'conducător vehicul cu tracțiune animală'
            }
            new_calitate = calitate_map.get(selected_tip, 'conducător auto')
            vehicle_vars[f'calitate_sofer_auto{auto_number}'].set(new_calitate)

        row1 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row1, text="Tip Vehicul:", width=120, anchor="w").pack(side="left")
        combo_tip_veh = ctk.CTkComboBox(row1, width=160, state="readonly", variable=vehicle_vars[f'tip_auto{auto_number}'],
            values=['Autoturism', 'Autospecială', 'Autobuz','Tramvai','Troleibuz','Autoutilitară', 'Motocicletă','Moped','Trotinetă electrică','Bicicletă', 'Autorulotă', 'Tractor', 'Cap tractor', 'Tracțiune animală'],
            command=update_calitate_sofer)
        combo_tip_veh.pack(side="left", padx=(0,10))
        
        ctk.CTkLabel(row1, text="Marca/ Tip:", width=80, anchor="w").pack(side="left")
        entry_marca = ctk.CTkEntry(row1, textvariable=vehicle_vars[f'marca_auto{auto_number}'])
        entry_marca.pack(side="left", expand=True, fill="x")
        entry_marca.bind("<KeyPress>", self.on_key_press_remedy)
        entry_marca.bind("<Button-3>", self._show_context_menu)
        
        row2 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row2, text="Nr. Înmatriculare:", width=120, anchor="w").pack(side="left")
        entry_nr = ctk.CTkEntry(row2, width=160, textvariable=vehicle_vars[f'nr_auto{auto_number}'])
        entry_nr.pack(side="left", padx=(0,10))
        entry_nr.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(row2, text="Serie Șasiu:", width=80, anchor="w").pack(side="left")
        entry_vin = ctk.CTkEntry(row2, textvariable=vehicle_vars[f'VIN_auto{auto_number}'])
        entry_vin.pack(side="left", expand=True, fill="x")
        entry_vin.bind("<Button-3>", self._show_context_menu)
        
        row3 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row3, text="Culoare:", width=120, anchor="w").pack(side="left")
        entry_culoare = ctk.CTkEntry(row3, width=160, textvariable=vehicle_vars[f'culoare_auto{auto_number}'])
        entry_culoare.pack(side="left", padx=(0,10))
        entry_culoare.bind("<KeyPress>", self.on_key_press_remedy)
        entry_culoare.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(row3, text="An fabricație:", width=80, anchor="w").pack(side="left")
        entry_an_fab = ctk.CTkEntry(row3, textvariable=vehicle_vars[f'an_fabricatie_auto{auto_number}'])
        entry_an_fab.pack(side="left", expand=True, fill="x")
        entry_an_fab.bind("<Button-3>", self._show_context_menu)

        row4 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row4.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row4, text="Proprietar:").pack(side="left", anchor="w")
        entry_prop = ctk.CTkEntry(row4, textvariable=vehicle_vars[f'proprietar_auto{auto_number}'])
        entry_prop.pack(side="left", expand=True, fill="x", padx=(5,0))
        entry_prop.bind("<KeyPress>", self.on_key_press_remedy)
        entry_prop.bind("<Button-3>", self._show_context_menu)

        row5 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row5.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row5, text="Domiciliu/Sediu Proprietar:").pack(side="left", anchor="w")
        entry_sediu_prop = ctk.CTkEntry(row5, textvariable=vehicle_vars[f'sediu_auto{auto_number}'])
        entry_sediu_prop.pack(side="left", expand=True, fill="x", padx=(5,0))
        entry_sediu_prop.bind("<KeyPress>", self.on_key_press_remedy)
        entry_sediu_prop.bind("<Button-3>", self._show_context_menu)

        # --- SECȚIUNE UTILIZATOR (COLLAPSIBLE) ---
        utilizator_container = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        utilizator_container.pack(fill="x", padx=5, pady=0)

        utilizator_visible_var = vehicle_vars[f'utilizator_visible{auto_number}']
        frame_utilizator_content = ctk.CTkFrame(utilizator_container)
        
        def toggle_utilizator():
            if utilizator_visible_var.get() == 0:
                frame_utilizator_content.pack(after=btn_toggle_utilizator, fill="x", expand=True, pady=(0,5))
                btn_toggle_utilizator.configure(text="▼ Date utilizator")
                utilizator_visible_var.set(1)
            else:
                frame_utilizator_content.pack_forget()
                btn_toggle_utilizator.configure(text="▶ Date utilizator")
                utilizator_visible_var.set(0)

        btn_toggle_utilizator = ctk.CTkButton(
            utilizator_container, text="▶ Date utilizator", command=toggle_utilizator, anchor="w",
            fg_color="transparent", text_color=(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            hover=False
        )
        btn_toggle_utilizator.pack(fill="x")
        
        ctk.CTkLabel(frame_utilizator_content, text="Utilizator:").pack(anchor="w", padx=10)
        entry_util = ctk.CTkEntry(frame_utilizator_content, textvariable=vehicle_vars[f'utilizator_auto{auto_number}'])
        entry_util.pack(fill="x", padx=10, pady=(0,5))
        entry_util.bind("<KeyPress>", self.on_key_press_remedy)
        entry_util.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(frame_utilizator_content, text="Domiciliu/Sediu Utilizator:").pack(anchor="w", padx=10)
        entry_sediu_util = ctk.CTkEntry(frame_utilizator_content, textvariable=vehicle_vars[f'sediu_util_auto{auto_number}'])
        entry_sediu_util.pack(fill="x", padx=10, pady=(0,5))
        entry_sediu_util.bind("<KeyPress>", self.on_key_press_remedy)
        entry_sediu_util.bind("<Button-3>", self._show_context_menu)
        
        row6 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row6.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row6, text="Țara înmatriculare:", width=120, anchor="w").pack(side="left")
        entry_tara = ctk.CTkEntry(row6, width=160, textvariable=vehicle_vars[f'tara_auto{auto_number}'])
        entry_tara.pack(side="left", padx=(0,10))
        entry_tara.bind("<KeyPress>", self.on_key_press_remedy)
        entry_tara.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(row6, text="ITP valabil până la:", width=120, anchor="w").pack(side="left")
        entry_itp = ctk.CTkEntry(row6, textvariable=vehicle_vars[f'itp_auto{auto_number}'])
        entry_itp.pack(side="left", expand=True, fill="x")
        entry_itp.bind("<Button-3>", self._show_context_menu)

        row7 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row7.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row7, text="Asigurare RCA:").pack(side="left", anchor="w")
        combo_rca = ctk.CTkComboBox(row7, variable=vehicle_vars[f'rca_auto{auto_number}'],
            values=['______________________','GRAWE', 'OMNIASIG','GROUPAMA', 'GENERALI', 'ASIROM','AXERIA IARD','Hellas Direct Insurance LTD Nicosia – Sucursala Bucuresti', 'ALLIANZ ȚIRIAC'])
        combo_rca.pack(side="left", expand=True, fill="x", padx=(5,0))
        
        row8 = ctk.CTkFrame(frame_vehicul, fg_color="transparent")
        row8.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row8, text="Serie RCA:", width=120, anchor="w").pack(side="left")
        entry_serie_rca = ctk.CTkEntry(row8, width=160, textvariable=vehicle_vars[f'serie_rca_auto{auto_number}'])
        entry_serie_rca.pack(side="left", padx=(0,10))
        entry_serie_rca.bind("<Button-3>", self._show_context_menu)

        ctk.CTkLabel(row8, text="Valabilitate:").pack(side="left", anchor="w")
        entry_start_rca = ctk.CTkEntry(row8, placeholder_text="de la", textvariable=vehicle_vars[f'inceput_rca_auto{auto_number}'])
        entry_start_rca.pack(side="left", expand=True, fill="x", padx=(5,2))
        entry_start_rca.bind("<Button-3>", self._show_context_menu)
        entry_end_rca = ctk.CTkEntry(row8, placeholder_text="până la", textvariable=vehicle_vars[f'sfarsit_rca_auto{auto_number}'])
        entry_end_rca.pack(side="left", expand=True, fill="x", padx=(2,0))
        entry_end_rca.bind("<Button-3>", self._show_context_menu)
        
        # --- Frame Vinovăție ---
        frame_vinovatie = ctk.CTkFrame(parent_scrollable_frame, border_width=1)
        frame_vinovatie.pack(fill="x", padx=5, pady=5, expand=False)
        frame_vinovatie.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkCheckBox(frame_vinovatie, text="VINOVAT", variable=vehicle_vars[f'bifa_vinovat_auto{auto_number}']).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkCheckBox(frame_vinovatie, text="VICTIMĂ", variable=vehicle_vars[f'bifa_victima_auto{auto_number}']).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # --- Frame Conducător Auto ---
        frame_sofer = ctk.CTkFrame(parent_scrollable_frame, border_width=1)
        frame_sofer.pack(fill="x", padx=5, pady=5, expand=False)
        frame_sofer.grid_columnconfigure((1, 3), weight=1)
        ctk.CTkLabel(frame_sofer, text=f"Conducător Auto nr. {auto_number}", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=(5, 10), sticky="ew")
        
        r_sof = 1
        ctk.CTkLabel(frame_sofer, text="Nume, prenume:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="w")
        entry_nume_sof = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'nume_sofer_auto{auto_number}'])
        entry_nume_sof.grid(row=r_sof, column=1, padx=2, pady=2, sticky="ew")
        entry_nume_sof.bind("<KeyPress>", self.on_key_press_remedy)
        entry_nume_sof.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(frame_sofer, text="CNP:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'cnp_sofer_auto{auto_number}']).grid(row=r_sof, column=3, padx=(0,10), pady=2, sticky="ew")
        
        r_sof += 1
        ctk.CTkLabel(frame_sofer, text="Adresă domiciliu:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="w")
        entry_adresa_sof = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'adresa_sofer_auto{auto_number}'])
        entry_adresa_sof.grid(row=r_sof, column=1, columnspan=3, padx=(0,10), pady=2, sticky="ew")
        entry_adresa_sof.bind("<KeyPress>", self.on_key_press_remedy)
        entry_adresa_sof.bind("<Button-3>", self._show_context_menu)
        
        r_sof += 1
        ctk.CTkLabel(frame_sofer, text="Cetățenie:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="w")
        entry_cet_sof = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'cetatenie_sofer_auto{auto_number}'])
        entry_cet_sof.grid(row=r_sof, column=1, padx=2, pady=2, sticky="ew")
        entry_cet_sof.bind("<KeyPress>", self.on_key_press_remedy)
        entry_cet_sof.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(frame_sofer, text="Telefon:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'tel_sofer_auto{auto_number}']).grid(row=r_sof, column=3, padx=(0,10), pady=2, sticky="ew")
        
        r_sof += 1
        ctk.CTkLabel(frame_sofer, text="Permis conducere nr.:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'nrpc_sofer_auto{auto_number}']).grid(row=r_sof, column=1, padx=2, pady=2, sticky="ew")
        
        ctk.CTkLabel(frame_sofer, text="Categoriile:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
        entry_catpc = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'catpc_sofer_auto{auto_number}'])
        entry_catpc.grid(row=r_sof, column=3, padx=(0,10), pady=2, sticky="ew")
        entry_catpc.bind("<KeyPress>", self.on_key_press_remedy)
        entry_catpc.bind("<Button-3>", self._show_context_menu)
        
        r_sof += 1
        ctk.CTkLabel(frame_sofer, text="Vechime din anul:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars[f'vechime_pc_sofer_auto{auto_number}']).grid(row=r_sof, column=1, padx=2, pady=2, sticky="ew")

        # --- SECȚIUNE DATE EXTRA ȘOFER (COLLAPSIBLE) ---
        r_sof += 1
        sofer_extra_container = ctk.CTkFrame(frame_sofer, fg_color="transparent")
        sofer_extra_container.grid(row=r_sof, column=0, columnspan=4, sticky="ew", padx=5, pady=0)
        
        sofer_extra_visible_var = vehicle_vars[f'sofer_extra_visible{auto_number}']
        frame_sofer_extra_content = ctk.CTkFrame(sofer_extra_container)
        
        def toggle_sofer_extra():
            if sofer_extra_visible_var.get() == 0:
                frame_sofer_extra_content.pack(after=btn_toggle_sofer_extra, fill="x", expand=True, pady=(0,5))
                btn_toggle_sofer_extra.configure(text="▼ Date extra conducător vehicul")
                sofer_extra_visible_var.set(1)
            else:
                frame_sofer_extra_content.pack_forget()
                btn_toggle_sofer_extra.configure(text="▶ Date extra conducător vehicul")
                sofer_extra_visible_var.set(0)

        btn_toggle_sofer_extra = ctk.CTkButton(
            sofer_extra_container, text="▶ Date extra conducător vehicul", command=toggle_sofer_extra, anchor="w",
            fg_color="transparent", text_color=(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            hover=False
        )
        btn_toggle_sofer_extra.pack(fill="x")
        
        frame_sofer_extra_content.grid_columnconfigure((1, 3), weight=1)
        ctk.CTkLabel(frame_sofer_extra_content, text="Atestat profesional:").grid(row=0, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_sofer_extra_content, textvariable=vehicle_vars[f'atestat_sofer_auto{auto_number}']).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        
        ctk.CTkLabel(frame_sofer_extra_content, text="Data eliberării:").grid(row=0, column=2, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_sofer_extra_content, textvariable=vehicle_vars[f'data_atestat_sofer_auto{auto_number}']).grid(row=0, column=3, padx=(0,10), pady=2, sticky="ew")
        
        ctk.CTkLabel(frame_sofer_extra_content, text="Angajat la:").grid(row=1, column=0, padx=(10,2), pady=2, sticky="w")
        entry_angajat = ctk.CTkEntry(frame_sofer_extra_content, textvariable=vehicle_vars[f'angajat_sofer_auto{auto_number}'])
        entry_angajat.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        entry_angajat.bind("<KeyPress>", self.on_key_press_remedy)
        entry_angajat.bind("<Button-3>", self._show_context_menu)
        
        ctk.CTkLabel(frame_sofer_extra_content, text="Funcția:").grid(row=1, column=2, padx=(10,2), pady=2, sticky="w")
        entry_functie = ctk.CTkEntry(frame_sofer_extra_content, textvariable=vehicle_vars[f'functie_sofer_auto{auto_number}'])
        entry_functie.grid(row=1, column=3, padx=(0,10), pady=2, sticky="ew")
        entry_functie.bind("<KeyPress>", self.on_key_press_remedy)
        entry_functie.bind("<Button-3>", self._show_context_menu)
        
        r_sof += 1
        ctk.CTkLabel(frame_sofer, text="Calitate:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkLabel(frame_sofer, textvariable=vehicle_vars[f'calitate_sofer_auto{auto_number}']).grid(row=r_sof, column=1, padx=2, pady=2, sticky="w")
        
        r_sof += 1
        ctk.CTkLabel(frame_sofer, text="Diagnostic:").grid(row=r_sof, column=0, padx=(10,2), pady=2, sticky="nw")
        textbox_diag_sof = ctk.CTkTextbox(frame_sofer, height=60, wrap=tk.WORD)
        textbox_diag_sof.grid(row=r_sof, column=1, columnspan=3, padx=(0,10), pady=(2,10), sticky="ew")
        textbox_diag_sof.bind("<KeyPress>", self.on_key_press_remedy)
        textbox_diag_sof.bind("<Button-3>", self._show_context_menu)
        diag_sof_var = vehicle_vars[f'diagnostic_sofer_auto{auto_number}']
        textbox_diag_sof.insert("1.0", diag_sof_var.get())
        textbox_diag_sof.bind("<FocusOut>", lambda event, w=textbox_diag_sof, v=diag_sof_var: self._update_var_from_text(w, v))

        # --- Frame Documente și Articole CP (Container) ---
        frame_docs_cp_container = ctk.CTkFrame(parent_scrollable_frame, fg_color="transparent")
        frame_docs_cp_container.pack(fill="x", padx=5, pady=5, expand=False)
        frame_docs_cp_container.grid_columnconfigure(0, weight=1)
        frame_docs_cp_container.grid_columnconfigure(1, weight=1, minsize=250)

        # Frame Întocmire Documente
        frame_docs = ctk.CTkFrame(frame_docs_cp_container, border_width=1)
        frame_docs.grid(row=0, column=0, padx=(0,5), pady=0, sticky="nsew")
        ctk.CTkLabel(frame_docs, text="Întocmire documente", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(5, 10), sticky="ew")
        
        r_doc = 1
        ctk.CTkCheckBox(frame_docs, text="Notă vinovăție", variable=vehicle_vars[f'nota_vinovatie_sofer_auto{auto_number}']).grid(row=r_doc, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        
        r_doc += 1
        ctk.CTkLabel(frame_docs, text="Articol OUG 195:").grid(row=r_doc, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_docs, textvariable=vehicle_vars[f'articol_sofer_auto{auto_number}']).grid(row=r_doc, column=1, padx=2, pady=2, sticky="ew")
        
        r_doc += 1
        ctk.CTkCheckBox(frame_docs, text="Raport Reținere PC - Accident", variable=vehicle_vars[f'raport_retinere_sofer_auto{auto_number}']).grid(row=r_doc, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        
        r_doc += 1
        ctk.CTkCheckBox(frame_docs, text="A fost reținut PC", variable=vehicle_vars[f'bifa_pc_sofer_auto{auto_number}']).grid(row=r_doc, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        
        r_doc += 1
        ctk.CTkLabel(frame_docs, text="Amendă:").grid(row=r_doc, column=0, padx=10, pady=2, sticky="w")
        ctk.CTkComboBox(frame_docs, variable=vehicle_vars[f'amenda_retinere_auto{auto_number}'], values=['', 'AVERTISMENT', '_______________']).grid(row=r_doc, column=1, padx=2, pady=2, sticky="ew")
        
        r_doc += 1
        ctk.CTkFrame(frame_docs, height=1, fg_color="gray50").grid(row=r_doc, column=0, columnspan=2, sticky='ew', pady=5, padx=10)
        
        r_doc += 1
        ctk.CTkCheckBox(frame_docs, text="Raport Reținere ITP Expirat", variable=vehicle_vars[f'raport_retinere_itp_auto{auto_number}']).grid(row=r_doc, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        
        r_doc += 1
        ctk.CTkLabel(frame_docs, text="Serie PVCC:").grid(row=r_doc, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_docs, textvariable=vehicle_vars[f'serie_pvcc_auto{auto_number}']).grid(row=r_doc, column=1, padx=2, pady=2, sticky="ew")
        
        r_doc += 1
        ctk.CTkCheckBox(frame_docs, text="Raport Reținere RCA Expirat", variable=vehicle_vars[f'raport_retinere_rca_auto{auto_number}']).grid(row=r_doc, column=0, columnspan=2, padx=10, pady=(2,10), sticky="w")

        # Frame Articole CP
        frame_cp = ctk.CTkFrame(frame_docs_cp_container, border_width=1)
        frame_cp.grid(row=0, column=1, padx=(5,0), pady=0, sticky="nsew")
        ctk.CTkLabel(frame_cp, text="+ alt articol CP:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(5, 10), sticky="ew")
        
        cp_keys = [
            'art_334_1_auto', 'art_336_1_auto', 'art_334_2_auto', 'art_336_1ind1_auto',
            'art_334_3_auto', 'art_336_2_auto', 'art_334_4_auto', 'art_337_auto',
            'art_335_1_auto', 'art_338_1_auto', 'art_335_2_auto', 'art_338_2_auto'
        ]
        cp_texts = {
            'art_334_1_auto': 'Art. 334/1', 'art_336_1_auto': 'Art. 336/1',
            'art_334_2_auto': 'Art. 334/2', 'art_336_1ind1_auto': 'Art. 336/1^1',
            'art_334_3_auto': 'Art. 334/3', 'art_336_2_auto': 'Art. 336/2',
            'art_334_4_auto': 'Art. 334/4', 'art_337_auto': 'Art. 337',
            'art_335_1_auto': 'Art. 335/1', 'art_338_1_auto': 'Art. 338/1',
            'art_335_2_auto': 'Art. 335/2', 'art_338_2_auto': 'Art. 338/2'
        }
        
        r_cp, c_cp = 1, 0
        for key in cp_keys:
            full_key = f"{key}{auto_number}"
            ctk.CTkCheckBox(frame_cp, text=cp_texts[key], width=110, variable=vehicle_vars[full_key]).grid(row=r_cp, column=c_cp, padx=10, pady=2, sticky="w")
            c_cp = (c_cp + 1) % 2
            if c_cp == 0: r_cp += 1
        
        # --- Frame Testări ---
        frame_testari = ctk.CTkFrame(parent_scrollable_frame, border_width=1)
        frame_testari.pack(fill="x", padx=5, pady=5, expand=False)
        ctk.CTkLabel(frame_testari, text="Testări", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 10))
        
        etilo_container = ctk.CTkFrame(frame_testari, fg_color="transparent")
        etilo_container.pack(fill="x", padx=10, pady=2)

        etilo_frame1 = ctk.CTkFrame(etilo_container, fg_color="transparent")
        etilo_frame1.pack(fill="x", anchor="w")
        ctk.CTkComboBox(etilo_frame1, width=150, state="readonly", variable=vehicle_vars[f'etilo_auto{auto_number}'], values=['A fost testat','Nu a fost testat', 'A refuzat testarea']).pack(side="left")
        ctk.CTkLabel(etilo_frame1, text="cu aparatul etilotest marca Drager seria").pack(side="left", padx=(5,2))
        ctk.CTkEntry(etilo_frame1, width=60, textvariable=vehicle_vars[f'serie_etilo_auto{auto_number}']).pack(side="left", padx=2)

        etilo_frame2 = ctk.CTkFrame(etilo_container, fg_color="transparent")
        etilo_frame2.pack(fill="x", anchor="w", pady=(2,0))
        ctk.CTkLabel(etilo_frame2, text="care la poziția").pack(side="left")
        ctk.CTkEntry(etilo_frame2, width=60, textvariable=vehicle_vars[f'pozitie_etilo_auto{auto_number}']).pack(side="left", padx=2)
        ctk.CTkLabel(etilo_frame2, text="a indicat o valoare de").pack(side="left", padx=(10,2))
        ctk.CTkComboBox(etilo_frame2, width=80, variable=vehicle_vars[f'rezultat_etilo_auto{auto_number}'], values=['0,00', ' ']).pack(side="left")
        ctk.CTkLabel(etilo_frame2, text="mg/l alcool pur în aerul expirat.").pack(side="left", padx=2)
        
        # --- Drugtest & Probe Biologice (Collapsible) ---
        drugtest_container = ctk.CTkFrame(frame_testari, fg_color="transparent")
        drugtest_container.pack(fill="x", padx=5, pady=5)

        drugtest_probe_visible_var = vehicle_vars[f'drugtest_probe_visible{auto_number}']
        frame_drugtest_content = ctk.CTkFrame(drugtest_container)

        def toggle_drugtest():
            if drugtest_probe_visible_var.get() == 0:
                frame_drugtest_content.pack(after=btn_toggle_drugtest, fill="x", expand=True, pady=(0,5))
                btn_toggle_drugtest.configure(text="▼ Drugtest si Probe Biologice")
                drugtest_probe_visible_var.set(1)
            else:
                frame_drugtest_content.pack_forget()
                btn_toggle_drugtest.configure(text="▶ Drugtest si Probe Biologice")
                drugtest_probe_visible_var.set(0)

        btn_toggle_drugtest = ctk.CTkButton(
            drugtest_container, text="▶ Drugtest si Probe Biologice", command=toggle_drugtest, anchor="w",
            fg_color="transparent", text_color=(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            hover=False
        )
        btn_toggle_drugtest.pack(fill="x")
        
        frame_drugtest_content.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame_drugtest_content, text="DrugTest:").grid(row=0, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkComboBox(frame_drugtest_content, state="readonly", variable=vehicle_vars[f'drugtest_auto{auto_number}'], values=['A fost testat','Nu a fost testat', 'A refuzat testarea']).grid(row=0, column=1, padx=(0,10), pady=2, sticky="ew")
        
        ctk.CTkLabel(frame_drugtest_content, text="Serie aparat:").grid(row=1, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_drugtest_content, textvariable=vehicle_vars[f'serie_drugtest_auto{auto_number}']).grid(row=1, column=1, padx=(0,10), pady=2, sticky="ew")

        ctk.CTkLabel(frame_drugtest_content, text="Poziție test:").grid(row=2, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_drugtest_content, textvariable=vehicle_vars[f'pozitie_drugtest_auto{auto_number}']).grid(row=2, column=1, padx=(0,10), pady=2, sticky="ew")

        ctk.CTkLabel(frame_drugtest_content, text="Rezultat:").grid(row=3, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkComboBox(frame_drugtest_content, state="readonly", variable=vehicle_vars[f'rezultat_drugtest_auto{auto_number}'], values=['Pozitiv', 'Negativ', '-----------']).grid(row=3, column=1, padx=(0,10), pady=2, sticky="ew")

        ctk.CTkLabel(frame_drugtest_content, text="Substanță:").grid(row=4, column=0, padx=(10,2), pady=2, sticky="w")
        ctk.CTkEntry(frame_drugtest_content, textvariable=vehicle_vars[f'droguri_drugtest_auto{auto_number}']).grid(row=4, column=1, padx=(0,10), pady=2, sticky="ew")

        ctk.CTkFrame(frame_drugtest_content, height=1, fg_color="gray50").grid(row=5, column=0, columnspan=2, sticky='ew', pady=5, padx=10)

        ctk.CTkLabel(frame_drugtest_content, text="Probe biologice:").grid(row=6, column=0, padx=(10,2), pady=(2,10), sticky="w")
        ctk.CTkComboBox(frame_drugtest_content, state="readonly", variable=vehicle_vars[f'inml_auto{auto_number}'], values=['Au fost recoltate','Nu au fost recoltate']).grid(row=6, column=1, padx=(0,10), pady=(2,10), sticky="ew")
        
        ctk.CTkLabel(frame_drugtest_content, text="Sigiliu trusă:").grid(row=7, column=0, padx=(10,2), pady=(2,10), sticky="w")
        ctk.CTkEntry(frame_drugtest_content, textvariable=vehicle_vars[f'sigiliu_inml_auto{auto_number}']).grid(row=7, column=1, padx=(0,10), pady=(2,10), sticky="ew")

        # --- Frame pentru direcția de deplasare ---
        frame_conducere_container = ctk.CTkFrame(parent_scrollable_frame, border_width=1)
        frame_conducere_container.pack(fill="x", padx=5, pady=5, expand=False)
        
        frame_conducere_row1 = ctk.CTkFrame(frame_conducere_container, fg_color="transparent")
        frame_conducere_row1.pack(fill="x", padx=10, pady=(5, 2))

        ctk.CTkLabel(frame_conducere_row1, text="Vehiculul a fost condus pe strada").pack(side="left")
        entry_condus_strada = ctk.CTkEntry(frame_conducere_row1, textvariable=vehicle_vars[f'condus_strada{auto_number}'])
        entry_condus_strada.pack(side="left", padx=2, expand=True, fill="x")
        entry_condus_strada.bind("<KeyPress>", self.on_key_press_remedy)
        entry_condus_strada.bind("<Button-3>", self._show_context_menu)

        ctk.CTkLabel(frame_conducere_row1, text=", din direcția").pack(side="left", padx=(5,0))
        entry_condus_directia = ctk.CTkEntry(frame_conducere_row1, textvariable=vehicle_vars[f'condus_directia{auto_number}'])
        entry_condus_directia.pack(side="left", padx=2, expand=True, fill="x")
        entry_condus_directia.bind("<KeyPress>", self.on_key_press_remedy)
        entry_condus_directia.bind("<Button-3>", self._show_context_menu)

        frame_conducere_row2 = ctk.CTkFrame(frame_conducere_container, fg_color="transparent")
        frame_conducere_row2.pack(fill="x", padx=10, pady=(0, 5))

        ctk.CTkLabel(frame_conducere_row2, text="către").pack(side="left")
        entry_condus_catre = ctk.CTkEntry(frame_conducere_row2, textvariable=vehicle_vars[f'condus_catre{auto_number}'])
        entry_condus_catre.pack(side="left", padx=(2,0), expand=True, fill="x")
        entry_condus_catre.bind("<KeyPress>", self.on_key_press_remedy)
        entry_condus_catre.bind("<Button-3>", self._show_context_menu)
        
        # --- Frames pentru Textbox-uri ---
        def create_textbox_frame(parent, title, text_var_key, default_text):
            frame = ctk.CTkFrame(parent, border_width=1)
            frame.pack(fill="x", padx=5, pady=5, expand=False)
            ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold")).pack(fill="x", padx=10, pady=(5,5))
            textbox = ctk.CTkTextbox(frame, height=100, wrap=tk.WORD)
            textbox.pack(fill="x", expand=True, padx=10, pady=(0,10))
            textbox.bind("<KeyPress>", self.on_key_press_remedy)
            textbox.bind("<Button-3>", self._show_context_menu)
            text_var = vehicle_vars[text_var_key]
            current_text = text_var.get()
            if not current_text:
                text_var.set(default_text)
            textbox.insert("1.0", text_var.get())
            textbox.bind("<FocusOut>", lambda event, w=textbox, v=text_var: self._update_var_from_text(w, v))
            return frame, textbox
        
        declaratie_frame, declaratie_textbox = create_textbox_frame(parent_scrollable_frame, "Declarație", f'text_declaratie_sofer_auto{auto_number}', 'Persoana în cauză nu a fost prezentă la fața locului la momentul efectuării CFL.')
        
        buttons_frame = ctk.CTkFrame(declaratie_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10), anchor="w")

        def set_declaration_text(text):
            declaratie_textbox.delete("1.0", "end")
            declaratie_textbox.insert("1.0", text)
            self._update_var_from_text(declaratie_textbox, vehicle_vars[f'text_declaratie_sofer_auto{auto_number}'])

        def get_common_template_data():
            data_accident = self.initial_data.get('data_producerii_accidentului', '___________')
            ora_accident = self.initial_data.get('ora_producerii_accidentului', '______')
            loc_accident = self.initial_data.get('locul_producerii_accidentului', '___________')
            tip_vehicul = vehicle_vars[f'tip_auto{auto_number}'].get()
            marca_model = vehicle_vars[f'marca_auto{auto_number}'].get()
            strada = vehicle_vars[f'condus_strada{auto_number}'].get()
            directia = vehicle_vars[f'condus_directia{auto_number}'].get()
            catre = vehicle_vars[f'condus_catre{auto_number}'].get()
            return data_accident, ora_accident, loc_accident, tip_vehicul, marca_model, strada, directia, catre

        def generate_template_declaration_auto():
            data_accident, ora_accident, loc_accident, tip_vehicul, marca_model, strada, directia, catre = get_common_template_data()
            nr_vehicul = vehicle_vars[f'nr_auto{auto_number}'].get()
            template = (
                f"La data de {data_accident}, în jurul orelor {ora_accident}, a condus "
                f"{tip_vehicul} {marca_model} cu nr. {nr_vehicul}, pe strada {strada}, "
                f"din directia {directia}, către {catre}. "
                f"Când a ajuns în întersecția {loc_accident}, a "
                "___________________________________________________"
            )
            set_declaration_text(template)

        def generate_template_declaration_no_plate():
            data_accident, ora_accident, loc_accident, tip_vehicul, marca_model, strada, directia, catre = get_common_template_data()
            template = (
                f"La data de {data_accident}, în jurul orelor {ora_accident}, a condus "
                f"{tip_vehicul} {marca_model}, pe strada {strada}, "
                f"din directia {directia}, către {catre}. "
                f"Când a ajuns în întersecția {loc_accident}, a "
                "___________________________________________________"
            )
            set_declaration_text(template)
            
        btn_nu_prezent = ctk.CTkButton(buttons_frame, text="Nu este prezent", height=20, command=lambda: set_declaration_text('Persoana în cauză nu a fost prezentă la fața locului la momentul efectuării CFL.'))
        btn_nu_prezent.pack(side="left", padx=(0, 5))

        btn_auto = ctk.CTkButton(buttons_frame, text="Declarație Auto", height=20, command=generate_template_declaration_auto)
        btn_auto.pack(side="left", padx=5)
        
        btn_troti = ctk.CTkButton(buttons_frame, text="Declarație Trotineta/Bicicleta", height=20, command=generate_template_declaration_no_plate)
        btn_troti.pack(side="left", padx=5)

        btn_fara = ctk.CTkButton(buttons_frame, text="Fără declarație", height=20, command=lambda: set_declaration_text(''))
        btn_fara.pack(side="left", padx=5)
        
        # --- MODIFICARE: Refactorizare Frame Pozitie Vehicul ---
        pozitie_frame = ctk.CTkFrame(parent_scrollable_frame, border_width=1)
        pozitie_frame.pack(fill="x", padx=5, pady=5, expand=False)
        ctk.CTkLabel(pozitie_frame, text="La fața locului vehiculul se afla în următoarea poziție:", font=ctk.CTkFont(weight="bold")).pack(fill="x", padx=10, pady=(5,5))

        # --- MUTA SECTIUNEA MĂSURĂTORI AICI ---
        masuratori_container = ctk.CTkFrame(pozitie_frame, fg_color="transparent")
        masuratori_container.pack(fill="x", padx=5, pady=0)
        
        masuratori_visible_var = vehicle_vars[f'masuratori_visible{auto_number}']
        frame_masuratori_content = ctk.CTkFrame(masuratori_container, border_width=1)
        
        def toggle_masuratori():
            if masuratori_visible_var.get() == 0:
                frame_masuratori_content.pack(after=btn_toggle_masuratori, fill="x", expand=True, pady=(0,5))
                btn_toggle_masuratori.configure(text="▼ Măsurători")
                masuratori_visible_var.set(1)
            else:
                frame_masuratori_content.pack_forget()
                btn_toggle_masuratori.configure(text="▶ Măsurători")
                masuratori_visible_var.set(0)

        btn_toggle_masuratori = ctk.CTkButton(
            masuratori_container, text="▶ Măsurători", command=toggle_masuratori, anchor="w",
            font=ctk.CTkFont(weight="bold"),
            fg_color="transparent", text_color=(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            hover=False
        )
        btn_toggle_masuratori.pack(fill="x")

        # --- Content of Măsurători ---
        row_mas_1 = ctk.CTkFrame(frame_masuratori_content, fg_color="transparent")
        row_mas_1.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row_mas_1, text="Vehiculul se afla pe partea carosabila a străzii").pack(side="left")
        ctk.CTkEntry(row_mas_1, width=100, textvariable=vehicle_vars[f'masuratori_strada_vehicul{auto_number}']).pack(side="left", padx=2)
        ctk.CTkLabel(row_mas_1, text=", orientat cu fata către").pack(side="left")
        ctk.CTkEntry(row_mas_1, width=100, textvariable=vehicle_vars[f'masuratori_orientare_vehicul{auto_number}']).pack(side="left", padx=2)

        row_mas_2 = ctk.CTkFrame(frame_masuratori_content, fg_color="transparent")
        row_mas_2.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row_mas_2, text="Măsurătorile au fost efectuate privind strada dinspre").pack(side="left")
        ctk.CTkEntry(row_mas_2, width=100, textvariable=vehicle_vars[f'masuratori_privind_dinspre{auto_number}']).pack(side="left", padx=2)
        ctk.CTkLabel(row_mas_2, text=", către").pack(side="left")
        ctk.CTkEntry(row_mas_2, width=100, textvariable=vehicle_vars[f'masuratori_privind_catre{auto_number}']).pack(side="left", padx=2)

        row_mas_radio = ctk.CTkFrame(frame_masuratori_content, fg_color="transparent")
        row_mas_radio.pack(fill="x", padx=10, pady=5)
        orientare_ax_var = vehicle_vars[f'masuratori_orientare_ax{auto_number}']
        orientare_ax_var.set(1)
        ctk.CTkRadioButton(row_mas_radio, text="paralel cu axul drumului | ↑ |", variable=orientare_ax_var, value=1).pack(side="left", padx=5)
        ctk.CTkRadioButton(row_mas_radio, text="oblic spre stanga | ← |", variable=orientare_ax_var, value=2).pack(side="left", padx=5)
        ctk.CTkRadioButton(row_mas_radio, text="oblic spre dreapta | → |", variable=orientare_ax_var, value=3).pack(side="left", padx=5)

        # --- MODIFICARE: Car Diagram ---
        car_diagram_frame = ctk.CTkFrame(frame_masuratori_content, fg_color="transparent")
        car_diagram_frame.pack(pady=10)
        
        car_diagram_frame.columnconfigure(0, minsize=95)
        car_diagram_frame.columnconfigure(1, minsize=100)
        car_diagram_frame.columnconfigure(2, minsize=95)

        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="inainte", textvariable=vehicle_vars[f'masuratori_dist_inainte{auto_number}']).grid(row=0, column=1, pady=2)
        
        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="stg. fata", textvariable=vehicle_vars[f'masuratori_dist_stg_fata{auto_number}']).grid(row=1, column=0, sticky="e", padx=5)
        ctk.CTkLabel(car_diagram_frame, text="┌ -----┐", font=("Courier", 12)).grid(row=1, column=1)
        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="dr. fata", textvariable=vehicle_vars[f'masuratori_dist_dr_fata{auto_number}']).grid(row=1, column=2, sticky="w", padx=5)
        
        ctk.CTkLabel(car_diagram_frame, text="|    ▲    |", font=("Courier", 12)).grid(row=2, column=1)
        
        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="partea stanga", textvariable=vehicle_vars[f'masuratori_dist_lateral_stg{auto_number}']).grid(row=3, column=0, sticky="e", padx=5)
        ctk.CTkLabel(car_diagram_frame, text="|         |", font=("Courier", 12)).grid(row=3, column=1)
        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="partea dreapta", textvariable=vehicle_vars[f'masuratori_dist_lateral_dr{auto_number}']).grid(row=3, column=2, sticky="w", padx=5)

        ctk.CTkLabel(car_diagram_frame, text="|         |", font=("Courier", 12)).grid(row=4, column=1)

        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="stg. spate", textvariable=vehicle_vars[f'masuratori_dist_stg_spate{auto_number}']).grid(row=5, column=0, sticky="e", padx=5)
        ctk.CTkLabel(car_diagram_frame, text="└ -----┘", font=("Courier", 12)).grid(row=5, column=1)
        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="dr. spate", textvariable=vehicle_vars[f'masuratori_dist_dr_spate{auto_number}']).grid(row=5, column=2, sticky="w", padx=5)

        ctk.CTkEntry(car_diagram_frame, width=90, placeholder_text="inapoi", textvariable=vehicle_vars[f'masuratori_dist_inapoi{auto_number}']).grid(row=6, column=1, pady=2)
        # --- Sfârșit Car Diagram ---

        pozitie_textbox = ctk.CTkTextbox(pozitie_frame, height=100, wrap=tk.WORD)
        pozitie_textbox.pack(fill="x", expand=True, padx=10, pady=(0,10))
        pozitie_textbox.bind("<KeyPress>", self.on_key_press_remedy)
        pozitie_textbox.bind("<Button-3>", self._show_context_menu)
        pozitie_text_var = vehicle_vars[f'text_pozitie_auto{auto_number}']
        pozitie_current_text = pozitie_text_var.get()
        if not pozitie_current_text:
            pozitie_text_var.set('Vehiculul nu se afla în poziția inițială producerii accidentului la momentul efectuării CFL.')
        pozitie_textbox.insert("1.0", pozitie_text_var.get())
        pozitie_textbox.bind("<FocusOut>", lambda event, w=pozitie_textbox, v=pozitie_text_var: self._update_var_from_text(w, v))
        
        pozitie_buttons_frame = ctk.CTkFrame(pozitie_frame, fg_color="transparent")
        pozitie_buttons_frame.pack(fill="x", padx=10, pady=(0, 10), anchor="w")

        def set_pozitie_text(text):
            pozitie_textbox.delete("1.0", "end")
            pozitie_textbox.insert("1.0", text)
            self._update_var_from_text(pozitie_textbox, vehicle_vars[f'text_pozitie_auto{auto_number}'])

        def generate_pozitie_auto_text():
            loc_accident = self.initial_data.get('locul_producerii_accidentului', '___________')
            strada_vehicul = vehicle_vars[f'masuratori_strada_vehicul{auto_number}'].get() or '___________'
            orientare_vehicul = vehicle_vars[f'masuratori_orientare_vehicul{auto_number}'].get() or '___________'
            privind_dinspre = vehicle_vars[f'masuratori_privind_dinspre{auto_number}'].get() or '___________'
            privind_catre = vehicle_vars[f'masuratori_privind_catre{auto_number}'].get() or '___________'
            
            orientare_ax_val = vehicle_vars[f'masuratori_orientare_ax{auto_number}'].get()
            orientare_ax_text = {
                1: "paralel cu axul drumului",
                2: "oblic spre stanga fata de axul drumului",
                3: "oblic spre dreapta fata de axul drumului"
            }.get(orientare_ax_val, "")

            text = (
                f"Vehiculul se afla pe partea carosabilă a străzii {strada_vehicul}, în intersectia {loc_accident}, "
                f"orientat cu partea din fata către {orientare_vehicul}, {orientare_ax_text}.\n"
                f"Privind strada {strada_vehicul} dinspre {privind_dinspre} către {privind_catre} au fost efectuate următoarele măsurători:\n"
            )

            masuratori = {
                "inainte": ("înainte", "partea din fata"), "dr_fata": ("către dreapta", "coltul dreapta fata"),
                "lateral_dr": ("către dreapta", "partea laterala dreapta"), "dr_spate": ("către dreapta", "coltul dreapta spate"),
                "inapoi": ("înapoi", "partea din spate"), "stg_spate": ("către stânga", "coltul stânga spate"),
                "lateral_stg": ("către stânga", "partea laterala stânga"), "stg_fata": ("către stânga", "coltul stânga fata")
            }
            
            added_measurements = False
            for key_suffix, (directie, punct_reper) in masuratori.items():
                val = vehicle_vars[f'masuratori_dist_{key_suffix}{auto_number}'].get()
                if val:
                    added_measurements = True
                    # MODIFICARE: Curăță valoarea de unități de măsură
                    cleaned_val = val.lower().replace('m', '').strip()
                    bordura_directie = "stânga" if "stg" in key_suffix or "stânga" in directie else "dreapta"
                    text += f"- s-a măsurat {directie} ({cleaned_val} m) de la {punct_reper} pana la bordura/nivelul bordurii din {bordura_directie} a străzii {strada_vehicul}.\n"
            
            if not added_measurements:
                text += "Nu au fost efectuate măsurători.\n"

            set_pozitie_text(text.strip())

        ctk.CTkButton(pozitie_buttons_frame, text="Fara pozitie", height=20, command=lambda: set_pozitie_text('Vehiculul nu se afla în poziția inițială producerii accidentului la momentul efectuării CFL.')).pack(side="left", padx=(0, 5))
        ctk.CTkButton(pozitie_buttons_frame, text="Pozitie auto", height=20, command=generate_pozitie_auto_text).pack(side="left", padx=5)

        create_textbox_frame(parent_scrollable_frame, f"Avarii Vehicul nr. {auto_number}", f'text_avarii_auto{auto_number}', 'Nu există avarii.')
        
        # --- SECȚIUNE EXAMINARE VEHICUL (COLLAPSIBLE) ---
        examinare_visible_var = vehicle_vars[f'examinare_vehicul_visible{auto_number}']
        
        frame_examinare_content = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)

        def toggle_examinare():
            if examinare_visible_var.get() == 0:
                frame_examinare_content.pack(fill="x", padx=5, pady=(0,5), expand=False, after=btn_toggle_examinare)
                btn_toggle_examinare.configure(text="▼ Examinând vehiculul am constatat următoarele:")
                examinare_visible_var.set(1)
            else:
                frame_examinare_content.pack_forget()
                btn_toggle_examinare.configure(text="▶ Examinând vehiculul am constatat următoarele:")
                examinare_visible_var.set(0)

        btn_toggle_examinare = ctk.CTkButton(
            parent_scrollable_frame,
            text="▶ Examinând vehiculul am constatat următoarele:",
            command=toggle_examinare,
            anchor="w",
            fg_color=("gray70", "gray25"),
            text_color=(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"]
        )
        btn_toggle_examinare.pack(fill="x", padx=5, pady=(10,0))

        # Populăm frame_examinare_content
        ex_row = 0
        ctk.CTkLabel(frame_examinare_content, text="Detalii suplimentare vehicul:", font=ctk.CTkFont(weight="bold")).grid(
            row=ex_row, column=0, columnspan=4, pady=(5,10), padx=5, sticky="ew")
        ex_row += 1
        # Anvelope
        frame_anv = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_anv.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_anv, text="- tipul anvelopelor:").pack(side="left")
        ctk.CTkComboBox(frame_anv, width=100, variable=vehicle_vars[f'examinare_anvelope_tip{auto_number}'], values=['vară', 'iarnă', 'mixt']).pack(side="left", padx=2)
        ctk.CTkLabel(frame_anv, text=", uzura anvelopelor:").pack(side="left")
        ctk.CTkComboBox(frame_anv, width=120, variable=vehicle_vars[f'examinare_anvelope_uzura{auto_number}'], values=['redusă', 'medie', 'peste limită']).pack(side="left", padx=2)
        ex_row += 1
        # Iluminare
        frame_ilum = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_ilum.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_ilum, text="- sistemul de iluminare semnalizare – în stare de funcționare:").pack(side="left")
        ctk.CTkComboBox(frame_ilum, width=150, variable=vehicle_vars[f'examinare_iluminare_functional{auto_number}'], values=['da', 'nu', 'nu se poate stabili']).pack(side="left", padx=2)
        ex_row += 1
        # Ștergătoare
        frame_sterg = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_sterg.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_sterg, text="- ștergătoare de parbriz – există:").pack(side="left")
        ctk.CTkComboBox(frame_sterg, width=80, variable=vehicle_vars[f'examinare_stergatoare_exista{auto_number}'], values=['da', 'nu']).pack(side="left", padx=2)
        ctk.CTkLabel(frame_sterg, text=", în stare de funcționare:").pack(side="left")
        ctk.CTkComboBox(frame_sterg, width=150, variable=vehicle_vars[f'examinare_stergatoare_functional{auto_number}'], values=['da', 'nu', 'nu se poate stabili']).pack(side="left", padx=2)
        ex_row += 1
        # Portiere
        frame_port = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_port.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_port, text="- portierele:").pack(side="left")
        ctk.CTkComboBox(frame_port, width=100, variable=vehicle_vars[f'examinare_portiere_stare{auto_number}'], values=['închise', 'deschise']).pack(side="left", padx=2)
        ctk.CTkComboBox(frame_port, width=120, variable=vehicle_vars[f'examinare_portiere_asigurare{auto_number}'], values=['asigurate', 'neasigurate']).pack(side="left", padx=2)
        ctk.CTkLabel(frame_port, text="cu mecanism:").pack(side="left")
        ctk.CTkComboBox(frame_port, width=100, variable=vehicle_vars[f'examinare_portiere_mecanism{auto_number}'], values=['asistat', 'manual']).pack(side="left", padx=2)
        ex_row += 1
        # Manete și airbaguri
        frame_manete = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_manete.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
        frame_manete.columnconfigure(1, weight=1)
        ctk.CTkLabel(frame_manete, text="- poziția manetei schimbător de viteze:").grid(row=0, column=0, sticky="w", pady=1)
        ctk.CTkEntry(frame_manete, textvariable=vehicle_vars[f'examinare_maneta_viteze{auto_number}']).grid(row=0, column=1, sticky="ew", padx=5, pady=1)
        ctk.CTkLabel(frame_manete, text="- poziția manetei frână de mână:").grid(row=1, column=0, sticky="w", pady=1)
        ctk.CTkEntry(frame_manete, textvariable=vehicle_vars[f'examinare_frana_mana{auto_number}']).grid(row=1, column=1, sticky="ew", padx=5, pady=1)
        ctk.CTkLabel(frame_manete, text="- airbag-uri declanșate:").grid(row=2, column=0, sticky="w", pady=1)
        ctk.CTkEntry(frame_manete, textvariable=vehicle_vars[f'examinare_airbaguri{auto_number}']).grid(row=2, column=1, sticky="ew", padx=5, pady=1)
        ex_row += 1
        # Kilometraj
        frame_km = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_km.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_km, text="- poziția acului kilometraj:").pack(side="left")
        ctk.CTkEntry(frame_km, width=70, textvariable=vehicle_vars[f'examinare_ac_kilometraj{auto_number}']).pack(side="left", padx=2)
        ctk.CTkLabel(frame_km, text="km/h, turometru:").pack(side="left")
        ctk.CTkEntry(frame_km, width=70, textvariable=vehicle_vars[f'examinare_turometru{auto_number}']).pack(side="left", padx=2)
        ctk.CTkLabel(frame_km, text="rot/min, km indicați:").pack(side="left")
        ctk.CTkEntry(frame_km, width=100, textvariable=vehicle_vars[f'examinare_km_indicati{auto_number}']).pack(side="left", padx=2)
        ex_row += 1
        # Frâne
        frame_frane = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_frane.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_frane, text="- pedala/maneta frânei de serviciu – opune rezistență:").pack(side="left")
        ctk.CTkComboBox(frame_frane, width=150, variable=vehicle_vars[f'examinare_pedala_frana{auto_number}'], values=['da', 'nu', 'nu se poate stabili']).pack(side="left", padx=2)
        ctk.CTkLabel(frame_frane, text=", sistemul de frânare:").pack(side="left")
        ctk.CTkComboBox(frame_frane, width=150, variable=vehicle_vars[f'examinare_sistem_franare{auto_number}'], values=['clasic', 'servo-asistat', 'ABS']).pack(side="left", padx=2)
        ex_row += 1
        # Încărcătură
        frame_incarc = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_incarc.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
        frame_incarc.columnconfigure(1, weight=1)
        ctk.CTkLabel(frame_incarc, text="- încărcat cu: persoane nr.").grid(row=0, column=0, sticky="w", pady=1)
        ctk.CTkEntry(frame_incarc, width=50, textvariable=vehicle_vars[f'examinare_incarcatura_persoane{auto_number}']).grid(row=0, column=1, sticky="w", padx=2, pady=1)
        ctk.CTkLabel(frame_incarc, text="/ tip încărcătură:").grid(row=0, column=2, sticky="w", pady=1)
        ctk.CTkEntry(frame_incarc, textvariable=vehicle_vars[f'examinare_incarcatura_tip{auto_number}']).grid(row=0, column=3, sticky="ew", padx=2, pady=1)
        ctk.CTkLabel(frame_incarc, text="- greutatea, modul de așezare și prindere a încărcăturii:").grid(row=1, column=0, columnspan=4, sticky="w", pady=1)
        ctk.CTkEntry(frame_incarc, placeholder_text="Detalii încărcătură...", textvariable=vehicle_vars[f'examinare_incarcatura_detalii{auto_number}']).grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=1)
        ex_row += 1
        # Elemente siguranță
        frame_sig = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
        frame_sig.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(frame_sig, text="- elemente de siguranță și protecție:").pack(anchor="w")
        sig_options_frame = ctk.CTkFrame(frame_sig, fg_color="transparent")
        sig_options_frame.pack(anchor="w", fill="x")
        ctk.CTkCheckBox(sig_options_frame, text="centuri", variable=vehicle_vars[f'examinare_sig_centuri{auto_number}']).pack(side="left", padx=5)
        ctk.CTkCheckBox(sig_options_frame, text="scaun copil", variable=vehicle_vars[f'examinare_sig_scaun_copil{auto_number}']).pack(side="left", padx=5)
        ctk.CTkCheckBox(sig_options_frame, text="reflectorizante", variable=vehicle_vars[f'examinare_sig_reflectorizante{auto_number}']).pack(side="left", padx=5)
        ctk.CTkCheckBox(sig_options_frame, text="cască", variable=vehicle_vars[f'examinare_sig_casca{auto_number}']).pack(side="left", padx=5)
        ctk.CTkCheckBox(sig_options_frame, text="geacă", variable=vehicle_vars[f'examinare_sig_geaca{auto_number}']).pack(side="left", padx=5)
        ctk.CTkCheckBox(sig_options_frame, text="pantaloni", variable=vehicle_vars[f'examinare_sig_pantaloni{auto_number}']).pack(side="left", padx=5)
        ctk.CTkEntry(sig_options_frame, placeholder_text="Altele...", width=150, textvariable=vehicle_vars[f'examinare_sig_altele{auto_number}']).pack(side="left", padx=5, pady=(0,5), expand=True, fill="x")

        if examinare_visible_var.get() == 1:
            frame_examinare_content.pack(fill="x", padx=5, pady=(0,5), expand=False, after=btn_toggle_examinare)
            btn_toggle_examinare.configure(text="▼ Examinând vehiculul am constatat următoarele:")
        else:
            btn_toggle_examinare.configure(text="▶ Examinând vehiculul am constatat următoarele:")


    def get_data(self):
        all_auto_data = {}
        for i, vehicle_vars_dict in enumerate(self.all_vehicle_data_vars, 1):
            for key_template in self.DATA_KEYS_PER_AUTO:
                base_key = key_template[:-1] if key_template.endswith('x') else key_template
                original_key = f"{base_key}{i}"
                if original_key in vehicle_vars_dict:
                    try:
                        all_auto_data[original_key] = vehicle_vars_dict[original_key].get()
                    except Exception as e:
                        print(f"Eroare la citirea datei pentru cheia {original_key}: {e}")
                        all_auto_data[original_key] = f"EROARE_CITIRE"
        return all_auto_data
