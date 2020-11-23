from .Class.Config import *
from .Class.Validador import *
from .Arquivo import Arquivo
from colorama import Fore, Style, init
from requests_html import HTMLSession
from tqdm.auto import tqdm
from random import sample
import threading

init(autoreset=True)


def Validador(DEFAULT=True):

    ListLog = []

    session = HTMLSession()

    print(Fore.WHITE + "\nAmbiente em preparação, aguarde um momento...")

    if validation["w3c"]:
        w3c = W3c(errosEncontrado[ERRO_W3C], erroValidacao[ERRO_VALIDACAO_W3C])

    if validation["colunaLateral"]:
        colunaLateral = ColunaLateral(
            errosEncontrado[ERRO_COLUNA_LATERAL],
            erroValidacao[ERRO_VALIDACAO_COLUNA_LATERAL],
        )

    if validation["mapaDoSite"]:
        mapaDoSite = MapaDoSite(
            errosEncontrado[ERRO_MAPA_SITE],
            erroValidacao[ERRO_VALIDACAO_MAPA_SITE],
        )

    if validation["menu"]:
        menu = MenuHeaderFooter(
            errosEncontrado[ERRO_MENU], erroValidacao[ERRO_VALIDACAO_MENU]
        )

    if validation["pageSpeed"]:
        pageSpeed = PageSpeed(
            errosEncontrado[ERRO_PAGESPEED], erroValidacao[ERRO_VALIDACAO_PAGESPEED]
        )

    if validation["texto"]:
        texto = Texto(errosEncontrado[ERRO_TEXTO], erroValidacao[ERRO_VALIDACAO_TEXTO])

    if validation["description"]:
        description = Description(
            errosEncontrado[ERRO_DESCRIPTION_1],
            errosEncontrado[ERRO_DESCRIPTION_2],
            erroValidacao[ERRO_VALIDACAO_DESCRIPTION],
        )

    if validation["imagem"]:
        imagem = Imagens(
            errosEncontrado[ERRO_IMAGENS_1],
            errosEncontrado[ERRO_IMAGENS_2],
            errosEncontrado[ERRO_IMAGENS_3],
            erroValidacao[ERRO_VALIDACAO_IMAGENS],
        )

    if validation["title"]:
        title = Title(
            errosEncontrado[ERRO_TITLE_1],
            errosEncontrado[ERRO_TITLE_2],
            errosEncontrado[ERRO_TITLE_3],
            errosEncontrado[ERRO_TITLE_4],
            errosEncontrado[ERRO_TITLE_5],
            erroValidacao[ERRO_VALIDACAO_TITLE],
        )

    if validation["mpi"]:
        mpi = Mpi(
            errosEncontrado[ERRO_MPI_1],
            errosEncontrado[ERRO_MPI_2],
            errosEncontrado[ERRO_MPI_3],
            errosEncontrado[ERRO_MPI_4],
            errosEncontrado[ERRO_MPI_5],
            errosEncontrado[ERRO_MPI_6],
            errosEncontrado[ERRO_MPI_7],
            erroValidacao[ERRO_VALIDACAO_MPI],
        )

    if validation["scrollHorizontal"]:
        scrollHorizontal = ScrollHorizontal(
            errosEncontrado[ERRO_SCROLL], erroValidacao[ERRO_VALIDACAO_SCROLL]
        )

    arquivo = Arquivo()

    def Urls():
        sites = open("sites.txt", "r")
        linha = sites.readlines()
        arrayUrl = []
        for url in linha:
            arrayUrl.append(url.strip("\n").strip(" "))

        sites.close()
        return arrayUrl

    urls = Urls()

    for Url in Array["validation"].keys():
        if Array["validation"][Url]:
            print(
                Fore.WHITE
                + " Status: "
                + Fore.GREEN
                + "ON"
                + Fore.WHITE
                + " Módulo: {}".format(Url)
            )
        else:
            print(
                Fore.WHITE
                + " Status: "
                + Fore.RED
                + "OFF"
                + Fore.WHITE
                + " Módulo: {}".format(Url)
            )

    print(Fore.WHITE + " Ambiente configurado com sucesso.")

    if len(urls) > 0:

        print(Fore.WHITE + f"\nForam recuperados ({len(urls)}) projetos para validação")

        for key, url in enumerate(urls):
            print(f" [{key + 1}] {url}")

        try:

            for url in urls:

                Page_Exists = False
                r = session.get(url)

                try:
                    if r.html.find("head title")[0].text.split(" ")[0] != "404":
                        Page_Exists = True
                except:
                    print(Fore.YELLOW + f"\nAviso: {ERRO[416]}")

                finally:

                    if Page_Exists:

                        print(Fore.YELLOW + f"\nProjeto em validação => {url}")

                        links = Links(
                            url,
                            errosEncontrado[ERRO_LINK],
                            erroValidacao[ERRO_VALIDACAO_LINK],
                            DEFAULT,
                        ).links_site()

                        msm = Fore.GREEN + "Validação em andamento"

                        for pagina in tqdm(links["Todos"], desc=msm):
                            item = Item(pagina, erroValidacao[ERRO_VALIDACAO_ITEM])

                            if validation["w3c"]:
                                threading.Thread(
                                    target=w3c.verifica, args=(pagina,)
                                ).start()

                            if validation["texto"]:
                                threading.Thread(
                                    target=texto.verifica,
                                    args=(
                                        pagina,
                                        item.texto_pagina(),
                                    ),
                                ).start()

                            if validation["imagem"]:
                                threading.Thread(
                                    target=imagem.verifica,
                                    args=(
                                        pagina,
                                        item.imagens(),
                                    ),
                                ).start()

                            if validation["colunaLateral"]:
                                threading.Thread(
                                    target=colunaLateral.verifica,
                                    args=(
                                        pagina,
                                        item.aside_links(),
                                    ),
                                ).start()

                            if validation["description"]:
                                threading.Thread(
                                    target=description.verifica,
                                    args=(
                                        pagina,
                                        item.description(),
                                        item.h1(),
                                    ),
                                ).start()

                            if validation["mapaDoSite"]:
                                threading.Thread(
                                    target=mapaDoSite.verifica,
                                    args=(
                                        pagina,
                                        links["Mapa Site"],
                                    ),
                                ).start()

                            if validation["title"]:
                                threading.Thread(
                                    target=title.verifica,
                                    args=(
                                        pagina,
                                        item.h1(),
                                        item.h2(),
                                        item.titulo_strong(),
                                        item.h3(),
                                    ),
                                ).start()

                            if validation["scrollHorizontal"]:
                                scrollHorizontal.verifica(pagina)

                            if pagina in links["MPI"]:
                                if validation["mpi"]:
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
                                        ),
                                    ).start()

                            if pagina == url:
                                if validation["menu"]:
                                    threading.Thread(
                                        target=menu.verifica,
                                        args=(
                                            item.menu_top_texts(),
                                            item.menu_footer_texts(),
                                            item.menu_top_links(),
                                            item.menu_footer_links(),
                                        ),
                                    ).start()

                                if validation["pageSpeed"]:
                                    try:
                                        random = sample(range(0, len(links["MPI"])), 3)
                                        pageSpeed.verifica(
                                            [
                                                pagina,
                                                links["MPI"][random[0]],
                                                links["MPI"][random[1]],
                                                links["MPI"][random[2]],
                                            ]
                                        )
                                    except:
                                        ListLog.append(url)

                        arquivo.arquivo_validacao_json(errosEncontrado, url)
                        arquivo.arquivo_validacao(errosEncontrado, erroValidacao, url)

                        print(Fore.WHITE + f"Validação do projeto concluída.")

                    else:
                        print(Fore.WHITE + f"{ERRO[414]}")

        except:
            print(ERRO[501])

        finally:
            if validation["scrollHorizontal"]:
                scrollHorizontal.fechar()

            if len(ListLog) > 0:
                print("\n" + ERRO[505])
                for projetos in ListLog:
                    print(f" => {projetos}")

    else:
        print(
            Fore.YELLOW
            + '\nAviso: Você não possui projetos para validar.\nDigite "sites" para adicionar novos projetos.'
        )
