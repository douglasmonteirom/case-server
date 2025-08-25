from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from app.models.email_response import EmailResponse
from app.core.email_processor import EmailProcessor
from app.services.agent import EmailAgent
from app.services.openai_service import OpenAIService
from app.services.file_extractor import FileExtractor

router = APIRouter()

def get_email_agent() -> EmailAgent:
    return EmailAgent(OpenAIService())


@router.post("/processar/", response_model=EmailResponse)
async def process_email(
    text: str = Form(None),
    file: UploadFile = File(None),
    agent: EmailAgent = Depends(get_email_agent),
):

    # Garantir que ao menos um dos inputs foi enviado
    if not text and not file.filename:
        raise HTTPException(status_code=400, detail="É necessário enviar texto ou arquivo")

    # Caso arquivo seja enviado, extrair conteúdo
    if file.filename:
        try:
            text = await FileExtractor.extract_text(file)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao extrair arquivo: {str(e)}")

    # Processar texto (limpeza com NLTK, etc.)
    processor = EmailProcessor()
    clean_text = processor.clean_text(text)

    # Chamar agente para análise com OpenAI
    try:
        result = await agent.analyze_email(clean_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar email: {str(e)}")

    return EmailResponse(**result)
