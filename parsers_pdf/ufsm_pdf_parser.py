import pdfplumber
import requests
from io import BytesIO
import re

def encontrar_indice(texto: str, padroes: list) -> int:
    for padrao in padroes:
        idx = texto.find(padrao.lower())
        if idx != -1:
            return idx
    return -1

def extrair_competencias(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    texto_completo = ""
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for i, page in enumerate(pdf.pages):
            texto = page.extract_text()
            if texto:
                texto_completo += texto
            else:
                print("[Página sem texto extraído]")

    # Certifique-se de que os termos estão em minúsculas
    texto_lower = texto_completo.lower()

    padroes_inicio = [
        "dos requisitos",
        "requisitos para",
        "requisitos necessários",
        "requisitos exigidos",
        "requisitos e compromissos",
        "requisitos",
        r"\d+\.\s*requisitos",
        "CRITÉRIOS DE SELEÇÃO"
    ]

    padroes_fim = [
        "período de vigência da bolsa",
        "dos projetos",
        "da inscrição",
        "das indicações",
        "documentação exigida"
    ]

    #inicio = texto_lower.find("dos requisitos")
    #fim = texto_lower.find("período de vigência da bolsa")

    inicio = encontrar_indice(texto_lower, padroes_inicio)
    if(inicio):
        print(texto_lower)
    fim = encontrar_indice(texto_lower, padroes_fim)


    if inicio != -1 and fim != -1:
        competencias = texto_completo[inicio:fim]
        print (competencias)
        return competencias.strip()
    else:
        return "Seção não encontrada"
