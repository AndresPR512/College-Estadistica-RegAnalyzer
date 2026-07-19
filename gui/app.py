import os
import sys
import customtkinter as ctk
import constants as c
import util as u
import numpy as np
import random
from data.csv_manager import CSVManager
from logic.regression_engine import RegressionEngine
from gui.widgets.dynamic_button import DynamicButton
from gui.widgets.regression_chart import RegressionChart
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# * ===== Aplicación principal =====
class RegressionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RegAnalyzer")
        u.set_dimensions(self, 1280, 780)
        self.configure(fg_color=c.COLORS["main_bg"])
        icon_path = self.resource_path(os.path.join("assets", "icons", "reganalyzer_icon.ico"))
        self.iconbitmap(icon_path)

        self.csv_manager = CSVManager()
        self.regression_engine = RegressionEngine()
        self.regression_results = {}
        self.best_regression = None
        self.current_regression = None
        self.row_entries = []
        self.reg_buttons = {}
        self.reg_formula_images = {}
        self._equation_image_broken = False
        self.actual_random_key = random.choice(list(c.REGRESSIONS.keys()))
        self.x_data = None
        self.y_data = None

        self._build_ui()
        self.random_example()
    
    def resource_path(self, relative_path):
        # Funciona tanto en desarrollo como compilado con PyInstaller
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # Sube un nivel desde gui/ hasta la raíz del proyecto
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
        
    # * ------------------------------------ Construcción de la interfaz principal ------------------------------------
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, minsize=520)
        self.grid_rowconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    # * Construye el panel izquierdo con la tabla de datos y los botones de control.
    def _build_left_panel(self):
        left = ctk.CTkFrame(self, corner_radius=10, fg_color=c.COLORS["panel_bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left.grid_propagate(False)

        # Titulo y subtitulo
        title = ctk.CTkLabel(left, text=c.TEXTS["left_panel_title"], font=c.FONTS["H2"])
        title.pack(padx=10, pady=(20, 0))

        subtitle = ctk.CTkLabel(left, text=c.TEXTS["left_panel_subtitle"], font=c.FONTS["base"])
        subtitle.pack(padx=10, pady=(0, 10))

        # Tabla scrollable
        self.table_frame = ctk.CTkScrollableFrame(left, height=320, corner_radius=6, fg_color=c.COLORS["secondary_bg"], border_width=1, border_color=c.COLORS["table_border"])
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.table_frame.grid_columnconfigure(0, minsize=60, weight=0)
        self.table_frame.grid_columnconfigure((1, 2), weight=1, uniform="data_columns")
        self.table_frame.grid_columnconfigure(3, minsize=5, weight=0)
        
        self.table_frame.grid_rowconfigure(0, minsize=42)

        # Numero header
        number_header = ctk.CTkFrame(self.table_frame, fg_color=c.COLORS["table_header"], corner_radius=0, border_width=1, border_color=c.COLORS["table_border"])
        number_header.grid(row=0, column=0, sticky="nsew")

        number_title = ctk.CTkLabel(number_header, text="#", font=c.FONTS["H4"], text_color=c.COLORS["table_text"], fg_color="transparent")
        number_title.pack(fill="both", expand=True, padx=2, pady=2)

        # X header
        x_header = ctk.CTkFrame(self.table_frame, fg_color=c.COLORS["table_header"], corner_radius=0, border_width=1, border_color=c.COLORS["table_border"])
        x_header.grid(row=0, column=1, sticky="nsew")

        x_title = ctk.CTkLabel(x_header, text="X", font=c.FONTS["H4"], text_color=c.COLORS["table_text"], fg_color="transparent")
        x_title.pack(fill="both", expand=True, padx=2, pady=2)

        # Y header
        y_header = ctk.CTkFrame(self.table_frame, fg_color=c.COLORS["table_header"], corner_radius=0, border_width=1, border_color=c.COLORS["table_border"])
        y_header.grid(row=0, column=2, sticky="nsew")

        y_title = ctk.CTkLabel(y_header, text="Y", font=c.FONTS["H4"], text_color=c.COLORS["table_text"], fg_color="transparent")
        y_title.pack(fill="both", expand=True, padx=2, pady=2)

        # Botones de manejo de filas
        btn_row = ctk.CTkFrame(left, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 5))
        btn_row.grid_columnconfigure((0, 1), weight=1)
        btn_row.grid_rowconfigure((0, 1), weight=1)
        
        add_row_btn = DynamicButton(btn_row, image=u.Resources.icon("add.png"), text="Agregar Fila", color=c.COLORS["dark_green"], command=self.add_row)
        add_row_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 5))
        remove_row_btn = DynamicButton(btn_row, image=u.Resources.icon("erase.png"), text="Eliminar Fila", color=c.COLORS["red"], command=self.remove_row)
        remove_row_btn.grid(row=0, column=1, sticky="nsew", pady=(0, 5))
        random_example_btn = DynamicButton(btn_row, image=u.Resources.icon("random.png"), text="Ejemplo", color=c.COLORS["violet"], command=self.random_example)
        random_example_btn.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        clear_all_btn = DynamicButton(btn_row, image=u.Resources.icon("delete.png"), text="Limpiar Todo", color=c.COLORS["gray"], command=self.clear_all)
        clear_all_btn.grid(row=1, column=1, sticky="nsew")

        # Importar / Exportar
        io_row = ctk.CTkFrame(left, fg_color="transparent")
        io_row.pack(fill="x", padx=10, pady=(0, 15))
        io_row.grid_columnconfigure((0, 1), weight=1)
        
        import_btn = DynamicButton(io_row, image=u.Resources.icon("import.png"), text="Importar CSV", color=c.COLORS["blue"], height=40, command=self.load_csv)
        import_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        export_btn = DynamicButton(io_row, image=u.Resources.icon("export.png"), text="Exportar CSV", color=c.COLORS["blue"], height=40, command=self.save_csv)
        export_btn.grid(row=0, column=1, sticky="nsew")

        # Boton para calcular la regresion
        calc_btn = DynamicButton(left, image=u.Resources.icon("calculate.png", size=(20, 20)), text="Calcular Regresión", color=c.COLORS["main_color"], font=c.FONTS["H4"], height=46, command=self.calculate_all)
        calc_btn.pack(fill="x", padx=10, pady=(0, 10))

    # * Construye el panel derecho con el selector de regresion, resultados y grafico.
    def _build_right_panel(self):
        right = ctk.CTkFrame(self, corner_radius=10, fg_color=c.COLORS["panel_bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        # Selector de tipo de regresion
        selector_container = ctk.CTkFrame(right, corner_radius=6, fg_color=c.COLORS["secondary_bg"], border_width=1, border_color=c.COLORS["table_border"])
        selector_container.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        selector_title = ctk.CTkLabel(selector_container, text="Tipo de Regresión", font=c.FONTS["H4"])
        selector_title.pack(anchor="w", padx=10, pady=(10, 0))

        selector_frame = ctk.CTkFrame(selector_container, fg_color="transparent")
        selector_frame.pack(fill="x", padx=5, pady=(0, 5))

        for regression_key, regression_data in c.REGRESSIONS.items():
            btn = ctk.CTkButton(selector_frame, text=regression_data["title"],
                                command=lambda key=regression_key: self.show_regression(key),
                                fg_color=c.COLORS["panel_bg"], hover_color=c.COLORS["input_bg"],
                                border_width=2, border_color=c.COLORS["table_border"],
                                font=c.FONTS["base_bold"], text_color="white", height=32)
            btn.pack(side="left", padx=5, pady=(0, 8), expand=True, fill="x")

            self.reg_buttons[regression_key] = btn

        # Panel de resultados
        self.results_frame = ctk.CTkFrame(right, corner_radius=6, fg_color=c.COLORS["secondary_bg"], border_width=1, border_color=c.COLORS["table_border"])
        self.results_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.best_label = ctk.CTkLabel(self.results_frame, text=c.TEXTS["main_panel_instructions"], font=c.FONTS["H3"], text_color="white", justify="center")
        self.best_label.pack(padx=10, pady=(20, 5))
        
        equation_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        equation_frame.pack(padx=10, pady=(0, 5))

        equation_title = ctk.CTkLabel(equation_frame, text="Ecuación:", font=c.FONTS["H4"], text_color=c.COLORS["main_color"], height=36)
        equation_title.pack(side="left", padx=(0, 10))

        self.equation_label = ctk.CTkLabel(equation_frame, text="", height=36)
        self.equation_label.pack(side="left")

        # Contenedor para los valores de a, b, c y r
        self.vals_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.vals_frame.pack(fill="x", padx=10, pady=0)
        self.vals_frame.grid_columnconfigure((0, 1, 3), weight=1)

        self.a_label = ctk.CTkLabel(self.vals_frame, text="a: -", font=c.FONTS["base"])
        self.a_label.grid(row=0, column=0, sticky="ew", padx=10, )

        self.b_label = ctk.CTkLabel(self.vals_frame, text="b: -", font=c.FONTS["base"])
        self.b_label.grid(row=0, column=1, sticky="ew", padx=10)

        self.c_label = ctk.CTkLabel(self.vals_frame, text="", font=c.FONTS["base"])
        self.c_label.grid(row=0, column=2, sticky="ew", padx=10)
        self.c_label.grid_remove()

        self.r_label = ctk.CTkLabel(self.vals_frame, text="r: -", font=c.FONTS["base"])
        self.r_label.grid(row=0, column=3, sticky="ew", padx=10)
        
        # Contenedor para los coeficientes de determinación y error
        metrics_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=10, pady=(0, 10))
        metrics_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.r2_label = ctk.CTkLabel(metrics_frame, text="R²: -", font=c.FONTS["base_bold"], text_color=c.COLORS["green"])
        self.r2_label.grid(row=0, column=0, sticky="ew", padx=10)

        self.adjusted_r2_label = ctk.CTkLabel(metrics_frame, text="R² ajustado: -", font=c.FONTS["base_bold"], text_color=c.COLORS["green"])
        self.adjusted_r2_label.grid(row=0, column=1, sticky="ew", padx=10)

        self.standard_error_label = ctk.CTkLabel(metrics_frame, text="Error estándar: -", font=c.FONTS["base_bold"], text_color=c.COLORS["green"])
        self.standard_error_label.grid(row=0, column=2, sticky="ew", padx=10)

        self.press_label = ctk.CTkLabel(metrics_frame, text="PRESS: -", font=c.FONTS["base_bold"], text_color=c.COLORS["green"])
        self.press_label.grid(row=0, column=3, sticky="ew", padx=10)

        self.predicted_r2_label = ctk.CTkLabel(metrics_frame, text="R² predictivo: -", font=c.FONTS["base_bold"], text_color=c.COLORS["green"])
        self.predicted_r2_label.grid(row=0, column=4, sticky="ew", padx=10)
        
        # Fila de predicción
        pred_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        pred_frame.pack(fill="x", padx=25, pady=(0, 10))
        
        # Predecir Y a partir de X
        pred_y_frame = ctk.CTkFrame(pred_frame, fg_color="transparent")
        pred_y_frame.pack(fill="x", pady=(0, 10))

        pred_y_label = ctk.CTkLabel(pred_y_frame, text=c.TEXTS["predict_y"], font=c.FONTS["base"], text_color=c.COLORS["white"], height=30)
        pred_y_label.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.pred_y_entry = ctk.CTkEntry(pred_y_frame, width=160, height=30, fg_color=c.COLORS["panel_bg"], border_color=c.COLORS["table_border"], font=c.FONTS["base"])
        self.pred_y_entry.grid(row=0, column=1, padx=5)

        pred_y_btn = DynamicButton(pred_y_frame, image=u.Resources.icon("calculator.png"), text="Calcular", color=c.COLORS["main_color_darker"], command=self.predict_y)
        pred_y_btn.grid(row=0, column=2, padx=5)

        self.pred_y_result = ctk.CTkLabel(pred_y_frame, text="", font=c.FONTS["large_bold"], height=30)
        self.pred_y_result.grid(row=0, column=3, padx=(5, 0))

        # Predecir X a partir de Y
        pred_x_frame = ctk.CTkFrame(pred_frame, fg_color="transparent")
        pred_x_frame.pack(fill="x")
        
        pred_x_label = ctk.CTkLabel(pred_x_frame, text=c.TEXTS["predict_x"], font=c.FONTS["base"], text_color=c.COLORS["white"], height=30)
        pred_x_label.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.pred_x_entry = ctk.CTkEntry(pred_x_frame, width=160, height=30, fg_color=c.COLORS["panel_bg"], border_color=c.COLORS["table_border"], font=c.FONTS["base"])
        self.pred_x_entry.grid(row=0, column=1, padx=5)

        pred_x_btn = DynamicButton(pred_x_frame, image=u.Resources.icon("calculator.png"), text="Calcular", color=c.COLORS["main_color_darker"], command=self.predict_x)
        pred_x_btn.grid(row=0, column=2, padx=5)

        self.pred_x_result = ctk.CTkLabel(pred_x_frame, text="", font=c.FONTS["large_bold"], height=30)
        self.pred_x_result.grid(row=0, column=3, padx=(5, 0))

        # Area del grafico
        self.graph_frame = ctk.CTkFrame(right, corner_radius=6, fg_color=c.COLORS["secondary_bg"], border_width=1, border_color=c.COLORS["table_border"])
        self.graph_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.chart = RegressionChart(self.graph_frame, c.COLORS)

    # * ------------------------------------ Manejo de filas de la tabla y botones ------------------------------------
    # * Añadir fila vacía
    def add_row(self):
        row_index = len(self.row_entries) + 1

        if row_index % 2 == 0:
            row_background = c.COLORS["table_alternate_row"]
        else:
            row_background = c.COLORS["table_row"]

        self.table_frame.grid_rowconfigure(row_index, minsize=40)

        # Celda para número de índice
        number_cell = ctk.CTkFrame(self.table_frame, fg_color=row_background, corner_radius=0, border_width=1, border_color=c.COLORS["table_border"])
        number_cell.grid(row=row_index, column=0, sticky="nsew")

        number_label = ctk.CTkLabel(number_cell, text=str(row_index), font=c.FONTS["base_bold"], text_color=c.COLORS["table_secondary_text"], fg_color="transparent")
        number_label.pack(fill="both", expand=True, padx=2, pady=2)

        # Celda para valor X
        x_cell = ctk.CTkFrame(self.table_frame, fg_color=row_background, corner_radius=0, border_width=1, border_color=c.COLORS["table_border"])
        x_cell.grid(row=row_index, column=1, sticky="nsew")

        x_variable = ctk.StringVar()

        x_entry = ctk.CTkEntry(x_cell, textvariable=x_variable, justify="center", font=c.FONTS["base"], text_color=c.COLORS["table_text"], fg_color=row_background, border_width=0, corner_radius=0)
        x_entry.pack(fill="both", expand=True, padx=2, pady=2)

        x_variable.trace_add("write", lambda *args, entry=x_entry, cell=x_cell: self._validate_numeric_entry(entry, cell))

        # Celda para valor Y
        y_cell = ctk.CTkFrame(self.table_frame, fg_color=row_background, corner_radius=0, border_width=1, border_color=c.COLORS["table_border"])
        y_cell.grid(row=row_index, column=2, sticky="nsew")

        y_variable = ctk.StringVar()

        y_entry = ctk.CTkEntry(y_cell, textvariable=y_variable, justify="center", font=c.FONTS["base"], text_color=c.COLORS["table_text"], fg_color=row_background, border_width=0, corner_radius=0)
        y_entry.pack(fill="both", expand=True, padx=2, pady=2)

        y_variable.trace_add("write", lambda *args, entry=y_entry, cell=y_cell: self._validate_numeric_entry(entry, cell))

        self.row_entries.append({"number_cell": number_cell, "x_cell": x_cell, "y_cell": y_cell, "number": number_label, "x": x_entry, "y": y_entry})

    # * Eliminar última fila
    def remove_row(self):
        if len(self.row_entries) > 2:
            row = self.row_entries.pop()
            for cell_name in ["number_cell", "x_cell", "y_cell"]:
                row[cell_name].destroy()

    # * Eliminar filas adicionales dejando solo las mínimas requeridas
    def remove_aditional_rows(self, min_rows):
        while len(self.row_entries) > min_rows:
            row = self.row_entries.pop()
            for cell_name in ["number_cell", "x_cell", "y_cell"]:
                row[cell_name].destroy()

    # * Limpiar todos los datos y resultados, dejando la tabla vacía.
    def clear_all(self, min_rows=4):
        self.remove_aditional_rows(min_rows)
        for row in self.row_entries:
            row["x"].delete(0, "end")
            row["y"].delete(0, "end")
        self.regression_results = {}
        self.best_regression = None
        self.current_regression = None
        self._reset_display()
        self.x_data = None
        self.y_data = None
    
    # * Carga un conjunto de datos de ejemplo aleatorio al iniciar la aplicación.
    def random_example(self):
        self.remove_aditional_rows(0)
        
        while True:
            random_key = random.choice(list(c.REGRESSIONS.keys()))
            if random_key != self.actual_random_key:
                break
        self.actual_random_key = random_key
        
        data = c.REGRESSIONS[random_key]
        for xv, yv in zip(data["example_x"], data["example_y"]):
            self.add_row()
            self.row_entries[-1]["x"].insert(0, str(xv))
            self.row_entries[-1]["y"].insert(0, str(yv))

    # * Reinicia los resultados y el grafico a su estado inicial.
    def _reset_display(self):
        self.best_label.configure(text=c.TEXTS["main_panel_instructions"], text_color="white")
        self._clear_equation_image("-")
        self.reg_formula_images.clear()
        self.a_label.configure(text="a: -")
        self.b_label.configure(text="b: -")
        self.c_label.configure(text="")
        self.c_label.grid_remove()
        self.r_label.configure(text="r: -")
        self.r2_label.configure(text="R²: -")
        self.adjusted_r2_label.configure(text="R² ajustado: -")
        self.standard_error_label.configure(text="Error estándar: -")
        self.press_label.configure(text="PRESS: -")
        self.predicted_r2_label.configure(text="R² predictivo: -")
        self.pred_y_result.configure(text="")
        self.pred_x_result.configure(text="")
        for btn in self.reg_buttons.values():
            btn.configure(fg_color=c.COLORS["panel_bg"], border_color=c.COLORS["table_border"], text_color="white", state="normal")
        self.chart.clear()
        
    def _clear_equation_image(self, text=""):
        try:
            # Elimina la imagen del Label interno de Tkinter
            self.equation_label._label.configure(image="")
            # Elimina la referencia interna de CustomTkinter
            self.equation_label.configure(image=None)
            # Ahora se puede modificar el texto sin provocar el error
            self.equation_label.configure(text=text)
        except Exception:
            # Respaldo por si en el futuro cambia la estructura interna de CustomTkinter
            self.equation_label.configure(text=text, image=None)

    # * ------------------------------------ Obtención de datos de entrada ------------------------------------
    def get_data(self):
        xs, ys = [], []
        for row in self.row_entries:
            x_val = row["x"].get().strip().replace(",", ".")
            y_val = row["y"].get().strip().replace(",", ".")
            if x_val and y_val:
                try:
                    xs.append(float(x_val))
                    ys.append(float(y_val))
                except ValueError:
                    raise ValueError(f"Valor no numérico: X='{x_val}', Y='{y_val}'")
        return np.array(xs), np.array(ys)
    
    def _validate_numeric_entry(self, entry, cell):
        value = entry.get().strip().replace(",", ".")
        if value == "":
            cell.configure(border_color=c.COLORS["table_border"])
            return

        try:
            number = float(value)
            is_valid = np.isfinite(number)
        except ValueError:
            is_valid = False

        if is_valid:
            cell.configure(border_color=c.COLORS["table_border"])
        else:
            cell.configure(border_color=c.COLORS["red"])

    # * ------------------------------------ Cálculo de las regresiones ------------------------------------
    def calculate_all(self):
        try:
            x, y = self.get_data()
        except ValueError as e:
            messagebox.showerror("Error en los datos.", str(e))
            return

        if len(x) < 4:
            messagebox.showwarning("Datos insuficientes.", "Necesitas al menos 4 puntos de datos.")
            return

        self.x_data = x
        self.y_data = y
        
        self.regression_results = self.regression_engine.fit_all(x, y)
        # Desvincular primero la imagen del label
        self._clear_equation_image()
        # Ahora se pueden destruir las imágenes anteriores
        self.reg_formula_images.clear()

        if not self.regression_results:
            messagebox.showerror("Error.", "No se pudo calcular ninguna regresión con estos datos.")
            return

        self.best_regression = max(self.regression_results.items(), key=lambda item: item[1]["predicted_r2"])[0]

        for name, btn in self.reg_buttons.items():
            if name in self.regression_results:
                btn.configure(fg_color=c.COLORS["panel_bg"], border_color=c.COLORS["table_border"], text_color="white", state="normal")
            else:
                btn.configure(fg_color=c.COLORS["secondary_bg"], border_color=c.COLORS["table_border"], text_color="gray", state="disabled")

        self.show_regression(self.best_regression)

    # * ------------------------------------ Actualizar panel según regresión ------------------------------------
    def show_regression(self, key):
        if key not in self.regression_results:
            return

        self.current_regression = key
        result = self.regression_results[key]
        regression_title = c.REGRESSIONS[key]["title"]

        # Colores de los botones según su estado
        for button_key, button in self.reg_buttons.items():
            if button_key not in self.regression_results:
                continue
            if button_key == key and button_key == self.best_regression:
                button.configure(fg_color="#00A86B", border_color="#00E676", text_color="white")
            elif button_key == key:
                button.configure(fg_color="#1F6AA5", border_color="#4FC3F7", text_color="white")
            elif button_key == self.best_regression:
                button.configure(fg_color=c.COLORS["panel_bg"], border_color="#00E676", text_color="#00E676")
            else:
                button.configure(fg_color=c.COLORS["panel_bg"], border_color=c.COLORS["table_border"], text_color="white")

        # Encabezado
        if key == self.best_regression:
            self.best_label.configure(text=f"Mejor ajuste: Regresión {regression_title} | R² = {result['r2']:.4f}", text_color="#00E676")
        else:
            self.best_label.configure(text=f"Mostrando: Regresión {regression_title} | R² = {result['r2']:.4f}", text_color="white")

        self._update_equation_display(key, result["equation"])
        self.a_label.configure(text=f"a = {result['a']:.4f}")
        self.b_label.configure(text=f"b = {result['b']:.4f}")
        # Si es cuadrática, muestra el valor c
        if key == "Quadratic":
            self.c_label.configure(text=f"c = {result['c']:.4f}")
            self.c_label.grid()
            self.vals_frame.grid_columnconfigure(2, weight=1)
        else:
            self.c_label.configure(text="")
            self.c_label.grid_remove()
            self.vals_frame.grid_columnconfigure(2, weight=0)

        # Muestra el resto de valores
        self.r_label.configure(text=f"r = {result['r']:.4f}")
        self.r2_label.configure(text=f"R² = {result['r2']:.4f}")
        self.adjusted_r2_label.configure(text=f"R² ajustado = {result['adjusted_r2']:.4f}")
        self.standard_error_label.configure(text=f"Error estándar = {result['standard_error']:.4f}")
        self.press_label.configure(text=f"PRESS = {result['press']:.4f}")
        self.predicted_r2_label.configure(text=f"R² predictivo = {result['predicted_r2']:.4f}")

        self._plot_regression(key)

    def _plot_regression(self, key):
        x, y = self.x_data, self.y_data
        result = self.regression_results[key]
        regression_title = c.REGRESSIONS[key]["title"]

        self.chart.plot(x, y, result, key, regression_title, key == self.best_regression)
    
    def _update_equation_display(self, key, equation):
        if self._equation_image_broken:
            self.equation_label.configure(text=u.latex_to_plain(equation), image=None)
            return
 
        try:
            if key not in self.reg_formula_images:
                self.reg_formula_images[key] = u.create_latex_image(equation)
            formula_image = self.reg_formula_images[key]
            self.equation_label.configure(image=formula_image)
            self.equation_label.configure(text="")
        except Exception:
            self._equation_image_broken = True
            self.reg_formula_images.clear()
            self.equation_label.configure(text=u.latex_to_plain(equation), image=None)

    # * ------------------------------------ Métodos para realizar las predicciones ------------------------------------
    def _get_prediction_value(self, entry, variable_name):
        value = entry.get().strip().replace(",", ".")
        if not value:
            return None
        
        try:
            number = float(value)
            if not np.isfinite(number):
                raise ValueError
            return number
        except ValueError:
            messagebox.showerror("Valor inválido", f"Ingresa un valor numérico válido para {variable_name}.")
            return None
    
    def predict_y(self):
        if not self.current_regression:
            messagebox.showinfo("Información", "Primero calcula una regresión.")
            return

        x_value = self._get_prediction_value(self.pred_y_entry, "X")
        if x_value is None:
            return

        if self.current_regression in ("Logarithmic", "Power") and x_value <= 0:
            messagebox.showwarning("Dominio inválido", "Para esta regresión, X debe ser mayor que 0.")
            return

        result = self.regression_results[self.current_regression]

        try:
            y_prediction = float(result["predict_y"](x_value))
            if not np.isfinite(y_prediction):
                raise ValueError("El resultado no es un número finito.")
            self.pred_y_result.configure(text=f"Y = {y_prediction:.4f}", text_color=c.COLORS["main_color"])
        except (ValueError, OverflowError, FloatingPointError) as error:
            messagebox.showerror("Error de predicción", str(error))
    
    def predict_x(self):
        if not self.current_regression:
            messagebox.showinfo("Información", "Primero calcula una regresión.")
            return

        y_value = self._get_prediction_value(self.pred_x_entry, "Y")
        if y_value is None:
            return

        if self.current_regression in ("Exponential", "Power") and y_value <= 0:
            messagebox.showwarning("Dominio inválido", "Para esta regresión, Y debe ser mayor que 0.")
            return

        result = self.regression_results[self.current_regression]

        try:
            x_prediction = result["predict_x"](y_value)

            # La cuadrática puede devolver dos soluciones.
            if isinstance(x_prediction, tuple):
                x1 = float(x_prediction[0])
                x2 = float(x_prediction[1])
                if not np.isfinite(x1) or not np.isfinite(x2):
                    raise ValueError("Las soluciones obtenidas no son números finitos.")
                if np.isclose(x1, x2, atol=1e-8):
                    result_text = f"X = {x1:.4f}"
                else:
                    result_text = f"X₁ = {x1:.4f} | X₂ = {x2:.4f}"
            else:
                x_prediction = float(x_prediction)
                if not np.isfinite(x_prediction):
                    raise ValueError("El resultado no es un número finito.")
                result_text = f"X = {x_prediction:.4f}"

            self.pred_x_result.configure(text=result_text, text_color=c.COLORS["main_color"])
        except (ValueError, OverflowError, FloatingPointError) as error:
            messagebox.showerror("Error de predicción", str(error))
    
    # * ------------------------------------ Métodos para cargar / guardar csv ------------------------------------
    def load_csv(self):
        data = self.csv_manager.load(parent=self)
        if not data:
            return  # None (error/cancelado) o lista vacia (sin pares validos)
 
        self.clear_all(0)
 
        for xv, yv in data:
            self.add_row()
            self.row_entries[-1]["x"].insert(0, str(xv))
            self.row_entries[-1]["y"].insert(0, str(yv))
 
    def save_csv(self):
        try:
            x, y = self.get_data()
        except ValueError as e:
            messagebox.showerror("Error en los datos", str(e))
            return
        self.csv_manager.save(x, y, parent=self)