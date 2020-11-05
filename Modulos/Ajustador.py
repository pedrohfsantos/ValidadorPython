from .Class.Config import *
from .Class.Ajustador import *
from .Arquivo import Arquivo
from .Class.Construct import *
from requests_html import HTMLSession
from tqdm.auto import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

def Ajustador():
    session = HTMLSession()

    erroAjusta = {
        'Description' : [],
        'Imagem' : [],
        'Palavra chave sem strong': [],
        'Titulo (H2/H3) igual H1': [],
        'Titulo duplicado': [],
    }

    description       = Description(erroAjusta['Description'])
    imagem            = Imagem(erroAjusta['Imagem'])
    strong            = Strong(erroAjusta['Palavra chave sem strong'])
    titulo_duplicado  = TituloDuplicado(erroAjusta['Titulo (H2/H3) igual H1'])
    sequencia_h2      = SequenciaH2(erroAjusta['Titulo duplicado'])
    arquivo           = Arquivo()  
    mascara           = Mascara()    

    arquivos = arquivo.lista_arquivos_json()

    if len(arquivos) > 0:
        for key, value in enumerate(arquivos):
            if len(arquivos) > 0:
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

        print('Realizando backup dos arquivos...')
        arquivo.backup(site=site, erros=[
            ERRO_MPI_3,
            # ERRO_IMAGENS_2,
            ERRO_MPI_6,
            ERRO_TITLE_3,
            ERRO_TITLE_4
        ])


        def Inicializa(site, url, erro, modulo):

            def Clear(url):
                url = url.split('//')[1].split('/')[-1].split(' ')[0]
                return url

            def Modulo(modulo):
                return {
                    'strong'            :strong.ajusta(html, url, r),
                    'sequencia_h2'      :sequencia_h2.ajusta(html, url),
                    'titulo_duplicado'  :titulo_duplicado.ajusta(html, url, r)
                }[modulo]

            caminho = site + '/' + Clear(url)
            r       = session.get(URL + caminho)
            html    = arquivo.ler_arquivo(localhost + caminho)
            if html:
                body = Modulo(modulo)
                if body != None:
                    arquivo.criar_arquivo(body, site, erro, Clear(url), localhost, html, False)
                else:
                    erroAjusta[erro].append('=> {}'.format(Clear(url)))
                mascara.reset()
            else:
                print(ERRO[404])


        if len(urls[ERRO_MPI_3]) > 0:
            print(Fore.YELLOW + f'\nIniciando ajustes de {ERRO_MPI_3}...')
            try:
                for url in tqdm(urls[ERRO_MPI_3]):
                    r = session.get(url)
                    description.ajusta(site, url, r)
            except:
                print(ERRO[303])


        if len(urls[ERRO_IMAGENS_2]) > 0:
            print(Fore.YELLOW + f'\nIniciando ajustes de {ERRO_IMAGENS_2}...')
            try:
                for url in tqdm(urls[ERRO_IMAGENS_2]):
                    imagem.ajusta(site, url)
            except:
                print(ERRO[303])


        if len(urls[ERRO_MPI_6]) > 0:
            print(Fore.YELLOW + f'\nIniciando ajustes de {ERRO_MPI_6}...')
            try:
                for url in tqdm(urls[ERRO_MPI_6]):
                    Inicializa(site.strip(), url.strip(), ERRO_MPI_6, modulo='strong')
            except:
                print(ERRO[303])


        if len(urls[ERRO_TITLE_3]) > 0:
            print(Fore.YELLOW + f'\nIniciando ajustes de {ERRO_TITLE_3}...')
            try:
                for url in tqdm(urls[ERRO_TITLE_3]):
                    Inicializa(site.strip(), url.strip(), ERRO_TITLE_3, 'titulo_duplicado')
            except:
                print(ERRO[303])


        if len(urls[ERRO_TITLE_4]) > 0:
            print(Fore.YELLOW + f'\nIniciando ajustes de {ERRO_TITLE_4}...')
            try:
                for url in tqdm(urls[ERRO_TITLE_4]):
                    Inicializa(site.strip(), url.strip(), ERRO_TITLE_4, 'sequencia_h2')
            except:
                print(ERRO[303])


        log = False
        for erro in erroAjusta.keys():
            if len(erroAjusta[erro]) > 0:
                log = True
                break

        if len(erroAjusta[erro]) > 0:
            print(Fore.RED + ERRO[504] + '\n')
            for errosItens in erroAjusta.keys():
                if len(erroAjusta[errosItens]) > 0:
                    print(f'{errosItens}:\n')

                    for errosValores in erroAjusta[errosItens]:
                        print(f'{errosValores}')
                    print('\n')

                erroAjusta[errosItens].clear()

    else:
        print(Fore.YELLOW + 'Aviso: Você não possui projetos para ajustar.\n')