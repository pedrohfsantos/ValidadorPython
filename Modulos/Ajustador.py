from .Class.Config import *
from .Class.Ajustador import *
from requests_html import HTMLSession
from tqdm.auto import tqdm
from .Arquivo import Arquivo
from colorama import Fore, Style, init
from .Class import Construct
init(autoreset=True)

def Ajustador():
    session = HTMLSession()

    erroAjusta = {
        'Description' : [],
        'Imagem' : [],
        'Strong': []
    }

    description = Description(erroAjusta['Description'])
    imagem      = Imagem(erroAjusta['Imagem'])
    strong      = Strong(erroAjusta['Strong'])
    arquivo     = Arquivo()    

    arquivos = arquivo.lista_arquivos_json()

    for key, value in enumerate(arquivos):
        print(f'[{key + 1}] {value}')

    while True:
        try:
            print(Fore.YELLOW + '\nSelecione um projeto para ajustar')
            opcao = int(input('$ '))
            if opcao in range(0, len(arquivos) + 1):
                break
            else:
                print(ERRO[503])
                for key, value in enumerate(arquivos):
                    print(f'[{key + 1}]{value}')
        except:
           return       
    
    site = arquivos[opcao - 1]
    site = site[:-5]
    urls = arquivo.ler_json(site)


    if len(urls[ERRO_MPI_3]) > 0:
        print(Fore.YELLOW + '\nIniciando ajustes de Description...')
        try:
            for url in tqdm(urls[ERRO_MPI_3]):
                r = session.get(url)
                description.ajusta(site, url, r)
        except:
            print(ERRO[303])

    if len(urls[ERRO_IMAGENS_2]) > 0:
        print(Fore.YELLOW + '\nIniciando ajustes de Imagens...')
        try:
            for url in tqdm(urls[ERRO_IMAGENS_2]):
                imagem.ajusta(site, url)
        except:
            print(ERRO[303])


    if len(urls[ERRO_MPI_6]) > 0:
        print(Fore.YELLOW + '\nIniciando ajustes de Strong...')
        try:
            for url in tqdm(urls[ERRO_MPI_6]):

                caminho = site.strip() + '/' + strong.arquivo(url.strip())
                html = arquivo.ler_arquivo(localhost + caminho)
                if html:
                    r = session.get(URL + caminho)
                    body = strong.ajusta(html, url, r)

                    if body != None:
                        arquivo.criar_arquivo(body, site.strip(), 'Strong', strong.arquivo(url.strip()))
                    else:
                        erroAjusta['Strong'].append('=> {}'.format(strong.arquivo(url.strip())))
                    strong.reset()
                else:
                    print(ERRO[404])
  
        except:
            print(ERRO[303])

    log = False
    for erro in erroAjusta.keys():
        if len(erroAjusta[erro]) > 0:
            log = True
            break

    if len(erroAjusta[erro]) > 0:
        print(ERRO[504])
        for errosItens in erroAjusta.keys():
            if len(erroAjusta[errosItens]) > 0:
                print(f' {errosItens}: \n')

                for errosValores in erroAjusta[errosItens]:
                    print(f'=> {errosValores} \n')
                print('\n')

            erroAjusta[errosItens].clear()