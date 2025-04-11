from bs4 import BeautifulSoup
import re
import requests

def limpar_titulo(titulo):
    titulo = re.sub(r'^\s*\d{2}/\d{4}\s*-?\s*', '', titulo)
    titulo = re.sub(r'^[-–—]\s*', '', titulo)
    return titulo.strip()

def parse_ufsm():
    url = 'https://www.ufsm.br/pro-reitorias/proinova/busca?q=&sites%5B%5D=399&area=editais&orderby=date&tags='
    pagina = requests.get(url)
    content = pagina.text


    soup = BeautifulSoup(content,'lxml')

    elementos = soup.find_all(class_='info-busca-lista')

    editais = []

    for elemento in elementos:
        link_elemento  = elemento.find("a")
        if not link_elemento:
            continue

        url_edital = link_elemento["href"]
        titulo =  limpar_titulo(link_elemento.text.strip())

        try:
            pagina_edital = requests.get(url_edital)
            soup_pagina_edital = BeautifulSoup(pagina_edital.text,'lxml')

            div_edital = soup_pagina_edital.find(class_="edital-tr-abertura")
            url_pdf = None

            if div_edital:
                link_pdf = div_edital.find("a", href=True)
                if link_pdf:
                    url_pdf = link_pdf["href"]

                editais.append({
                    "titulo":titulo,
                    "url":url_pdf   
                })
        except Exception as e:
            print(f"Erro ao processar o edital {url_edital}: {e}")
    
    return editais
    
"""links_detalhes = [elemento.find("a")["href"] for elemento in elementos if elemento.find("a")]
    pdf_links = []

    for link in links_detalhes:
        pagina_edital = requests.get(link)
        soup_edital = BeautifulSoup(pagina_edital.text,'lxml')

        div_edital = soup_edital.find(class_="edital-tr-abertura")



        if div_edital:
            link_pdf = div_edital.find("a",href=True)
            if link_pdf and 'href' in link_pdf.attrs:   
                pdf_links.append(link_pdf["href"])
    return pdf_links"""