from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import quote


def parse_sebrae():
    url_base = 'https://sebrae.com.br/'
    url = 'https://sebrae.com.br/sites/PortalSebrae/ufs/rn/sebraeaz/licitacoes-e-pregao,c32b1d6351ce3510VgnVCM1000004c00210aRCRD'
    pagina = requests.get(url)
    content = pagina.text

    #OBS: ATUALMENTE, SÓ ESTÁ PEGANDO O PRIMEIRO PDF, PARA FINS DE TESTE!

    soup = BeautifulSoup(content,'lxml')

    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True).lower()
        href_lower = href.lower()

        if href_lower.endswith('.pdf') and ('edital' in text):
            match = re.search(r'/\./(.+)', href)
            if match:
                caminho = match.group(1)
                caminho_codificado = quote(caminho, safe='/')  # codifica espaços e caracteres especiais
                return url_base + caminho_codificado
            return href