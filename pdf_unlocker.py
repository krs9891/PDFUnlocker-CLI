import os
import sys
import PyPDF2
import shutil
import PyPDF2.errors
import argparse

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from yaspin import yaspin
from version import __version__

class PlainSpinner:
    """Drop-in stand-in for yaspin, for output that can't show an animation.

    yaspin animates with Braille characters. When stdout is redirected, or the
    console runs a legacy codepage, encoding those raises UnicodeEncodeError
    inside the spinner thread and dumps a traceback over the output. Piping
    `pu -a` to a file is ordinary usage, so print plain lines instead.
    """

    def __init__(self):
        self.text = ""
        self.color = None

    def start(self):
        pass

    def stop(self):
        pass

    def ok(self, mark="OK"):
        print(f"{mark} {self.text}")

    def fail(self, mark="FAIL"):
        print(f"{mark} {self.text}")

    def write(self, message):
        print(message)

def stdout_is_console():
    """Whether prompt_toolkit can be used.

    Both color_print and the inquirer prompts go through prompt_toolkit, which
    raises NoConsoleScreenBufferError when stdout isn't a real console.
    """
    return sys.stdout.isatty()

def supports_spinner():
    if not stdout_is_console():
        return False
    try:
        "⠋".encode(sys.stdout.encoding or "ascii")
    except (UnicodeEncodeError, LookupError):
        return False
    return True

def print_error(message):
    if stdout_is_console():
        color_print([("fg:red", message)])
    else:
        print(message)

sp = yaspin() if supports_spinner() else PlainSpinner()

def handle_failure(message):
    sp.color = "red"
    sp.fail()
    sp.write(message)

def extract_pages_to_new_pdf(input_pdf_path):
    temp_output_pdf_path = 'temp_output.pdf'

    sp.color = "green"
    sp.text = input_pdf_path
    sp.start()

    try:
        with open(input_pdf_path, 'rb') as input_pdf_file:
            reader = PyPDF2.PdfReader(input_pdf_file)
            writer = PyPDF2.PdfWriter()

            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            with open(temp_output_pdf_path, 'wb') as output_pdf_file:
                writer.write(output_pdf_file)

        shutil.move(temp_output_pdf_path, input_pdf_path)
        sp.ok()
    except PermissionError:
        handle_failure(f"Could not process {input_pdf_path} because it is currently in use.")
        os.remove(temp_output_pdf_path)
    except (PyPDF2.errors.EmptyFileError, PyPDF2.errors.PdfReadError):
        handle_failure(f"Could not process {input_pdf_path} because the file is damaged or unreadable.")

    sp.stop()

def get_pdf_choices_from_dir():
    files = [Choice(file) for file in os.listdir('.') if file.endswith(".pdf")]
    if not files:
        print_error("No PDF files found in the current directory.")
        sys.exit()
    return files

def main():
    parser = argparse.ArgumentParser(description="Unlock PDF files by extracting all pages to a new PDF file.")
    parser.add_argument("-v", "--version", action="version", version=f"PDFUnlocker-CLI version {__version__}")
    parser.add_argument("-a", "--all", action="store_true", help="Unlock all PDF files in the current directory.")
    args = parser.parse_args()
    
    try:
        if args.all:
            files_to_process = [file for file in os.listdir('.') if file.endswith(".pdf")]
            if not files_to_process:
                print_error("No PDF files found in the current directory.")
                sys.exit()

            for file in files_to_process:
                extract_pages_to_new_pdf(file)
            return

        # Default behavior with inquirer prompts, which need a real console
        if not stdout_is_console():
            print_error("This command needs an interactive terminal. Use -a to unlock every PDF in the current directory without prompts.")
            sys.exit(1)

        files_list = get_pdf_choices_from_dir()

        action = inquirer.select(
            message="What do you want to do?",
            choices=[Choice(value="All", name="Unlock All PDFs"), 
                     Choice(value="Select", name="Select PDFs")],
            default="All"
        ).execute()

        if action == "All":
            files_to_process = [file.value for file in files_list]
        else:
            files_to_process = inquirer.checkbox(
                message="Select file(s):",
                choices=files_list,
                transformer=lambda result: "%s file%s selected"
                % (len(result), "s" if len(result) > 1 else ""),
                validate=lambda result: len(result) >= 1,
                invalid_message="You must select at least one file."
            ).execute()

        proceed = inquirer.confirm(
            message="Do you want to proceed?",
            default=True
        ).execute()

        if proceed:
            for file in files_to_process:
                extract_pages_to_new_pdf(file)

    except KeyboardInterrupt:
        # sys.exit, not exit: the latter is installed by the site module and
        # doesn't exist in the PyInstaller-frozen build, where calling it
        # raises NameError instead of exiting.
        print("\nExiting...")
        sys.exit()

if __name__ == "__main__":
    main()