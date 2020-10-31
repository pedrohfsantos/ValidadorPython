from .Class.Config import *
from .Class.Ajustador import *
from requests_html import HTMLSession
from tqdm.auto import tqdm
from .Arquivo import Arquivo
from colorama import Fore, Style, init

init(autoreset=True)

def Ajustador():
    session = HTMLSession()

    erroAjusta = {
        'Description' : [],
        'Imagem' : []
    }

    description = Description(erroAjusta['Description'])
    imagem      = Imagem(erroAjusta['Imagem'])
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
                print('\nNão foi possível selecionar o projeto informado \n')
                for key, value in enumerate(arquivos):
                    print(f'[{key + 1}]{value}')
        except:
           return       
    
    site = arquivos[opcao - 1]
    site = site[:-5]
    urls = arquivo.ler_json(site)

    if len(urls[ERRO_MPI_3]) > 0:
        print('\nAjustando Description')
        for url in tqdm(urls[ERRO_MPI_3]):
            r = session.get(url)
            arquivo.create(description.ajusta(site, url, r), url)

            
    if len(urls[ERRO_IMAGENS_2]) > 0:
        print('\nAjustando Imagens')
        for url in tqdm(urls[ERRO_IMAGENS_2]):
            imagem.ajusta(site, url)

# Log de ajustes

    # log = False
    # for erro in erroAjusta.keys():
    #     if len(erroAjusta[erro]) > 0:
    #         log = True
    #         break

    if len(erroAjusta[erro]) > 0:
        print(f"\nNão foi possível realizar os ajustes")
        for errosItens in erroAjusta.keys():
            if len(erroAjusta[errosItens]) > 0:
                print(f' {errosItens}: \n')

                for errosValores in erroAjusta[errosItens]:
                    print(f'=> {errosValores} \n')
                print('\n')

            erroAjusta[errosItens].clear()