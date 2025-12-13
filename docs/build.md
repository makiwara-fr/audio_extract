# Build Instructions

## 1. Building the Python Package (Wheel and Source Distribution)

To build the standard Python package (installable via pip), use `uv`.

### Prerequisites
Ensure `uv` is installed.

### Build Command
Run the following command from the root of the repository:
```bash
uv build
```

This will create a `dist/` directory containing the `.whl` and `.tar.gz` files.

## 2. Building the Standalone GUI Executable

To create a standalone executable (e.g., `.exe` on Windows) for the GUI, use `PyInstaller`.

### Prerequisites
Ensure the package and development dependencies are installed:
```bash
uv pip install . pyinstaller
```

### Build Command
Run the following command from the root of the repository:
```bash
pyinstaller --noconsole --onefile --name audio_extract_gui src/audio_extract/gui.py
```

The resulting executable will be found in the `dist/` folder.

**Note:** The generated executable requires FFMPEG to be installed on the target system or configured within the application.
