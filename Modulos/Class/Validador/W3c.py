from requests_html import HTMLSession


class W3c:
    def __init__(self, erroW3C, erroValidador):
        self.erroW3C = erroW3C
        self.session = HTMLSession()
        self.erroValidador = erroValidador
        

    def verifica(self, pagina):
        try:
            w3cLink = f"https://validator.w3.org/nu/?doc={pagina}"
            r = self.session.get(w3cLink)
            erros = r.html.find('#results strong')
            if erros:
                self.erroW3C.append(pagina)   
        except:
            self.erroValidador.append(pagina)