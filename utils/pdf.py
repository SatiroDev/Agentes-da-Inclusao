from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import textwrap
import os

def gerar_pdf_prova(texto, session_id):
    os.makedirs("pdfs", exist_ok=True)

    caminho = f"pdfs/prova_{session_id}.pdf"
    c = canvas.Canvas(caminho, pagesize=A4)

    largura, altura = A4
    margem_esquerda = 2 * cm
    margem_direita = 2 * cm
    margem_superior = 2 * cm
    margem_inferior = 2 * cm

    largura_util = largura - margem_esquerda - margem_direita
    y = altura - margem_superior

    c.setFont("Helvetica", 12)

    for linha in texto.split("\n"):

        # quebra automática de linha baseada na largura
        linhas_quebradas = textwrap.wrap(linha, width=90)

        for l in linhas_quebradas:
            if y < margem_inferior:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = altura - margem_superior

            c.drawString(margem_esquerda, y, l)
            y -= 15

    c.save()
    return caminho
