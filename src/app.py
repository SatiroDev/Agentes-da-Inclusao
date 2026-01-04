from flask import Flask, render_template, url_for

app = Flask(__name__)

agentes = [
    {
        "nome": "Agente IA - TEA",
        "descricao": "Adapta linguagem e estrutura para alunos com Transtorno do Especrtro Autista.",
        "urlImg": ""
    },
    {
        "nome": "Agente IA - Surdez",
        "descricao": "Otimiza conteúdo visual e simplifica textos para alunos surdos ou com deficiência auditiva.",
        "urlImg": ""
    },
    {
        "nome": "Agente IA - TDAH",
        "descricao": "Divide atividades em etapas menores e adiciona elementos de engajamento.",
        "urlImg": ""
    },
    {
        "nome": "Agente IA - Dislexia",
        "descricao": "Adapta textos com fontes, espaçamentos e estrutura otimizados para facilitar a leitura de pessoas com dislexia.",
        "urlImg": ""
    },
    {
        "nome": "Agente IA - Narrador",
        "descricao": "Otimiza conteúdo visual e simplifica textos para alunos surdos ou com deficiência auditiva.",
        "urlImg": ""
    }
]

@app.route("/")
def index():
    return render_template("index.html", agentes=agentes)

if __name__ == "__main__":
    app.run(debug=True)