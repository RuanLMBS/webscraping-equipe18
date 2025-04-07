from bs4 import BeautifulSoup
import requests
import os

def getpdflinks():
    url = 'https://www.ufsm.br/pro-reitorias/proinova/busca?q=&sites%5B%5D=399&area=editais&orderby=date&tags='
    pagina = requests.get(url)
    pagina.encoding = 'utf-8'
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
