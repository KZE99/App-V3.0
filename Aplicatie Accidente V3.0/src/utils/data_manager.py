import json
import os
import socket
import pandas as pd
from datetime import datetime

# --- CONFIGURĂRI CĂI ---
# Folderul de backup în profilul utilizatorului (conform BARSV V3.2)
BASE_BACKUP_DIR = os.path.join(os.path.expanduser("~"), "BARSV APP Backup")
SETTINGS_FILE = os.path.join(BASE_BACKUP_DIR, "settings.json")
DATA_DIR = "data"
LOGIN_FILE = os.path.join(DATA_DIR, "login_data.json")

# --- SECURITATE (LISTĂ STAȚII AUTORIZATE) ---
ALLOWED_HOSTNAMES = [
    'DESKTOP-7H7ELRD', 'DESKTOP-1NNK2DH', 'DESKTOP-2JSKFMS', 
    'PC-B1-BR-039', 'PC-B1-BR-040', 'PC-B1-BR041', 'PC-B1-BR042', 
    'PC-B1-BR043', 'PC-B1-BR044', 'PC-B1-BR045', 'PC-B1-BR046', 
    'PC-B1-BR047', 'PC-B1-BR048', 'PC-B1-BR049', 'PC-B1-BR050', 
    'PC-B1-BR051', 'PC-B1-BR052', 'DESKTOP-GICB227'
]

def check_security():
    """Verifică dacă stația de lucru este autorizată."""
    try:
        hostname = socket.gethostname()
        return hostname in ALLOWED_HOSTNAMES
    except Exception:
        return False

# --- GESTIONARE LOGIN (PENTRU LOGIN_WINDOW.PY) ---
def save_login_data(username):
    """Salvează numele de utilizator întrun fișier JSON."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        data_to_save = {"last_username": username}
        with open(LOGIN_FILE, "w", encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)
        return True
    except Exception as e:
        print(f"Eroare la salvarea datelor de login: {e}")
        return False

def load_login_data():
    """Încarcă numele de utilizator salvat."""
    if not os.path.exists(LOGIN_FILE):
        return None
    try:
        with open(LOGIN_FILE, "r", encoding='utf-8') as f:
            data = json.load(f)
            return data.get("last_username")
    except Exception:
        return None

def clear_login_data():
    """Șterge fișierul cu datele de login."""
    if os.path.exists(LOGIN_FILE):
        try:
            os.remove(LOGIN_FILE)
            return True
        except Exception as e:
            print(f"Eroare la ștergerea datelor de login: {e}")
            return False
    return True

# --- SETĂRI GLOBALE ---
def load_settings():
    """Încarcă setările (agenți, contravenții, șefi)."""
    defaults = {
        'nume_agent1': '',
        'insigna_agent1': '',
        'lista_agent2': [],
        'lista_sef_tura': [],
        'lista_contraventii': ['', 'Art. 48', 'Art. 54/1', 'Art. 336/1'],
        'titulatura_sef_br': 'Î/ŞEFUL BRIGĂZII RUTIERE',
        'grad_sef_br': 'Comisar-șef de poliție',
        'nume_sef_br': 'VLĂȘCEANU IONUȚ'
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                defaults.update(data)
                return defaults
        except Exception:
            pass
    return defaults

def save_settings(settings_dict):
    """Salvează setările în JSON."""
    try:
        os.makedirs(BASE_BACKUP_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=4)
        return True
    except Exception as e:
        print(f"Eroare salvare setări: {e}")
        return False

# --- BACKUP EXCEL ---
def save_excel_backup(data_dict):
    """Salvează datele curente în format Excel .xlsx."""
    try:
        os.makedirs(BASE_BACKUP_DIR, exist_ok=True)
        nr_penal = data_dict.get("numar_lucrare", "fara_numar")
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
        file_path = os.path.join(BASE_BACKUP_DIR, f"Backup_{nr_penal}_{timestamp}.xlsx")

        # Curățăm datele pentru DataFrame
        cleaned = {k: str(v) for k, v in data_dict.items() if not isinstance(v, (list, dict))}
        
        df = pd.DataFrame([cleaned])
        df.to_excel(file_path, index=False, engine='openpyxl')
        return True, file_path
    except Exception as e:
        return False, str(e)