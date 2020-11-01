from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
from ..Construct import *
import re

mascara = Mascara()  

class Strong:
    def __init__(self, erro):
        self.erro = erro

    def ajusta(self, html, url, r):
        content = []
        try:
            soup = BeautifulSoup(mascara.Aplicar(html), "html.parser")
            title = r.html.find('h1')[0].text

            tipoMPI = '.mpi-content > p, .tabs-content > p' if len(soup.find_all('div', class_="mpi-content")) > 0 else 'article > p'

            for p in soup.select(tipoMPI):

                element = p.find_all('strong')

                if element:
                    for strong in element:
                        if unidecode(title).lower() != unidecode(strong.string).lower().strip():
                            strong.string = title.lower()
                else:
                    try:
                        if unidecode(title).lower() in unidecode(p.string).lower().strip():
                            r = unidecode(p.string).lower().strip().replace(unidecode(title).lower().strip(), '<strong>' + title.lower() + '</strong>')
                            p.string = r
                    except:
                        self.erro.append(f"=> {url}")

            for elem in soup.prettify(formatter=None):
                content.append(elem)
            value = ''.join(map(str, content))

            return mascara.Retirar(value)
            mascara.reset()

        except:
            mascara.reset()

    def arquivo(self, url):
        url = url.split('//')[1].split('/')[-1].split(' ')[0]
        return url