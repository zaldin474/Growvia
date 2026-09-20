import io
import pdfplumber

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

def _iter_docx_blocks( document):

    for child in (
        document.element.body.iterchildren()
    ):

        if child.tag == qn("w:p"):

            yield Paragraph(
                child,
                document
            )

        elif child.tag == qn("w:tbl"):

            yield Table(
                child,
                document
            )
            
            
def extract_pdf_text(file_bytes: bytes) -> str:
    text_parts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                text_parts.append(text)

    return "\n".join(text_parts)


def extract_docx_text(
    file_bytes: bytes
) -> str:

    document = Document(
        io.BytesIO(file_bytes)
    )

    text_parts = []

    for block in _iter_docx_blocks(
        document
    ):

        if isinstance(
            block,
            Paragraph
        ):

            text = block.text.strip()

            if text:

                text_parts.append(
                    text
                )

        elif isinstance(
            block,
            Table
        ):

            for row in block.rows:

                row_parts = []

                for cell in row.cells:

                    cell_text = " ".join(
                        paragraph.text.strip()
                        for paragraph
                        in cell.paragraphs
                        if paragraph.text.strip()
                    )

                    if (
                        cell_text
                        and
                        cell_text
                        not in row_parts
                    ):

                        row_parts.append(
                            cell_text
                        )

                if row_parts:

                    text_parts.append(
                        " | ".join(
                            row_parts
                        )
                    )

    return "\n".join(
        text_parts
    )


def extract_txt_text(file_bytes: bytes) -> str:
    return file_bytes.decode(
        "utf-8",
        errors="ignore"
    )


def extract_cv_text(file_bytes: bytes, filename: str) -> str:

    if (
        not isinstance(filename, str)
        or
        not filename.strip()
    ):

        raise ValueError(
            "CV filename is required."
        )

    filename = filename.lower()

    if filename.endswith(".pdf"):

        parser = extract_pdf_text

    elif filename.endswith(".docx"):

        parser = extract_docx_text

    elif filename.endswith(".txt"):

        parser = extract_txt_text

    else:

        raise ValueError(
            "Unsupported CV format. "
            "Supported formats: PDF, DOCX, TXT."
        )

    try:

        text = parser(
            file_bytes
        )

    except Exception as error:

        raise ValueError(
            "The uploaded CV file could not be parsed. "
            "It may be corrupted or invalid."
        ) from error

    text = text.strip()

    if not text:

        raise ValueError(
            "No readable text was found in the CV."
        )

    return text