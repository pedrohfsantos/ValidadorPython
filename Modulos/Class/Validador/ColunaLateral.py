from collections import defaultdict


class ColunaLateral:
    def __init__(self, erro, erroValidador):
        self.erro = erro
        self.erroValidador = erroValidador
        
    
    def verifica(self, pagina, asideLinks):
        try:
            keys = defaultdict(list)
            for key, value in enumerate(asideLinks):
                keys[value].append(key)

            for value in keys:
                if len(keys[value]) > 1 and value not in self.erro:
                    self.erro.append(value)
        except:
            self.erroValidador.append(pagina)