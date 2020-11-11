from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
import re

class Strong:
    
    def __init__(self, erro):
        self.erro = erro

    def ajusta(self, html, url, r):

        content = []
        dic     = []

        def mask(html, chave):

            msk = '!!!PHP!!!'

            def remove(e):
                dic.append(e.group())
                return msk

            def add(e):
                return dic.pop(0)

            try:
                body = re.sub(r"<\?.*\?>", remove, html)
                soup = BeautifulSoup(body, "html.parser")
                mask = re.sub(msk, remove, str(soup.prettify(formatter=None))) if chave else re.sub(msk, add, str(soup.prettify(formatter=None)))
            except:
                mask = False

            return mask

        try:    

            soup = BeautifulSoup(mask(html, True), "html.parser")
            title = re.search(r'\$h1\s*=\s*[\"\'](.*?)[\"\'\;]', html).group(1)
            tipoMPI = '.mpi-content > p, .tabs-content > p' if (soup.find_all('div', class_="mpi-content")) else 'article > p'

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

            return mask(value, False)

        except:
            return False

    def arquivo(self, url):
        url = url.split('//')[1].split('/')[-1].split(' ')[0]
        return url