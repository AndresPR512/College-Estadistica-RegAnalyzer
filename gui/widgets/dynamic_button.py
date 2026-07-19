import customtkinter as ctk
import constants as c

# Botón personalizado que genera automáticamente sus colores normal y hover a partir de un único color base.
class DynamicButton(ctk.CTkButton):
    def __init__(self, master, image, text, color, font=c.FONTS["base_bold"], height=32, command=None, **kwargs):
        super().__init__(
            master,
            image=image,
            text=text,
            fg_color=self._oscurecer(color),
            hover_color=self._aclarar(color),
            text_color=c.COLORS["white"],
            font=font,
            corner_radius=5,
            height=height,
            command=command,
            **kwargs,
        )

    # Aumenta el brillo de un color hexadecimal.
    @staticmethod
    def _aclarar(color_hex: str) -> str:
        h = color_hex.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        factor = 1.15
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02X}{g:02X}{b:02X}"
    
    # Reduce el brillo de un color hexadecimal.
    @staticmethod
    def _oscurecer(color_hex: str) -> str:
        h = color_hex.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        factor = 0.80
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02X}{g:02X}{b:02X}"