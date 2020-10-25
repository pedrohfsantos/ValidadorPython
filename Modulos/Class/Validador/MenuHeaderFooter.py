class MenuHeaderFooter:
    def __init__(self, erro, erroValidador):
        self.erro = erro
        self.erroValidador = erroValidador

    
    def verifica(self, menuTopTexts, menuFooterTexts, menuTopLinks, menuFooterLinks):
        try:
            if menuTopTexts != menuFooterTexts:
                self.erro.append('Menu footer diferente do menu header') 

            if menuTopLinks != menuFooterLinks:
                self.erro.append('Links do menu footer diferente do menu header')
        except:
            self.erroValidador.append('MENU TOP/FOOTER')