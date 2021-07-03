import logging
import os

import PyPDF2
import click


@click.command()
@click.option("-dir", "--directory", "dir", type=click.Path(exists=True), required=True)
@click.option("-out", "--output-filename", "out", type=str, default="MergedPDF")
@click.option("--replace", is_flag=True)
@click.option("--debug", is_flag=True)
def merge_pdf(dir, out: str, replace, debug):
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    if not debug:
        logging.disable(logging.DEBUG)
    logging.debug(f"Directory Name: {dir}")

    all_pdf_files = []
    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            all_pdf_files.append(os.path.join(dir, filename))

    if len(all_pdf_files) == 0:
        logging.warning("No PDF Files found in the directory")
    else:
        logging.debug(f"Merging files: {all_pdf_files}")
        pdf_merger = PyPDF2.PdfFileMerger()
        for pdf_filename in all_pdf_files:
            pdf_merger.append(pdf_filename)
        pdf_out_filename = os.path.join(dir, f"{out}.pdf")
        with open(pdf_out_filename, "wb") as out_pdf_file:
            pdf_merger.write(out_pdf_file)
        logging.info(f"Merged PDF saved at {pdf_out_filename}")


if __name__ == "__main__":
    merge_pdf()
