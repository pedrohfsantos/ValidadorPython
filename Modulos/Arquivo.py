from os import listdir, makedirs
import os.path
from datetime import datetime
from pathlib import Path
import json
import re
import shutil


class Arquivo:
    def __init__(self):
        if not os.path.isdir('./Projetos'):
            makedirs('./Projetos/JSON')

        if not os.path.isdir('./Projetos/JSON'):
            makedirs('./Projetos/JSON')

        if not os.path.isdir('./Projetos/Validação'):
            makedirs('./Projetos/Validação')

        if not os.path.isdir('./Projetos/Backup'):
            makedirs('./Projetos/Backup')

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


        with open(f'Projetos/Validação/{self.url_projeto_mpitemporario(site)}.txt', 'w', encoding='utf-8') as arquivo:

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


    def criar_arquivo(self, body, projeto, funcao, arquivo, htdocs, backup = False, subs = False):

        DIR = { 'backup' : projeto + '/' + funcao + '/' + arquivo + '.php', 'caminho'  : htdocs + projeto + '/' + arquivo + '.php' }
        Path(f'./Projetos/Backup/{projeto}/{funcao}/').mkdir(parents=True, exist_ok=True)
        body = body.replace(f'<!-- {subs} -->', f'<?={subs}?>').re.sub(r'<\?=\s*\$caminho2\s*\?>', '', body) if subs else body
        try:
            with open(DIR['caminho'], 'w', encoding='utf-8') as f:
                f.write(body)
                f.write('</html>')
            # with open('./Projetos/Backup/' + DIR['backup'], 'w', encoding='utf-8') as f:
            #     f.write(backup)
        except: 
            return False


    def backup(self, site, erros):
        urlsBackup = []

        try:
            #Cria a pasta do projeto dentro da pasta Backup (ex: site.com.br-dia-mes-ano-hora-minuto-segundo)
            now = datetime.now()
            pasta = [f'./Projetos/Backup/{site}', f'./Projetos/Backup/{site}/{now.strftime("%d-%m-%Y-%H-%M-%S")}']
            for criar in pasta:
                makedirs(criar)

            #Separa os links que serão reajustados pelo validador        
            listaUrlJson = self.ler_json(False, f'./Projetos/JSON/{site}')
            for item in listaUrlJson:
                if item in erros:
                    for url in listaUrlJson[item]:
                        urlsBackup.append(url)

            #Copia todos arquivos
            for arquivo in set(urlsBackup):
                arquivo = re.search('http.*?\S*[^: ]', arquivo).group(0)
                arquivo = 'index' if arquivo.split('/')[-1] == '' else arquivo.split('/')[-1]

                configJson = self.ler_json(False, './Config')
                arquivoOriginal = f"{configJson['localhost']}{site}/{arquivo}.php"
                shutil.copy(arquivoOriginal, pasta)

            print('Backup realizado com sucesso.')

        except:
            print('Erro: Não foi possível realizar o Backup.')
