import os
import argparse
import PyPDF2
import shutil

def extract_pages_to_new_pdf(input_pdf_path):
    temp_output_pdf_path = 'temp_output.pdf'

    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        with open(temp_output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

    shutil.move(temp_output_pdf_path, input_pdf_path)
    print(f"Cleaned {input_pdf_path}")

def main():
    parser = argparse.ArgumentParser(description='Process some PDFs.')
    parser.add_argument('files', metavar='F', type=str, nargs='*', help='a list of PDF files to process')
    args = parser.parse_args()

    files_to_process = args.files if args.files else [file for file in os.listdir(os.curdir) if file.endswith(".pdf")]

    for file in files_to_process:
        extract_pages_to_new_pdf(file)

if __name__ == "__main__":
    main()