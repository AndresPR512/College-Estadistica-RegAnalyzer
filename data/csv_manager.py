import csv
from tkinter import filedialog, messagebox

class CSVManager:
    @staticmethod
    def load(parent=None):
        path = filedialog.askopenfilename(
            title="Cargar datos desde CSV",
            filetypes=[("CSV files", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not path:
            return None

        try:
            data = []
            
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                
                for row in reader:
                    if len(row) >= 2:
                        try:
                            x_val = row[0].strip().replace(",", ".")
                            y_val = row[1].strip().replace(",", ".")
                            data.append((float(x_val), float(y_val)))
                        except ValueError:
                            continue
            
            if not data:
                messagebox.showwarning("Vacio", "No se encontraron pares numericos.")
                return []
            
            messagebox.showinfo("Listo", f"Se cargaron {len(data)} puntos.")
            return data

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
            return None

    @staticmethod
    def save(x, y, parent=None):
        if len(x) == 0:
            messagebox.showwarning("Vacio", "No hay datos para guardar.")
            return False

        path = filedialog.asksaveasfilename(
            title="Guardar datos como CSV", defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return False

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["X", "Y"])
                for xv, yv in zip(x, y):
                    writer.writerow([xv, yv])
            messagebox.showinfo("Listo", "Datos guardados correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False