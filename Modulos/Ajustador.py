from .Class.Config import *
from .Class.Ajustador import *
from requests_html import HTMLSession
from tqdm.auto import tqdm
from .Arquivo import Arquivo


def Ajustador():
    session = HTMLSession()

    erroAjusta = {
        'Description' : [],
        'Imagem' : []
    }

    description = Description(erroAjusta['Description'])
    imagem = Imagem(erroAjusta['Imagem'])
    arquivo = Arquivo()    


    print('\n=-=-=-=-=-=-=-=-=-=-=-=-= MODO AJUSTE =-=-=-=-=--=-=-=-=-=-=-=-=-=-= \n')

    arquivos = arquivo.lista_arquivos_json()

    for key, value in enumerate(arquivos):
        print(f'[{key + 1}]{value}')

    while True:
        try:
            opcao = int(input('\nEscolha qual projeto dejeta ajustar: '))
            if opcao in range(0, len(arquivos) + 1):
                break

            else:
                print('\n********** Opcao invalida, tente novamente ********** \n')
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
            description.ajusta(site, url, r)

            
    if len(urls[ERRO_IMAGENS_2]) > 0:
        print('\nAjustando Imagens')
        for url in tqdm(urls[ERRO_IMAGENS_2]):
            imagem.ajusta(site, url)



# ====================== Saida dos erros de ajuste ======================

    log = False
    for erro in erroAjusta.keys():
        if len(erroAjusta[erro]) > 0:
            log = True
            break

    if log:
        print(f"\n*********** Erro que não conseguimos ajustar :( ***********\n")
        for errosItens in erroAjusta.keys():
            if len(erroAjusta[errosItens]) > 0:
                print(f'{errosItens}: \n')

                for errosValores in erroAjusta[errosItens]:
                    print(f'=> {errosValores} \n')
                print('\n')

            erroAjusta[errosItens].clear()

    print('\n=-=-=-=-=-=-=-=-=-=-=-=-= FIM MODO AJUSTE =-=-=-=-=--=-=-=-=-=-=-=-=-= \n')
    