from pathlib import Path
from urllib.parse import unquote,urlsplit
import requests
import pdfplumber
from io import BytesIO
def ler_pdf (url: str):

    try:
        response = requests.get(url)
        response.raise_for_status()

        with pdfplumber.open(BytesIO(response.content)) as pdf:
            texto = ""

            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"

        return texto
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o PDF: {e}")