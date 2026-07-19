import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# * ===== Gráfico de regresión =====
class RegressionChart:
    """
    Encapsula la figura de matplotlib, el canvas embebido en Tkinter
    y toda la lógica de dibujado del gráfico de regresión.
    """
    def __init__(self, parent, colors):
        self.colors = colors

        self.figure = Figure(figsize=(7, 4.5), dpi=100, facecolor=colors["secondary_bg"])
        self.ax = self.figure.add_subplot(111)
        self._style_axes()

        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()

    # * Aplica el estilo (colores, grid, spines) a los ejes del gráfico.
    def _style_axes(self):
        self.ax.set_facecolor(self.colors["secondary_bg"])
        self.ax.tick_params(colors="white")
        for spine in self.ax.spines.values():
            spine.set_color("#555555")
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")
        self.ax.title.set_color("white")
        self.ax.grid(True, alpha=0.2, color="gray", linestyle="--")

    # * Dibuja los puntos observados y la curva de regresión para la clave dada.
    def plot(self, x, y, result, key, regression_title, is_best):
        self.ax.clear()
        self._style_axes()
        
        if len(x) == 0 or len(y) == 0:
            return

        # Puntos originales
        self.ax.scatter(x, y, color=self.colors["coral_red"], s=80, zorder=5, edgecolors=self.colors["white"], linewidth=1.5, label="Datos observados")

        # Curva
        x_min, x_max = float(np.min(x)), float(np.max(x))
        margin = (x_max - x_min) * 0.08 if x_max > x_min else 1.0

        if key in ("Logarithmic", "Power"):
            start = max(1e-6, x_min - margin)
            x_curve = np.linspace(start, x_max + margin, 300)
        else:
            x_curve = np.linspace(x_min - margin, x_max + margin, 300)

        try:
            y_curve = result["curve"](x_curve)
            color = self.colors["green"] if is_best else self.colors["main_color"]
            label = f"{key} (R² = {result['r2']:.4f})"
            self.ax.plot(x_curve, y_curve, color=color, linewidth=2.5, label=label, zorder=4)
        except Exception:
            pass

        self.ax.set_xlabel("X", fontsize=12, fontweight="bold")
        self.ax.set_ylabel("Y", fontsize=12, fontweight="bold")

        title_color = "#00E676" if is_best else "#4FC3F7"
        prefix = "MEJOR:  " if is_best else ""
        self.ax.set_title(
            f"{prefix}Regresión {regression_title}",
            fontsize=14, color=title_color, fontweight="bold", pad=12
        )

        legend = self.ax.legend(loc="best", framealpha=0.9, fontsize=11)
        legend.get_frame().set_facecolor(self.colors["panel_bg"])
        legend.get_frame().set_edgecolor(self.colors["table_border"])
        for text in legend.get_texts():
            text.set_color("white")

        self.figure.tight_layout()
        self.canvas.draw()
    
    def clear(self):
        self.ax.clear()
        self._style_axes()
        self.canvas.draw()