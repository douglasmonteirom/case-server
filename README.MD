# Email Analyzer Backend

Backend da aplicação de análise de emails, categorizando-os como **Produtivo** ou **Improdutivo** e sugerindo respostas automatizadas usando a API da OpenAI.

## Estrutura do projeto
```
project/
├─── app/
│    ├── main.py # Entrada da aplicação FastAPI
│    ├── config.py # Configurações e variáveis de ambiente
│    ├── api/
│    │    ├── routes.py # Definição das rotas
│    ├── core/
│    │    ├── email_processor.py # Pipeline de pré-processamento (NLTK, limpeza de texto)
│    ├── services/
│    │    ├── openai_service.py # Comunicação com a API da OpenAI
│    │    ├── agent.py # Definição do agente (prompt, regras)
│    │    ├── file_extractor.py # Extração de texto de arquivos TXT e PDF
│    ├── models/
│    │    ├── email_request.py # Pydantic model para requests
│    │    ├── email_response.py # Pydantic model para responses
│    └── utils/
│         ├── nltk_setup.py # Configuração inicial do NLTK
│
├─── requirements.txt
├─── README.md
└─── start.sh

```
## Pré-requisitos

- Python 3.10 ou superior  
- Pip ou Poetry  
- Conta na OpenAI com API Key

## Instalação e execução local

1. **Clonar o repositório**
```bash
git clone <REPO_URL>
cd <REPO_FOLDER>
```

2. **Criar ambiente virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux / MacOS
.venv\Scripts\activate     # Windows
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```
4. **Configurar variáveis de ambiente**
- Crie um arquivo .env na raiz do projeto com a sua API Key da OpenAI:
```bash
OPENAI_API_KEY=your_openai_api_key
```
5. **Rodar a aplicação**
```bash
uvicorn app.main:app --reload
```
6. **API em Produção**

- A API está disponível na nuvem no seguinte endpoint:

    https://case-server.onrender.com/

7. **Testar a API**

- Após iniciar o servidor, acesse:

Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc

- Ou no ambiente em produção:

Swagger UI → https://case-server.onrender.com/docs

Redoc → https://case-server.onrender.com/redoc


| Rota          | Método | Descrição                                                                        |
| ------------- | ------ | -------------------------------------------------------------------------------- |
| `/processar/` | POST   | Recebe texto ou arquivo (TXT/PDF) e retorna categorização e sugestão de resposta |


**Suporte a arquivos**

- TXT (text/plain)

- PDF (application/pdf)

**Configuração do NLTK**

- O setup inicial dos pacotes do NLTK é feito automaticamente pelo módulo app.utils.nltk_setup. Ele baixa os recursos necessários (punkt, stopwords, wordnet, omw-1.4).

**Boas práticas**

- CORS configurado apenas para o frontend em produção

- Tipagem estática com Pydantic para requests e responses

- Modularidade seguindo padrões SOLID

- Deploy

- Pode ser feito em Render, Vercel, Heroku, ou outro serviço de backend compatível com FastAPI.

- Certifique-se de definir a variável OPENAI_API_KEY no ambiente de produção.

*Autor: Douglas Monteiro*

*Última atualização: Agosto 2025*