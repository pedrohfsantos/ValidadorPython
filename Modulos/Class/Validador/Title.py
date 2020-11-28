from collections import defaultdict

class Title:
    def __init__(self, erroSemH1, erroH1, erroTituloIgualH1, erroTituloDuplicado, erroTtutiloStrong, erroValidador):
        self.erroSemH1 = erroSemH1
        self.erroH1 = erroH1
        self.erroTituloIgualH1 = erroTituloIgualH1
        self.erroTituloDuplicado = erroTituloDuplicado
        self.erroTtutiloStrong = erroTtutiloStrong
        self.erroValidador = erroValidador

    def verifica(self, pagina, h1, h2, titleStrong, h3=False):
        try:
            if len(h1) == 0:
                self.erroSemH1.append(pagina)

            elif len(h1) > 1:
                self.erroH1.append(pagina)
            
            self.titulo_duplicado(h2, pagina)
            self.titulo_igual_h1(h2, h1, pagina)

            if len(titleStrong) > 0:
                self.erroTtutiloStrong.append(pagina)

            if h3:
                self.titulo_duplicado(h3, pagina)
                self.titulo_igual_h1(h3, h1, pagina)
        except:
            self.erroValidador.append(pagina)

    def titulo_igual_h1(self, title, h1, pagina):
        for titulo in title:
            if titulo.text.lower() == h1[0].text.lower():
                self.erroTituloIgualH1.append(pagina)
                return

    def titulo_duplicado(self, title, pagina):
        msm = []
        keys = defaultdict(list)
        for key, value in enumerate(title):
            keys[value.text].append(key)

        for value in keys:
            if len(keys[value]) > 1:
                msm.append(f'"{value}"')

        if len(msm) > 0:
            self.erroTituloDuplicado.append(pagina + ": " + ", ".join(msm))
