import PyPDF2
from docx import Document
import io

async def extract_content(file) -> str:
    """Extrai texto de PDF, DOCX ou TXT"""
    
    content = await file.read()
    filename = file.filename.lower()
    
    if filename.endswith(".pdf"):
        return extract_pdf(content)
    elif filename.endswith(".docx"):
        return extract_docx(content)
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    
    raise ValueError("Formato não suportado")

def extract_pdf(content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_docx(content: bytes) -> str:
    """Extrai texto de DOCX"""
    doc = Document(io.BytesIO(content))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text