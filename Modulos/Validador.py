from .Class.Config import *
from .Class.Validador import *
from .Arquivo import Arquivo
from colorama import Fore, Style, init
from requests_html import HTMLSession
from tqdm.auto import tqdm
from random import sample
import threading
init(autoreset=True)

def Validador():

    session = HTMLSession()

    print(Fore.YELLOW + "\nAmbiente em preparação, aguarde um momento...")

    if validation['w3c']:
        w3c = W3c(
            errosEncontrado[ERRO_W3C],
            erroValidacao[ERRO_VALIDACAO_W3C]
        )

    if validation['colunaLateral']:
        colunaLateral = ColunaLateral(
            errosEncontrado[ERRO_COLUNA_LATERAL],
            erroValidacao[ERRO_VALIDACAO_COLUNA_LATERAL]
        ) 

    if validation['mapaDoSite']:
        mapaDoSite = MapaDoSite(
            errosEncontrado[ERRO_MAPA_SITE],
            erroValidacao[ERRO_VALIDACAO_MAPA_SITE],
        ) 
    
    if validation['menu']:
        menu = MenuHeaderFooter(
            errosEncontrado[ERRO_MENU],
            erroValidacao[ERRO_VALIDACAO_MENU]
        )

    if validation['pageSpeed']:
        pageSpeed = PageSpeed(
            errosEncontrado[ERRO_PAGESPEED],
            erroValidacao[ERRO_VALIDACAO_PAGESPEED]
        ) 

    if validation['texto']:
        texto = Texto(
            errosEncontrado[ERRO_TEXTO],
            erroValidacao[ERRO_VALIDACAO_TEXTO]
        )

    if validation['description']:
        description = Description(
            errosEncontrado[ERRO_DESCRIPTION_1],
            errosEncontrado[ERRO_DESCRIPTION_2],
            erroValidacao[ERRO_VALIDACAO_DESCRIPTION]
        )

    if validation['imagem']:
        imagem = Imagens(
            errosEncontrado[ERRO_IMAGENS_1],
            errosEncontrado[ERRO_IMAGENS_2],
            errosEncontrado[ERRO_IMAGENS_3],
            erroValidacao[ERRO_VALIDACAO_IMAGENS]
        ) 

    if validation['title']:
        title = Title(
            errosEncontrado[ERRO_TITLE_1],
            errosEncontrado[ERRO_TITLE_2],
            errosEncontrado[ERRO_TITLE_3],
            errosEncontrado[ERRO_TITLE_4],
            errosEncontrado[ERRO_TITLE_5],
            erroValidacao[ERRO_VALIDACAO_TITLE]
        )

    if validation['mpi']:
        mpi = Mpi(
            errosEncontrado[ERRO_MPI_1],
            errosEncontrado[ERRO_MPI_2],
            errosEncontrado[ERRO_MPI_3],
            errosEncontrado[ERRO_MPI_4],
            errosEncontrado[ERRO_MPI_5],
            errosEncontrado[ERRO_MPI_6],
            errosEncontrado[ERRO_MPI_7],
            erroValidacao[ERRO_VALIDACAO_MPI]
        )

    if validation['scrollHorizontal']:
        scrollHorizontal = ScrollHorizontal(
            errosEncontrado[ERRO_SCROLL],
            erroValidacao[ERRO_VALIDACAO_SCROLL]
        ) 

    arquivo = Arquivo()

    def Urls():  
        sites = open('sites.txt', "r")
        linha = sites.readlines()
        arrayUrl = []
        for url in linha:
            arrayUrl.append(url.strip("\n").strip(" "))
            
        sites.close()
        return arrayUrl

    urls = Urls()

    print(Fore.GREEN + 'Ambiente configurado com sucesso.')

    if len(urls) > 0:

        print(Fore.YELLOW + f'\nForam recuperados ({len(urls)}) projetos para validar')

        for key, url in enumerate(urls):
            print(f'[{key + 1}] {url}')

        print('\n')

        try:
            for url in urls:

                if session.get(url).html.find('h1')[0].text != '404':

                    Page_Not_Found = False

                    print(Fore.YELLOW + f'Projeto em validação\n=> {url}')
                    print(Fore.YELLOW + '\nRastreando e categorizando os links... \n')

                    links = Links(
                        url,
                        errosEncontrado[ERRO_LINK],
                        erroValidacao[ERRO_VALIDACAO_LINK],
                        ).links_site()

                    print(Fore.GREEN + 'Tudo pronto!')
                    print(Fore.YELLOW +'Validação em andamento...\n')

                    for pagina in tqdm(links['Todos']):
                        item = Item(pagina, erroValidacao[ERRO_VALIDACAO_ITEM])
                        
                        threading.Thread(
                            target=texto.verifica,
                            args=(pagina, item.texto_pagina(),)).start()

                        threading.Thread(
                            target=w3c.verifica,
                            args=(pagina,)).start()

                        threading.Thread(
                            target=imagem.verifica,
                            args=(pagina, item.imagens(),)).start()

                        threading.Thread(
                            target=colunaLateral.verifica,
                            args=(pagina, item.aside_links(),)).start()

                        threading.Thread(
                            target=description.verifica,
                            args=(pagina,
                            item.description(),
                            item.h1(),
                            )).start()
                        
                        threading.Thread(
                            target=mapaDoSite.verifica,
                            args=(pagina, links['Mapa Site'],)).start()
                        
                        threading.Thread(
                            target=title.verifica,
                            args=(
                                pagina, item.h1(),
                                item.h2(),
                                item.titulo_strong(),
                                item.h3(),
                                )).start()

                        if validation['scrollHorizontal']:
                            scrollHorizontal.verifica(pagina)

                        if pagina in links['MPI']:
                            threading.Thread(
                                target=mpi.verifica,
                                args=(
                                    pagina,
                                    item.description(),
                                    item.imagens_mpi(),
                                    item.h1(),
                                    item.h2_mpi(),
                                    item.paragrafos_mpi(),
                                    item.imagens_mpi(),
                                    )).start()

                        if pagina == url:
                            threading.Thread(
                                target=menu.verifica,
                                args=(
                                    item.menu_top_texts(),
                                    item.menu_footer_texts(),
                                    item.menu_top_links(),
                                    item.menu_footer_links(),
                                    )).start()
                            
                            random = sample(range(0, len(links['MPI'])), 3)
                            pageSpeed.verifica([ 
                                pagina,
                                links['MPI'][random[0]],
                                links['MPI'][random[1]],
                                links['MPI'][random[2]]
                                ])

                else:
                    Page_Not_Found = True

                if not Page_Not_Found:
                    arquivo.arquivo_validacao_json(errosEncontrado, url)
                    arquivo.arquivo_validacao(errosEncontrado, erroValidacao, url)

                    print(Fore.YELLOW + f'\nValidação do projeto finalizada\n=> {url}\n')

                else:
                    print(Fore.YELLOW + f'{ERRO[404]} Certifique-se de que o projeto esteja devidamente alocado no servidor temporário.')
            
        except:
            print(ERRO[501])

        finally:
            if validation['scrollHorizontal']:
                scrollHorizontal.fechar()

    else:
        print(Fore.YELLOW + '\nAviso: Você não possui projetos para validar.')