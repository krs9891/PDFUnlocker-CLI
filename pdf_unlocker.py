import os
import PyPDF2
import shutil
import PyPDF2.errors

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from yaspin import yaspin

sp = yaspin()

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
        color_print([("fg:red", "No PDF files found in the current directory.")])
        exit()
    return files

def main():
    try:
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
        print("\nExiting...")
        exit()

if __name__ == "__main__":
    main()