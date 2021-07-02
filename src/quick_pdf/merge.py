import logging

import PyPDF2
import click
import os


@click.command()
@click.option("-dir", "--directory", "dir", type=click.Path(exists=True), required=True)
@click.option("-out", "--output-filename", "out", type=str, default="MergedPDF")
@click.option("--replace", is_flag=True)
@click.option("--debug", is_flag=True)
def merge_pdf(dir, out: str, replace, debug):
    logging.debug(f'Directory Name: {dir}')

    all_pdf_files = []
    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            all_pdf_files.append(os.path.join(dir, filename))

    if len(all_pdf_files) == 0:
        logging.warning("No PDF Files found in the directory")
    else:
        pdf_writer = PyPDF2.PdfFileWriter()
        for pdf_file in all_pdf_files:
            with open(pdf_file, "rb") as file:
                pdf_reader = PyPDF2.PdfFileReader(file)
                if pdf_reader.numPages > 0:
                    for page_number in range(0, pdf_reader.numPages):
                        pdf_file_page = pdf_reader.getPage(page_number)
                        pdf_writer.addPage(pdf_file_page)

        pdf_out_filename = os.path.join(dir, f"{out}.pdf")
        with open(pdf_out_filename, "wb") as out_pdf_file:
            pdf_writer.write(out_pdf_file)


if __name__ == "__main__":
    merge_pdf()
