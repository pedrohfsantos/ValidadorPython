from os import listdir
from os import makedirs
from pathlib import Path
import json
import re
import os.path

class Arquivo:
    def __init__(self):
        if not os.path.isdir('./Projetos'):
            makedirs('./Projetos/JSON')

        if not os.path.isdir('./Projetos/JSON'):
            makedirs('./Projetos/JSON')


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


        with open(f'Projetos/{self.url_projeto_mpitemporario(site)}.txt', 'w', encoding='utf-8') as arquivo:

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


    def arquivo_validacao_json(self, errosEncontrado, site):
        with open(f'Projetos/JSON/{self.url_projeto_mpitemporario(site)}.json', 'w', encoding='utf-8') as arquivo:
            json.dump(errosEncontrado, arquivo, indent=4)


    def escreve_json(self, config):
        with open('./Config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)


    def ler_json(self, site = False, caminho = 'Projetos/JSON/'):
        path = caminho + site if site != False else caminho
        with open(f'{path}.json', 'r', encoding='utf-8') as arquivoJson:
            dados = arquivoJson.read()
            return json.loads(dados)


    def lista_arquivos_json(self):
        listaArquivos = listdir('Projetos/JSON/')
        for keys, arquivo in enumerate(listaArquivos):
            if 'json' not in arquivo:
                del listaArquivos[keys]
        return listaArquivos


    def ler_arquivo(self, caminho):
        content = []
        try:
            with open(caminho + '.php', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for elem in lines:
                    content.append(elem)                    
                return ''.join(map(str, content))
        except IOError:
            return False    
    

    def criar_arquivo(self, body, projeto, funcao, arquivo):
        caminho = projeto + '/' + funcao + '/' + arquivo
        try:
            Path(f'./Projetos/Ajustes/{projeto}/{funcao}/').mkdir(parents=True, exist_ok=True)
            with open(f'./Projetos/Ajustes/{caminho}' + '.php', 'w', encoding='utf-8') as f:
                f.write(body)
                f.write('</html>')
        except: 
            return False