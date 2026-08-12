# PDF Unlocker

PDF Unlocker is a Python utility that helps to unlock PDF files. It uses the PyPDF2 library to read and write PDF files, and offers a user-friendly command-line interface, enhancing the user interaction experience. For optimal performance, it is recommended to use the Windows Terminal. Please be aware that this utility has been exclusively tested on Windows.

**Note:** This utility does not crack or bypass any form of PDF encryption or password protection. It simply reads and writes PDF files using the PyPDF2 library. If a PDF file is encrypted or password-protected, PyPDF2 will not be able to read it. This utility is intended for use with PDF files that are not encrypted or password-protected.

## Installation

**No administrator rights are required.** Both options below install into your own user profile and never prompt for elevation.

### Option 1: the installer (recommended)

Download `PDFUnlocker_<version>_Installer.exe` from the [latest release](https://github.com/krs9891/PDFUnlocker-CLI/releases/latest) and run it. It installs to `%LOCALAPPDATA%\Programs\PDFUnlocker` and adds that folder to your personal `PATH`, so you can type `pu` in any directory.

Close and reopen your terminal after installing, otherwise it won't have picked up the new `PATH` yet.

### Option 2: the portable executable

Download `pu.exe` from the same release and put it wherever you like. Run it as `.\pu.exe` from the folder you keep it in, or add that folder to your `PATH` yourself. Nothing is installed and there is nothing to uninstall — delete the file when you're done with it.

### "Windows protected your PC"

The download is not code-signed, so the first time you run it Windows SmartScreen shows a blue warning. This is expected and simply means the file is new, not that anything is wrong with it.

To continue: click **More info**, then the **Run anyway** button that appears. The "Run anyway" button is hidden until you click "More info" — that's the step most people miss.

If your browser blocks the download itself, choose **Keep** in the downloads bar.

### Upgrading from 0.1.x

The command was renamed from `pdfunlocker` to `pu` in 0.2.0. Version 0.1.x installed to `C:\Program Files` and required an administrator; if someone installed it for you, ask them to uninstall it from **Settings → Apps** so the old `pdfunlocker` command doesn't linger on your `PATH`.

### Running from source

If you have Python installed, you can clone the repository, `pip install -r requirements.txt`, and run [pu.bat](pu.bat) instead. It activates `.venv` if one is present and forwards all arguments to the script.

## Usage

1. Open Windows Terminal in the directory containing the PDF files you want to unlock.
2. Run the command `pu`.
3. You will be prompted with the question "What do you want to do?" with two options:
   - "Unlock All PDFs": This will unlock all PDF files in the directory.
   - "Select PDFs": This will allow you to select specific PDF files to unlock.
4. If you choose "Select PDFs", you will be able to select the PDF files you want to unlock from the list. Navigate through the list using the arrow keys. Select a file by pressing the spacebar, and confirm your selection by pressing Enter.
5. After selecting the files, you will be asked to confirm if you want to proceed.
6. If you confirm, the script will unlock the selected PDF files, overwriting the original files with the unlocked versions.

### Options

| Flag | Description |
| --- | --- |
| `-a`, `--all` | Unlock every PDF in the current directory without any prompts. Useful in scripts. |
| `-v`, `--version` | Print the version and exit. |
| `-h`, `--help` | Show usage. |

```
pu -a
```

## Error Handling

- **In-Use Files**: If the chosen PDF file is currently in use, the script will display a message and stop processing that file.
- **Damaged Files**: If the chosen PDF file is damaged or unreadable, the script will display a message and stop processing that file.

## Dependencies

- **PyPDF2**: A Python library for reading and writing PDF files.
- **InquirerPy**: A Python library for creating interactive command-line user interfaces.
- **yaspin**: A Python library for creating spinners in the command-line interface.
