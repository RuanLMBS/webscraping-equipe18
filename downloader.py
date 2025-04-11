import requests
import os
from pathlib import Path
from urllib.parse import unquote,urlsplit

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