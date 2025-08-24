from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
from processa_emails import processar_email
import os
import json
import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

try:
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print("Arquivo .env carregado")
    else:
        print(".env não encontrado, usando variáveis de ambiente do sistema")
except ImportError:
    print("python-dotenv não instalado, usando variáveis de ambiente do sistema")


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY não definida! Configure no .env ou nas variáveis de ambiente do servidor")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://case-client-9wcrzx18r-douglas-projects-a646adef.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(api_key=API_KEY)

@app.post("/processar/")
async def processar(file: UploadFile = File(None), texto: str = Form(None)):

    if file.filename != "":
        filename = file.filename if file.filename is not None else ""
        ext = os.path.splitext(filename)[1].lower()
        conteudo = await file.read()
        caminho_temp = f"temp{ext}"
        with open(caminho_temp, "wb") as f:
            f.write(conteudo)
        texto_processado = processar_email(caminho_temp)
        os.remove(caminho_temp)
    elif texto:
        texto_processado = processar_email(texto)
    else:
        return JSONResponse({"erro": "Envie um arquivo ou texto."}, status_code=400)

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "Você é um assistente que recebe e analisa textos de email, "
             "categoriza o conteúdo em Produtivo ou Improdutivo e sugere uma resposta "
             "adequada para enviar do destinatario ao remetente à categoria identificada, "
             "por exemplod: - **Produtivo:** Emails que requerem uma ação ou resposta "
             "específica ex.: solicitações de suporte técnico, atualização sobre casos em aberto, "
             "dúvidas sobre o sistema.- **Improdutivo:** "
             "Emails que não necessitam de uma ação imediata ex.: "
             "mensagens de felicitações, agradecimentos."
             "gere uma resposta com o seguinte formato, um objeto com as chaves category e suggestion, onmde será possível acessar essas chaves de dentro do conteudo da resposta da API da OpenAI"},
            {"role": "user", "content": texto_processado}
        ]
    )
    if resposta.choices[0].message.content is not None:
        Resp = json.loads(resposta.choices[0].message.content)
    else:
        Resp = { "category": "", "suggestion": ""}
    return Resp