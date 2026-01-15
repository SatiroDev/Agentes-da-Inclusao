from flask import Flask, render_template, url_for, redirect

app = Flask( __name__,
    template_folder="src/templates",
    static_folder="src/static")

agentes = [
    {
        "id": 0,
        "nome": "Agente IA - TEA",
        "descricao": "Adapta linguagem e estrutura para alunos com Transtorno do Especrtro Autista.",
        "urlImg": "puzzle-piece-svgrepo-com.svg"
    },
    {
        "id": 1,
        "nome": "Agente IA - Surdez",
        "descricao": "Otimiza conteúdo visual e simplifica textos para alunos surdos ou com deficiência auditiva.",
        "urlImg": "ear-svgrepo-com.svg"
    },
    {
        "id": 2,
        "nome": "Agente IA - TDAH",
        "descricao": "Divide atividades em etapas menores e adiciona elementos de engajamento.",
        "urlImg": "brain-svgrepo-com.svg"
    },
    {
        "id": 3,
        "nome": "Agente IA - Dislexia",
        "descricao": "Adapta textos com fontes, espaçamentos e estrutura otimizados para facilitar a leitura de pessoas com dislexia.",
        "urlImg": "eye-svgrepo-com.svg"
    },
    {
        "id": 4,
        "nome": "Agente IA - Narrador",
        "descricao": "Otimiza conteúdo visual e simplifica textos para alunos surdos ou com deficiência auditiva.",
        "urlImg": "sound-loud-svgrepo-com.svg"
    }
]

@app.route("/")
def index():
    return render_template("index.html", agentes=agentes)

@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route("/chat")
def chat():
    return render_template('chat.html')