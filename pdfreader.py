import requests
import pdfplumber
import io
import fitz  # PyMuPDF
from Testes.scraping import getpdflinks

pdf_url = getpdflinks()

if pdf_url:
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
    print(" Nenhum PDF encontrado!")
