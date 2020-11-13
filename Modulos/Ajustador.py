from .Class.Config import *
from .Class.Ajustador import *
from .Arquivo import Arquivo
from requests_html import HTMLSession
from tqdm.auto import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

def Ajustador():

    session = HTMLSession()

    Switch = {
        'Description'               : True,     
        'Imagem'                    : True,     
        'Strong'                    : True,     
        'Titulo duplicado'          : False,    
        'Sequência de H2'           : False,     
    }

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

        print('\nIniciando ajustes no projeto...')

        arquivo.backup(site=site, erros=[
            ERRO_MPI_3,
            # ERRO_IMAGENS_2,
            ERRO_MPI_6,
            ERRO_TITLE_3,
            ERRO_TITLE_4
        ])


        erroInicializa = []

        def Inicializa(site, url, erro, modulo):

            def Clear(url):
                url = re.search(r'http.*?\S*[^: ]', url).group(0).split('//')[1].split('/')[-1].split(' ')[0]
                return url

            def Modulo(modulo):
                return {
                    'strong'            :strong.ajusta(html, url, r),
                    'titulo_duplicado'  :titulo_duplicado.ajusta(html, url, r),
                    'sequencia_h2'      :sequencia_h2.ajusta(html, url)
                }[modulo]

            caminho = site + '/' + Clear(url)
            r       = session.get(urlmpitemporario + caminho)
            html    = arquivo.ler_arquivo(localhost + caminho)
            if html:
                body = Modulo(modulo)
                # print(body)
                if body != None:
                    arquivo.criar_arquivo(body, site, erro, Clear(url), localhost, html, False)
                else:
                    erroAjusta[erro].append('=> {}'.format(Clear(url)))
            else:
                erroInicializa.append('{} => {}'.format(caminho, ERRO[404]))


        if Switch['Description']:
            if len(urls[ERRO_MPI_3]) > 0:
                try:
                    for url in tqdm(urls[ERRO_MPI_3], desc=ERRO_MPI_3):
                        r = session.get(url)
                        description.ajusta(site, url, r)
                except:
                    print(ERRO[303])


        if Switch['Imagem']:
            if len(urls[ERRO_IMAGENS_2]) > 0:
                try:
                    for url in tqdm(urls[ERRO_IMAGENS_2], desc=ERRO_IMAGENS_2):
                        imagem.ajusta(site, url)
                except:
                    print(ERRO[303])


        if Switch['Strong']:
            if len(urls[ERRO_MPI_6]) > 0:
                try:
                    for url in tqdm(urls[ERRO_MPI_6], desc=ERRO_MPI_6):
                        f = url.find(' - ')
                        r = session.get(url[:f])
                        strong.ajusta(site, url[:f], r)
                except:
                    print(ERRO[303])


        if Switch['Titulo duplicado']:
            if len(urls[ERRO_TITLE_3]) > 0:
                try:
                    for url in tqdm(urls[ERRO_TITLE_3], desc=ERRO_TITLE_3):
                        Inicializa(site.strip(), url.strip(), ERRO_TITLE_3, modulo='titulo_duplicado')
                except:
                    print(ERRO[303])


        if Switch['Sequência de H2']:
            if len(urls[ERRO_TITLE_4]) > 0:
                try:
                    for url in tqdm(urls[ERRO_TITLE_4], desc=ERRO_TITLE_4):
                        Inicializa(site.strip(), url.strip(), ERRO_TITLE_4, modulo='sequencia_h2')
                except:
                    print(ERRO[303])

                    
        print('Ajustes realizados com sucesso.')

        log = False
        for erro in erroAjusta.keys():
            if len(erroAjusta[erro]) > 0:
                log = True
                break

        if len(erroInicializa) > 0:
            print(Fore.YELLOW + 'Aviso: Arquivos não localizados:\n')
            for Erros in erroInicializa:
                print('../ ' + Erros)

        if len(erroAjusta[erro]) > 0:
            print(Fore.YELLOW + ERRO[504] + '\n')
            for errosItens in erroAjusta.keys():
                if len(erroAjusta[errosItens]) > 0:
                    print(f' {errosItens}:\n')

                    for errosValores in erroAjusta[errosItens]:
                        print(f'   {arquivo.limpa_url(site, errosValores)}')

                erroAjusta[errosItens].clear()


    else:
        print(Fore.YELLOW + 'Aviso: Você não possui projetos para ajustar.\n')