# RegAnalyzer

A desktop application for regression analysis and curve fitting, built with Python and customtkinter.

## Features

- Curve fitting from user-provided data
- Coefficient of determination (R²) calculation
- Graphical visualization of data points and the fitted curve
- Modern, lightweight interface built with customtkinter

## Download

If you just want to use the app, grab the latest `.exe` from the [Releases](https://github.com/tu-usuario/reganalyzer/releases) page, no need to install Python or any dependencies.

## Requirements (for running from source)

- Python 3.10 or higher
- Dependencies listed in `requirements.txt`

## Installation

Clone the repository:

```
git clone https://github.com/tu-usuario/reganalyzer.git
cd reganalyzer
```

Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

Run the application from the project root:

```
python main.py
```

## Project structure

```
reganalyzer/
├── main.py
├── gui/
│   └── app.py
├── assets/
│   └── icons/
│       └── reganalyzer_icon.ico
├── requirements.txt
└── README.md
```

## Building the executable (.exe)

The project can be packaged as a standalone executable using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icons/reganalyzer_icon.ico --add-data "assets;assets" main.py
```

The final executable will be in the `dist/` folder.

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
