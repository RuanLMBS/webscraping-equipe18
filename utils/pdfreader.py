import requests
import os
from pathlib import Path
from urllib.parse import unquote,urlsplit
import fitz  # PyMuPDF
import pdfplumber
from scraping import parse_ufsm,parse_sebrae

link = parse_sebrae()

def baixar_arquivo(url_pdf: str, nome_arquivo: str = None):
    """
    Baixa um arquivo PDF dado o link completo.
    
    :param url_pdf: URL completa do PDF
    :param nome_arquivo: Nome do arquivo para salvar (opcional)
    """
    if not url_pdf:
        print("URL vazia, nada para baixar.")
        return

    try:
        # Extrair nome do arquivo da URL se nenhum for passado
        if not nome_arquivo:
            nome_arquivo = os.path.basename(urlsplit(url_pdf).path)
            nome_arquivo = unquote(nome_arquivo)  # decodifica espaços, acentos etc.

        # Caminho da pasta Downloads
        pasta_downloads = Path.home() / 'Downloads'
        caminho_completo = pasta_downloads / nome_arquivo

        # Fazer o download
        response = requests.get(url_pdf)
        response.raise_for_status()

        # Salvar o arquivo
        with open(caminho_completo, 'wb') as f:
            f.write(response.content)

        print(f"Arquivo salvo em: {caminho_completo}")

    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")
#baixar_arquivo(link)

#def ler_pdf(caminho_pdf):
caminho_pdf = r'C:\Users\Ulle-\Downloads\Edital-06-2025-Bolsista-NPV-Comunicacao.pdf'

"""with pdfplumber.open(caminho_pdf) as pdf: ESSE  AQUI TA RETORNANDO O PDF INTEIRO!
    texto_completo = ""
    for pagina in pdf.pages:
        texto_completo += pagina.extract_text() + "\n"

print(texto_completo.encode("utf-8").decode("utf-8"))"""
    
def extrair_competencias(caminho):
    texto_completo = ""

    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
                
    inicio = texto_completo.lower().find("dos requisitos básicos")
    fim = texto_completo.lower().find("período de vigência")

    if inicio != -1 and fim != -1:
        competencias = texto_completo[inicio:fim]
        return competencias.strip()
    else:
        return "Seção de competências não encontrada."

print(extrair_competencias(caminho_pdf))
'''if pdf_url:
    response = requests.get(pdf_url)

    if response.status_code == 200:
        print(f"\n Lendo o PDF: {pdf_url}\n")

        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            texto_paginas = []
            
            for i, page in enumerate(pdf.pages):
                texto = page.extract_text()
                if texto:
                    texto_paginas.append(texto)
                else:
                    print(f" Página {i+1} sem texto detectado!")

            texto_completo = "\n".join(texto_paginas)

        if texto_completo.strip():
            print(texto_completo[:3000])  
        else:
            print("\n Nenhum texto extraído com pdfplumber. Tentando com PyMuPDF...\n")
            doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
            texto_completo = "\n".join([page.get_text() for page in doc])

            print(texto_completo[:4000])

    else:
        print(f" Erro ao acessar {pdf_url}\n")
else:
    print(" Nenhum PDF encontrado!")'''
