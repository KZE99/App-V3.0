import customtkinter as ctk
import tkinter as tk
from src.login.login_window import LoginWindow
from src.main_app.main_page import MainPage
from src.utils.data_manager import check_security
import sys

class AppController(ctk.CTk):
    """
    Controller-ul central al aplicației.
    Gestionează stările, securitatea, diacriticele și temele.
    """
    def __init__(self):
        super().__init__()

        # --- 1. VERIFICARE SECURITATE ---
        # Integrăm logica din BARSV APP V3.2
        if not check_security():
            # Folosim un mesaj temporar deoarece fereastra principală nu e gata
            root = tk.Tk()
            root.withdraw()
            tk.messagebox.showerror("Eroare Securitate", "Această stație de lucru nu este autorizată să ruleze aplicația.")
            root.destroy()
            sys.exit()

        # --- 2. CONFIGURARE FEREASTRĂ RĂDĂCINĂ ---
        self.title("Manager Documente BARSV")
        self.geometry("1000x700")
        self.withdraw() # Rămâne ascunsă până la login succes

        # Setări aspect
        ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")

        # --- 3. LOGICA PENTRU DIACRITICE (REPER: BARSV V3.2) ---
        self.REMEDIED_CHARS = {
            ord(c): c for c in 'șțâîăȘȚÂÎĂ'
        }

        # Date utilizator
        self.current_user = None
        
        # Lansăm procesul de login
        self.show_login_window()

    def on_key_press_remedy(self, event):
        """Handler-ul de corecție pentru caractere românești."""
        char_remedy = self.REMEDIED_CHARS.get(event.keysym_num)
        if char_remedy:
            event.widget.insert('insert', char_remedy)
            return 'break'

    def show_context_menu(self, event):
        """Meniu click-dreapta pentru Cut/Copy/Paste (Reper: BARSV V3.2)."""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Taie", command=lambda: event.widget.event_generate("<<Cut>>"))
        menu.add_command(label="Copiază", command=lambda: event.widget.event_generate("<<Copy>>"))
        menu.add_command(label="Lipește", command=lambda: event.widget.event_generate("<<Paste>>"))
        menu.tk_popup(event.x_root, event.y_root)

    def apply_global_patches(self, parent_widget):
        """
        Aplică recursiv diacriticele și meniul de click-dreapta 
        pe toate elementele de input.
        """
        # Widget-uri care acceptă text
        input_widgets = (ctk.CTkEntry, ctk.CTkComboBox, ctk.CTkTextbox)

        for widget in parent_widget.winfo_children():
            # Verificăm dacă este un widget de input sau dacă are un sub-widget de tip Entry
            if isinstance(widget, input_widgets):
                # Bind pentru diacritice
                widget.bind("<KeyPress>", self.on_key_press_remedy)
                # Bind pentru click dreapta
                widget.bind("<Button-3>", self.show_context_menu)
            
            # Continuăm recursiv în containere (frames, tabviews)
            self.apply_global_patches(widget)

    def show_login_window(self):
        """Deschide fereastra de autentificare."""
        login_win = LoginWindow(master=self, on_login_success_callback=self.on_login_success)
        
        # Aplicăm patch-urile pe fereastra de login
        self.apply_global_patches(login_win)
        
        # Dacă se închide fereastra de login fără succes, închidem tot
        login_win.protocol("WM_DELETE_WINDOW", self.destroy)

    def on_login_success(self, username):
        """Callback apelat de LoginWindow la succes."""
        self.current_user = username
        
        # Distrugem toate ferestrele CTkToplevel (fereastra de login)
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
        
        # Afișăm fereastra principală
        self.deiconify()
        
        # Încărcăm conținutul paginii principale
        self.main_frame = MainPage(master=self, current_user=self.current_user)
        self.main_frame.pack(fill="both", expand=True)

        # Aplicăm patch-urile pe toată interfața principală
        self.apply_global_patches(self.main_frame)

if __name__ == "__main__":
    app = AppController()
    app.mainloop()