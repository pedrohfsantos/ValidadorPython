class MapaDoSite:
    def __init__(self, erro, erroValidador):
        self.erro = erro
        self.erroValidador = erroValidador

    def verifica(self, pagina, listaDeLinks):
        try:
            if pagina not in listaDeLinks and '/mapa-site' not in pagina:
                self.erro.append(pagina)
        except:
            self.erroValidador.append(pagina)