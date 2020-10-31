from bs4 import BeautifulSoup
from os import listdir
from pathlib import Path
import json
import re
import os.path

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


    def ler_json(self, site):
        with open(f'Projetos/JSON/{site}.json', 'r', encoding='utf-8') as arquivoJson:
            dados = arquivoJson.read()
            return json.loads(dados)


    def lista_arquivos_json(self):
        listaArquivos = listdir('Projetos/JSON/')
        for keys, arquivo in enumerate(listaArquivos):
            if 'json' not in arquivo:
                del listaArquivos[keys]
        return listaArquivos

    def ler_arquivo(f):
        content = []

        try:
            with open(f + '.php', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for elem in lines:
                    content.append(elem)                    
                return ''.join(map(str, content))
        except IOError:
            return False    
    
    elements = []

    def mascara(body, status):

        subsmask = '!!!PHP!!!'

        def remove(d):
            elements.append(d.group())
            return subsmask
        def adiciona(e):
            return elements.pop(0)
        
        try:            
            m = re.sub(r"<\?.*\?>", remove, body)
            soup = BeautifulSoup(m, "html.parser")
            mask = re.sub(subsmask, remove, str(soup.prettify(formatter=None))) if status else re.sub(subsmask, adiciona, str(soup.prettify(formatter=None)))
        except:
            mask = False

        return mask
    
    def create(body, arquivo, funcao):
        
        arquivo = projeto + '/' + funcao + '/' + arquivo        
        try:

            Path(f'./projetos/{projeto}/{funcao}/').mkdir(parents=True, exist_ok=True)
            with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:
                f.write(body)
                f.write('</html>')

        except: 
            return 'Não possível gerar o arquivo.'