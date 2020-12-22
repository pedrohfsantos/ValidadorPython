import re
from requests_html import HTMLSession
from Modulos.Class.Config import localhost, urlmpitemporario


class W3c:
    def __init__(self, erroW3C, erroValidador):
        self.erroW3C = erroW3C
        self.session = HTMLSession()
        self.erroValidador = erroValidador

    def verifica(self, pagina):
        try:
            w3cLink = f"https://validator.w3.org/nu/?doc={self.url_urlmpitemporario(pagina)}"
            r = self.session.get(w3cLink)
            erros = r.html.find("#results strong")
            if erros:
                self.erroW3C.append(pagina)
        except:
            self.erroValidador.append(pagina)

    def url_urlmpitemporario(self, url):
        if "localhost/" in url:
            htdocs = re.search(r"^.*?htdocs\\*(.*)", localhost)
            htdocs = "" if not htdocs.group(1) else htdocs.group(1).replace("\\", "/")
            url = re.sub(r"https?:\/\/.*?\/" + htdocs, urlmpitemporario, url)
        return url
