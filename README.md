# PDF Unlocker

PDF Unlocker is a Python utility that helps to unlock PDF files. It uses the PyPDF2 library to read and write PDF files, and offers a user-friendly command-line interface, enhancing the user interaction experience. For optimal performance, it is recommended to use the Windows Terminal. Please be aware that this utility has been exclusively tested on Windows.

**Note:** This utility does not crack or bypass any form of PDF encryption or password protection. It simply reads and writes PDF files using the PyPDF2 library. If a PDF file is encrypted or password-protected, PyPDF2 will not be able to read it. This utility is intended for use with PDF files that are not encrypted or password-protected.

## Installation

To install PDF Unlocker, download the installer and follow the prompts. This will install the utility and add it to your system's path, allowing you to run it from any directory.

## Usage

1. Open Windows Terminal in the directory containing the PDF files you want to unlock.
2. Run the command `pdfunlocker`.
3. You will be prompted with the question "What do you want to do?" with two options:
   - "Unlock All PDFs": This will unlock all PDF files in the directory.
   - "Select PDFs": This will allow you to select specific PDF files to unlock.
4. If you choose "Select PDFs", you will be able to select the PDF files you want to unlock from the list. Navigate through the list using the arrow keys. Select a file by pressing the spacebar, and confirm your selection by pressing Enter.
5. After selecting the files, you will be asked to confirm if you want to proceed.
6. If you confirm, the script will unlock the selected PDF files, overwriting the original files with the unlocked versions.

## Error Handling

- **In-Use Files**: If the chosen PDF file is currently in use, the script will display a message and stop processing that file.
- **Damaged Files**: If the chosen PDF file is damaged or unreadable, the script will display a message and stop processing that file.

## Dependencies

- **PyPDF2**: A Python library for reading and writing PDF files.
- **InquirerPy**: A Python library for creating interactive command-line user interfaces.
- **yaspin**: A Python library for creating spinners in the command-line interface.
