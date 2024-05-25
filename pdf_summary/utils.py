import io
from PyPDF2 import PdfReader
from config.logging_config import logger

def get_text_content_from_pdf_content(content: bytes) -> str:
    text_content = str()
    with io.BytesIO(content) as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text_content += page.extract_text()
    
    logger.debug(text_content)
    return text_content
