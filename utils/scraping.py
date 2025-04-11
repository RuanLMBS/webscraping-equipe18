from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import quote
    
def parse_ufsm():
    url = 'https://www.ufsm.br/pro-reitorias/proinova/busca?q=&sites%5B%5D=399&area=editais&orderby=date&tags='
    pagina = requests.get(url)
    content = pagina.text


    soup = BeautifulSoup(content,'lxml')

    elementos = soup.find_all(class_='info-busca-lista')

    links_detalhes = [elemento.find("a")["href"] for elemento in elementos if elemento.find("a")]

    pdf_links = []

    for link in links_detalhes:
        pagina_edital = requests.get(link)
        soup_edital = BeautifulSoup(pagina_edital.text,'lxml')

        div_edital = soup_edital.find(class_="edital-tr-abertura")

        if div_edital:
            link_pdf = div_edital.find("a",href=True)
            if link_pdf and 'href' in link_pdf.attrs:
                return link_pdf["href"]
            
        #PARA LISTAR TODOS OS LINKS:
        """if div_edital:
            link_pdf = div_edital.find("a",href=True)
            if link_pdf and 'href' in link_pdf.attrs:   
                pdf_links.append(link_pdf["href"])
    print(pdf_links)"""


def parse_sebrae():
    url_base = 'https://sebrae.com.br/'
    url = 'https://sebrae.com.br/sites/PortalSebrae/ufs/rn/sebraeaz/licitacoes-e-pregao,c32b1d6351ce3510VgnVCM1000004c00210aRCRD'
    pagina = requests.get(url)
    content = pagina.text


    soup = BeautifulSoup(content,'lxml')

    pdf_links = []

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
            return href  # fallback
            

    
    """      if '/./' in href:
                return href.split('/./', 1)[1]  # pega apenas o que vem depois do /./
        else:"""