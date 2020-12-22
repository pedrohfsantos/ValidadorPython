class Description:
    def __init__(self, erroTamanho, erroH1, erroValidador):
        self.erroTamanho = erroTamanho
        self.erroH1 = erroH1
        self.erroValidador = erroValidador

    def verifica(self, pagina, description, h1):
        try:
            if len(description) > 160 or len(description) < 140:
                self.erroTamanho.append(pagina)

            if h1[0].text.lower() not in description.lower():
                self.erroH1.append(pagina)
        except:
            self.erroValidador.append(pagina)