import pandas as pd
import os

class ExcelManager:
    @staticmethod
    def save_backup(data_dict, file_path):
        """Salvează datele curente într-un fișier Excel."""
        try:
            # Curățăm datele de obiecte care nu pot fi serializate
            cleaned_data = {}
            for k, v in data_dict.items():
                if isinstance(v, (str, int, float, bool)):
                    cleaned_data[k] = v
                elif v is None:
                    cleaned_data[k] = ""
                else:
                    # Liste sau dicționare (cum ar fi victimele) le salvăm ca string JSON
                    import json
                    cleaned_data[k] = json.dumps(v)

            df = pd.DataFrame([cleaned_data])
            df.to_excel(file_path, index=False, engine='openpyxl')
            return True, "Backup salvat cu succes."
        except Exception as e:
            return False, f"Eroare Excel: {str(e)}"