import pdfplumber
import requests
from io import BytesIO
import re

def encontrar_indices(texto: str, padroes: list) -> list:
    indices = []
    for padrao in padroes:
        for match in re.finditer(padrao, texto, re.IGNORECASE):
            indices.append(match.start())
    return sorted(indices)

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

    texto_lower = texto_completo.lower()

    padroes_inicio = [
        "dos requisitos",
        "requisitos para",
        "requisitos necessários",
        "requisitos exigidos",
        "requisitos e compromissos",
        "requisitos",
        "características e critérios"
    ]

    padroes_fim = [
        "período de vigência da bolsa",
        "dos projetos",
        "da inscrição",
        "das indicações",
        "documentação exigida",
        "cronograma"
    ]

    inicios = encontrar_indices(texto_lower, padroes_inicio)
    fins = encontrar_indices(texto_lower, padroes_fim)

    print("Índices de início encontrados:", inicios)
    print("Índices de fim encontrados:", fins)

    # Encontra o primeiro par válido onde inicio < fim
    for inicio in inicios:
        for fim in fins:
            if inicio < fim:
                trecho = texto_completo[inicio:fim]
                print("[Trecho encontrado]:", trecho[:300], "...")
                return trecho.strip()

    return "Seção não encontrada"
