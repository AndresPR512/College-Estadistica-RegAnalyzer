FONTS = {
    "H1": ("Inter", 24, "bold"),
    "H2": ("Inter", 20, "bold"),
    "H3": ("Inter", 16, "bold"),
    "H4": ("Inter", 14, "bold"),
    "lg": ("Inter", 14),
    "large_bold": ("Inter", 14, "bold"),
    "base": ("Inter", 12),
    "base_bold": ("Inter", 12, "bold"),
    "sm": ("Inter", 12),
    "caption": ("Inter", 10),
}

TEXTS = {
    "main_app_title": "RegAnalyzer",
    "main_app_subtitle": "Analizador de Regresiones",
    "left_panel_title": "Datos de Entrada",
    "left_panel_subtitle": "Ingresa los pares (X, Y)",
    "main_panel_instructions": "Ingresa los datos en la tabla y presiona 'Calcular Regresión'.",
    "predict_y": "Predecir Y a partir de X = ",
    "predict_x": "Predecir X a partir de Y = ",
}

COLORS = {
    "main_color": "#1BBBFF",
    "main_color_darker": "#118CC1",
    
    # - BACKGROUNDS -
    "main_bg": "#000000",
    "secondary_bg": "#060615",
    "panel_bg": "#0F0F28",
    "input_bg": "#12122E",

    # - TABLE -
    "table_header": "#1B1B42",
    "table_row": "#12122E",
    "table_alternate_row": "#161635",
    "table_border": "#30305A",
    "table_text": "#F2F2F7",
    "table_secondary_text": "#B8B8D0",
    
    # - BASIC -
    "white": "#FFFFFF",
    "gray": "#3D3D3D",
    "dark_green": "#194E2D",
    "green": "#24C752",
    "light_green": "#00E676",
    "red": "#802234",
    "coral_red": "#FF6B6B",
    "blue": "#194D85",
    "violet": "#813784",
}

REGRESSIONS = {
    "Linear": {
        "title": "Lineal",
        "formula": r"$y = a + bx$",
        "example_x": [1, 3, 6, 10, 15, 21],
        "example_y": [5, 11, 20, 32, 47, 65],
    },

    "Exponential": {
        "title": "Exponencial",
        "formula": r"$y = ae^{bx}$",
        "example_x": [0, 1, 2, 3, 4, 5],
        "example_y": [3.00, 4.95, 8.15, 13.45, 22.17, 36.55],
    },

    "Logarithmic": {
        "title": "Logarítmica",
        "formula": r"$y = a + b\ln(x)$",
        "example_x": [1, 2, 4, 8, 16, 32],
        "example_y": [2.00, 4.08, 6.16, 8.24, 10.32, 12.40],
    },

    "Quadratic": {
        "title": "Cuadrática",
        "formula": r"$y = a + bx + cx^2$",
        "example_x": [0, 1, 2, 3, 4, 5],
        "example_y": [2.0, 5.5, 13.0, 24.5, 40.0, 59.5],
    },

    "Power": {
        "title": "Potencial",
        "formula": r"$y = ax^b$",
        "example_x": [1, 2, 3, 5, 8, 12],
        "example_y": [2, 8, 18, 50, 128, 288],
    },
}