from unidecode import unidecode
from ..Config import localhost
import re


class Description:
    def __init__(self, erro):
        self.erro = erro

    def ajusta(self, site, url, r):
        h1 = r.html.find("h1")[0].text.lower()
        todos_paragrafos = r.html.find("article p:not(.content-call)")
        for p in todos_paragrafos:
            i = unidecode(p.text.lower()).find(unidecode(h1))
            if i >= 0:
                if len(p.text[i:]) >= 125:
                    nova_description = p.text[i:]
                    descriptionOK = True
                    break

            else:
                descriptionOK = False

        if descriptionOK:

            if nova_description[-1] == "." and len(nova_description) in range(140, 161):
                nova_description = nova_description.capitalize()

            else:
                while len(nova_description) > 145:
                    nova_description = nova_description.split(" ")
                    del nova_description[-1]
                    nova_description = " ".join(nova_description)

                nova_description = nova_description.capitalize()
                nova_description += "... Saiba mais.".encode("latin1").decode("unicode_escape")

            nova_description = f'$desc = "{nova_description}";'

            with open(f"{localhost}{site}/{self.arquivo(url)}.php", "rt", -1, "utf-8") as mpi:
                dados = mpi.read()
                dados = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", nova_description, dados)
            with open(f"{localhost}{site}/{self.arquivo(url)}.php", "wt", -1, "utf-8") as mpi:
                mpi.write(dados)

        else:
            self.erro.append(f"=> {url}")

    def arquivo(self, url):
        url = url.split("//")[1].split("/")[-1]
        return url