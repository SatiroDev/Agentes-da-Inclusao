from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import ProvaOrchestrator
from utils.file_processor import extract_content
import asyncio
from session_store import sessions

from utils.pdf import gerar_pdf_prova

from fastapi.responses import StreamingResponse



from config import client


from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent



app = FastAPI(title="API de Adaptação de Provas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "src" / "static")), name="static")



# Instância do orquestrador
orchestrator = ProvaOrchestrator()

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "content": None,
            "adapted_content": None,
            "stage": None,
            "agente": "educacional",
            "metadata": {}
        }
    return sessions[session_id]



@app.post("/api/adapt/upload")
async def upload_prova(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    session = get_session(session_id)

    content = await extract_content(file)
    session["content"] = content
    session["stage"] = "auto_adapt"

    agente = session.get("agente", "educacional")

    prompt = f"""
    Você é um especialista em adaptação pedagógica ({agente}).

    Reformule a prova abaixo de forma clara, organizada e acessível ao público-alvo.

    ⚠️ REGRAS IMPORTANTES:
    - NÃO use Markdown.
    - NÃO use **, *, # ou qualquer símbolo de formatação.
    - NÃO use símbolos LaTeX como $, \\ ou comandos matemáticos.
    - NÃO use negrito, itálico ou listas com traços.
    - Use apenas texto simples.
    - Organize com quebras de linha bem distribuídas.
    - Deixe o texto pronto para impressão em PDF.

    Responda exatamente neste formato:

    ===PROVA===
    (conteúdo final da prova organizado, limpo e pronto para impressão)

    ===EXPLICACAO===
    (explicação objetiva do que foi adaptado e por quê)

    Prova original:
    {content}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    texto = response.text

    if "===PROVA===" in texto and "===EXPLICACAO===" in texto:
        prova = texto.split("===PROVA===")[1].split("===EXPLICACAO===")[0].strip()
        explicacao = texto.split("===EXPLICACAO===")[1].strip()
    else:
        prova = texto
        explicacao = ""

    session["adapted_content"] = prova
    session["explicacao"] = explicacao
    session["stage"] = "chatting"

    pdf_path = gerar_pdf_prova(prova, session_id)

    return {
        "message": "✅ Prova adaptada com sucesso!",
        "adapted": prova,
        "explicacao": explicacao,
        "pdf_url": f"/api/adapt/pdf?session_id={session_id}"
    }

templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")

@app.get("/")
async def index(request: Request):
    agentes = get_agents()  # <- pega dados diretamente
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "agentes": agentes
        }
    )

@app.get("/api/agents")
async def list_agents():
    """Lista todos os agentes disponíveis"""
    return {"agents": AGENTS}

@app.get("/upload")
async def upload(request: Request, agente: str | None = None):
   return templates.TemplateResponse(
        "upload.html",
        {
            "request": request,
            "agente": agente
        }
    )

@app.get("/chat")
async def chat(request: Request):
    agente = request.query_params.get("agente")

    return templates.TemplateResponse(
        'chat.html',
        {
            "request": request,
            "agente": agente
        }
    )

@app.post("/api/chat")
async def chat_api(
    session_id: str = Form(...),
    mensagem: str = Form(...)
):
    session = get_session(session_id)

    content = session.get("content")
    adapted = session.get("adapted_content")

    # 🔹 Se ainda não existe prova
    if not content and not adapted:
        return {
            "resposta": "📂 Envie uma prova primeiro para que eu possa adaptá-la."
        }

    texto = mensagem.lower()

    # 🔹 Se pediu PDF
    if "pdf" in texto or "baixar" in texto or "gerar" in texto:

        if not adapted:
            return {"resposta": "⚠️ Nenhuma prova adaptada encontrada."}

        return {
            "resposta": "📄 Sua prova está pronta!",
            "pdf_url": f"/api/adapt/pdf?session_id={session_id}"
        }

    # 🔹 Conversa normal
    contexto = adapted or content

    prompt = f"""
Contexto da prova:
{contexto}

Usuário:
{mensagem}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return {"resposta": response.text}



@app.post("/api/chat/init")
async def chat_init(
    agente: str = Form(...),
    session_id: str = Form(...)
):
    session = get_session(session_id)

    session["agente"] = agente
    session["stage"] = "init"
    session["content"] = None  # ainda não tem prova
    prompts_iniciais = {
        "tea": """
Você é um agente especializado em adaptação de provas para alunos com TEA.
Explique brevemente como você pode ajudar e pergunte se o usuário deseja
alguma adaptação específica (linguagem, estrutura, visual).
""",

        "tdah": """
Você é um agente especializado em adaptação para alunos com TDAH.
Explique que você pode dividir conteúdos em etapas, reduzir distrações
e melhorar a organização do conteúdo.
Pergunte como o usuário prefere a apresentação da prova.
""",

        "surdez": """
Você é um agente especializado em adaptação de provas para alunos surdos.
Explique que você pode:
- Simplificar a linguagem
- Priorizar frases curtas e diretas
- Adaptar para Libras (descrição textual)
Pergunte se a prova será usada com Libras, leitura labial ou apenas texto.
""",

        "dislexia": """
Você é um agente especializado em adaptação para alunos com dislexia.
Explique que você pode:
- Simplificar vocabulário
- Reduzir blocos longos de texto
- Reorganizar enunciados de forma clara
Pergunte se o usuário prefere frases mais curtas ou apoio visual.
""",

        "narrador": """
Você é um agente narrador educacional.
Explique que você pode transformar o conteúdo em leitura guiada,
com ritmo ajustável e pausas.
Pergunte se prefere leitura lenta, normal ou com explicações extras.
"""
    }

    prompt = prompts_iniciais.get(
        agente,
        "Você é um agente educacional especializado em adaptação de provas."
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return {"resposta": response.text}

def get_agents():
    return AGENTS

@app.get("/api/adapt/pdf")
async def baixar_pdf(session_id: str):
    session = get_session(session_id)

    adapted = session.get("adapted_content")
    if not adapted:
        return {"error": "Prova adaptada não encontrada"}

    caminho_pdf = gerar_pdf_prova(adapted, session_id)

    return FileResponse(
        caminho_pdf,
        media_type="application/pdf",
        filename="prova_adaptada.pdf"
    )




AGENTS = [
    {
        "id": "tea",
        "name": "Agente IA - TEA",
        "description": "Adapta linguagem e estrutura para alunos com Transtorno do Espectro Autista",
        "url": "puzzle-piece-svgrepo-com.svg"
    },
    {
        "id": "surdez",
        "name": "Agente IA - Surdez",
        "description": "Otimiza conteúdo visual para alunos surdos ou com deficiência auditiva",
        "url": "ear-svgrepo-com.svg"
    },
    {
        "id": "tdah",
        "name": "Agente IA - TDAH",
        "description": "Divide atividades em etapas menores e adiciona elementos de engajamento",
        "url": "brain-svgrepo-com.svg"
    },
    {
        "id": "dislexia",
        "name": "Agente IA - Dislexia",
        "description": "Adapta textos com fontes, espaçamentos e estrutura otimizados",
        "url": "eye-svgrepo-com.svg"
    },
    {
        "id": "narrador",
        "name": "Agente IA - Narrador",
        "description": "Otimiza conteúdo para narração e leitura em voz alta",
        "url": "sound-loud-svgrepo-com.svg"
    }
]


