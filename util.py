import customtkinter as ctk
import matplotlib as mpl
import constants as c
import re
from pathlib import Path
from PIL import Image
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Función para centrar una ventana en la pantalla y establecer sus dimensiones mínimas.
def set_dimensions(ventana, ancho, alto):
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.minsize(ancho, alto)

# Renderiza una imagen LaTeX para mostrar la ecuación
def render_latex(expression, text_color=c.COLORS["main_color"], font_size=16, dpi=200, font_set="dejavusans"):
    if not expression.startswith("$"):
        expression = f"${expression}$"

    with mpl.rc_context({"mathtext.fontset": font_set}):
        figure = Figure(figsize=(0.01, 0.01), dpi=dpi)
        figure.patch.set_alpha(0)

        figure.text(0.5, 0.5, expression, fontsize=font_size, color=text_color, horizontalalignment="center", verticalalignment="center")

        canvas = FigureCanvasAgg(figure)
        canvas.draw()

        buffer = BytesIO()
        figure.savefig(buffer, format="png", transparent=True, bbox_inches="tight", pad_inches=0.02)
        buffer.seek(0)

        original_image = Image.open(buffer).convert("RGBA")
        original_image.load()

        image = original_image.copy()

        original_image.close()
        buffer.close()
        figure.clear()

        return image

# Crea la imagen LaTeX para la ecuación
def create_latex_image(expression, font_size=14, light_color="#151515", dark_color="#FFFFFF", scale=2, font_set="cm"):
    light_image = render_latex(expression, light_color, font_size, font_set=font_set)
    dark_image = render_latex(expression, dark_color, font_size, font_set=font_set)

    display_width = max(1, dark_image.width // scale)
    display_height = max(1, dark_image.height // scale)

    return ctk.CTkImage(light_image=light_image, dark_image=dark_image, size=(display_width, display_height))

# Convierte una expresión LaTeX simple (como las usadas en las ecuaciones de regresión)
# a texto plano legible, usando caracteres unicode para exponentes enteros y
# formato "^(...)" para exponentes decimales o con variables.
# Se usa como respaldo cuando el renderizado de la imagen LaTeX falla.
_SUPERSCRIPT_MAP = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
}
 
_LATEX_REPLACEMENTS = {
    r"\cdot": "·",
    r"\times": "×",
    r"\left": "",
    r"\right": "",
    r"\ln": "ln",
    r"\log": "log",
    r"\sqrt": "√",
    r"\pm": "±",
    r"\,": " ",
    r"\;": " ",
    r"\!": "",
}
 
def latex_to_plain(expression):
    text = expression.strip()
    if text.startswith("$") and text.endswith("$"):
        text = text[1:-1]
 
    def _format_exponent(content):
        if re.fullmatch(r"[0-9]+", content):
            return "".join(_SUPERSCRIPT_MAP[ch] for ch in content)
        return f"^({content})"
 
    # Exponentes entre llaves: ^{0.5678x}, ^{2}, etc
    text = re.sub(r"\^\{([^}]*)\}", lambda m: _format_exponent(m.group(1)), text)
    # Exponentes de un solo caracter sin llaves: ^2, ^x, etc
    text = re.sub(r"\^([0-9A-Za-z])", lambda m: _format_exponent(m.group(1)), text)
 
    for old, new in _LATEX_REPLACEMENTS.items():
        text = text.replace(old, new)
 
    # Espacio antes de "ln(" o "e^(" cuando quedan pegados a un número
    text = re.sub(r"(\d)(ln\()", r"\1 \2", text)
    text = re.sub(r"(\d)(e\^)", r"\1 \2", text)
 
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Clase Resources para manejar e insertar los iconos
class Resources:
    BASE_DIR = Path(__file__).resolve().parent
    ICONS_DIR = BASE_DIR / "assets" / "icons"
    @staticmethod
    def icon(name, size=(16, 16)):
        ruta = Resources.ICONS_DIR / name
        return ctk.CTkImage(light_image=Image.open(ruta),size=size)