class Texto:
    def __init__(self, erroLoremIpsum, erroValidador):
        self.erroLoremIpsum = erroLoremIpsum
        self.erroValidador = erroValidador

    def verifica(self, pagina, texto_pagina):
        try:
            self.texto_lorem_ipsum(pagina, texto_pagina)
        except:
            self.erroValidador.append(pagina)

    def texto_lorem_ipsum(self, pagina, texto):
        if "lorem ipsum" in str(texto).lower():
            self.erroLoremIpsum.append(pagina)