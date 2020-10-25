import json
from os import listdir


class Arquivo:
    def __init__(self):
        pass


    def url_projeto_mpitemporario(self, limpaUrl):
        limpaUrl = limpaUrl.split('//')
        limpaUrl = limpaUrl[1].split('/')
        limpaUrl = [x for x in limpaUrl if x]
        return limpaUrl[-1]


    def arquivo_validacao(self, errosEncontrado, erroValidacao, site):
        log = False
        for erro in erroValidacao.keys():
            if len(erroValidacao[erro]) > 0:
                log = True
                break

        arquivo = open(f"Projetos/{self.url_projeto_mpitemporario(site)}.txt", "w", -1, "utf-8")

        for errosItens in errosEncontrado.keys():
            if len(errosEncontrado[errosItens]) > 0:
                arquivo.write(f'{errosItens}: \n')

                for errosValores in errosEncontrado[errosItens]:
                    arquivo.write(f'=> {errosValores} \n')

                arquivo.write('\n')

            errosEncontrado[errosItens].clear()

        if log:
            arquivo.write(f' =-==-==-==-==-==-==-==-==-= LOG DE ERRO DO VALIDADOR | PROJETO {site} =-==-==-==-==-==-==-==-==-==-==-= \n')
            for errosItensValidacao in erroValidacao.keys():
                if len(erroValidacao[errosItensValidacao]) > 0:
                    arquivo.write(f'{errosItensValidacao}: \n')

                    for errosValores in erroValidacao[errosItensValidacao]:
                        arquivo.write(f'=> {errosValores}\n')

                    arquivo.write('\n')

                erroValidacao[errosItensValidacao].clear()

        arquivo.close()


    def arquivo_validacao_json(self, errosEncontrado, site):
        arquivo = open(f"Projetos/JSON/{self.url_projeto_mpitemporario(site)}.json", 'w', encoding='utf-8')
        json.dump(errosEncontrado, arquivo, indent=4)
        arquivo.close()


    def ler_json(self, site):
        arquivoJson = open(f"Projetos/JSON/{site}.json", "r", -1, "utf-8")
        dados = arquivoJson.read()
        return json.loads(dados)


    def lista_arquivos_json(self):
        listaArquivos = listdir('Projetos/JSON/')
        for keys, arquivo in enumerate(listaArquivos):
            if 'json' not in arquivo:
                del listaArquivos[keys]
        return listaArquivos


