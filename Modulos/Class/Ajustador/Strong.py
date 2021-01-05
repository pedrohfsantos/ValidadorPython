from unidecode import unidecode
from ..Config import localhost
import re


class Strong:
    def __init__(self, erro):
        self.erro = erro

    def ajusta(self, site, url, r):
        try:
            h1 = r.html.find("h1")[0].text.lower()
            todosParagrafo = r.html.find("article p")
            paginaAjustada = False

            for p in todosParagrafo:
                strong = True if p.find("strong") else False
                h1InP = True if unidecode(h1) in unidecode(p.text.lower()) else False

                if strong != h1InP:
                    i = unidecode(p.text.lower()).find(unidecode(h1))
                    f = i + len(h1)
                    mpi = open(f"{localhost}{site}/{self.arquivo(url)}.php", "rt", -1, "utf-8")
                    dados = mpi.read()
                    dados = re.sub(
                        r"(<\s*(p|li)>\s*.*?)(?:(?:<\s*strong\s*>)?" + p.text[i:f] + r"(?:<\s*\/strong\s*>)?)",
                        r"\1<strong>" + h1 + "</strong>",
                        dados,
                        flags=re.IGNORECASE,
                    )
                    mpi = open(f"{localhost}{site}/{self.arquivo(url)}.php", "wt", -1, "utf-8")
                    mpi.write(dados)
                    mpi.close()

                    paginaAjustada = True

                if paginaAjustada:
                    break

            if paginaAjustada == False:
                self.erro.append(f"{url}")

        except Exception as erro:
            self.erro.append(f"{url} - {erro}")

    def arquivo(self, url):
        url = url.split("//")
        url = url[1].split("/")
        return url[-1]