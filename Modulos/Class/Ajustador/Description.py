from unidecode import unidecode
from ..Config import localhost
import re


class Description:
    def __init__(self, erro):
        self.erro = erro

    def ajusta(self, site, url, r):
        h1 = r.html.find('h1')[0].text.lower()
        todosParagrafo = r.html.find('article p')
        for p in todosParagrafo:
            i = unidecode(p.text.lower()).find(unidecode(h1))
            if i >= 0:
                if len(p.text[i:]) >= 125:
                    novaDescription = p.text[i:]
                    descriptionOK = True
                    break

            else:
                descriptionOK = False
        
        if descriptionOK:
            if novaDescription[-1] == '.' and len(novaDescription) >= 140 and len(novaDescription) <= 160 :
                novaDescription = novaDescription.capitalize()

            else:
                while len(novaDescription) > 145:
                    novaDescription = novaDescription.split(" ")
                    del novaDescription[-1]
                    novaDescription = " ".join(novaDescription)

                novaDescription = novaDescription.capitalize()
                novaDescription += "... Saiba mais.".encode("latin1").decode("unicode_escape")
            
            novaDescription = f"$desc = \"{novaDescription}\";"
            mpi = open(f"{localhost}{site}/{self.arquivo(url)}.php", "rt", -1, "utf-8")
            dados = mpi.read()
            dados = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", novaDescription, dados)
            mpi = open(f"{localhost}{site}/{self.arquivo(url)}.php", "wt", -1, "utf-8")
            mpi.write(dados)
            mpi.close()

        else:
            self.erro.append(f"=> {url}")

    def arquivo(self, url):
        url = url.split('//')
        url = url[1].split('/')
        return url[-1]

