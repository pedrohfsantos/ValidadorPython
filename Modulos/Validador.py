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

    print(Fore.WHITE + "\nAmbiente em preparação, aguarde um momento...")

    if validation['w3c']:
        w3c = W3c(
            errosEncontrado[ERRO_W3C],
            erroValidacao[ERRO_VALIDACAO_W3C]
        )
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: W3C")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: W3C")


    if validation['colunaLateral']:
        colunaLateral = ColunaLateral(
            errosEncontrado[ERRO_COLUNA_LATERAL],
            erroValidacao[ERRO_VALIDACAO_COLUNA_LATERAL]
        ) 
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: colunaLateral")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: colunaLateral")


    if validation['mapaDoSite']:
        mapaDoSite = MapaDoSite(
            errosEncontrado[ERRO_MAPA_SITE],
            erroValidacao[ERRO_VALIDACAO_MAPA_SITE],
        ) 
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: mapaDoSite")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: mapaDoSite")
    
    
    if validation['menu']:
        menu = MenuHeaderFooter(
            errosEncontrado[ERRO_MENU],
            erroValidacao[ERRO_VALIDACAO_MENU]
        )
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: menu")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: menu")


    if validation['pageSpeed']:
        pageSpeed = PageSpeed(
            errosEncontrado[ERRO_PAGESPEED],
            erroValidacao[ERRO_VALIDACAO_PAGESPEED]
        ) 
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: pageSpeed")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: pageSpeed")


    if validation['texto']:
        texto = Texto(
            errosEncontrado[ERRO_TEXTO],
            erroValidacao[ERRO_VALIDACAO_TEXTO]
        )
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: texto")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: texto")


    if validation['description']:
        description = Description(
            errosEncontrado[ERRO_DESCRIPTION_1],
            errosEncontrado[ERRO_DESCRIPTION_2],
            erroValidacao[ERRO_VALIDACAO_DESCRIPTION]
        )
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: description")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: description")


    if validation['imagem']:
        imagem = Imagens(
            errosEncontrado[ERRO_IMAGENS_1],
            errosEncontrado[ERRO_IMAGENS_2],
            errosEncontrado[ERRO_IMAGENS_3],
            erroValidacao[ERRO_VALIDACAO_IMAGENS]
        )
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: imagem")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: imagem") 


    if validation['title']:
        title = Title(
            errosEncontrado[ERRO_TITLE_1],
            errosEncontrado[ERRO_TITLE_2],
            errosEncontrado[ERRO_TITLE_3],
            errosEncontrado[ERRO_TITLE_4],
            errosEncontrado[ERRO_TITLE_5],
            erroValidacao[ERRO_VALIDACAO_TITLE]
        )
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: title")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: title") 


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
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: mpi")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: mpi") 


    if validation['scrollHorizontal']:
        scrollHorizontal = ScrollHorizontal(
            errosEncontrado[ERRO_SCROLL],
            erroValidacao[ERRO_VALIDACAO_SCROLL]
        ) 
        print(Fore.WHITE + " Status: " + Fore.GREEN + 'ON' + Fore.WHITE + " Módulo: scrollHorizontal")
    else:
        print(Fore.WHITE + " Status: " + Fore.RED + 'OFF' + Fore.WHITE + " Módulo: scrollHorizontal") 


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

    print(Fore.WHITE + ' Ambiente configurado com sucesso.')

    if len(urls) > 0:

        print(Fore.WHITE + f'\nForam recuperados ({len(urls)}) projetos para validação')

        for key, url in enumerate(urls):
            print(f' [{key + 1}] {url}')

        try:

            for url in urls:

                Page_Exists = False
                r = session.get(url)

                try:
                    if r.html.find('head title')[0].text.split(' ')[0] != '404':
                        Page_Exists = True
                except:
                    print(Fore.YELLOW + f'\nAviso: {ERRO[416]}')

                finally:

                    if Page_Exists:

                        print(Fore.YELLOW + f'\nProjeto em validação => {url}')
                        print(Fore.WHITE + 'Rastreando e categorizando os links...')

                        links = Links(
                            url,
                            errosEncontrado[ERRO_LINK],
                            erroValidacao[ERRO_VALIDACAO_LINK],
                            False
                            ).links_site()

                        print(Fore.WHITE + 'Tudo pronto.')
                        print(Fore.WHITE + 'Validação em andamento...')

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

                        arquivo.arquivo_validacao_json(errosEncontrado, url)
                        arquivo.arquivo_validacao(errosEncontrado, erroValidacao, url)

                        print(Fore.WHITE + f'\nValidação do projeto concluída.')

                    else:
                        print(Fore.WHITE + f'{ERRO[414]}')

        except:
            print(ERRO[501])

        finally:
            if validation['scrollHorizontal']:
                scrollHorizontal.fechar()

    else:
        print(Fore.YELLOW + '\nAviso: Você não possui projetos para validar.')