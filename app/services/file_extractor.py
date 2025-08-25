import io
from fastapi import UploadFile
from PyPDF2 import PdfReader

class FileExtractor:

    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        """Extrai texto de arquivos TXT ou PDF"""
        if file.content_type == "text/plain":
            content = await file.read()
            return content.decode("utf-8")

        elif file.content_type == "application/pdf":
            pdf_bytes = await file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text.strip()

        else:
            raise ValueError(f"Formato de arquivo não suportado: {file.content_type}")
