from docxtpl import DocxTemplate
import os

class DocGenerator:
    @staticmethod
    def generate_report(data, template_path, output_path):
        """
        Generează un document Word folosind un template și un dicționar de date.
        """
        try:
            # Încărcăm template-ul
            doc = DocxTemplate(template_path)
            
            # Randăm datele în template
            doc.render(data)
            
            # Salvăm rezultatul
            doc.save(output_path)
            return True, f"Document generat cu succes: {output_path}"
        except Exception as e:
            return False, f"Eroare la generarea documentului: {str(e)}"