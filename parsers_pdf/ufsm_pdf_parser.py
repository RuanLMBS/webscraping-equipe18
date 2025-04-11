import pdfplumber
import requests
from io import BytesIO


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

    inicio = texto_lower.find("dos requisitos básicos")
    fim = texto_lower.find("período de vigência da bolsa")

    if inicio != -1 and fim != -1:
        competencias = texto_completo[inicio:fim]
        return competencias.strip()
    else:
        return "Seção não encontrada"
