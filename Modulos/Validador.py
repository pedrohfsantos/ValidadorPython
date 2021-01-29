from .Class.Config import *
from .Class.Validador import *
from .Arquivo import Arquivo
from colorama import Fore, Style, init
from requests_html import HTMLSession
from tqdm.auto import tqdm
from random import sample
import threading, os

init(autoreset=True)


def Validador(DEFAULT=True, RastrearImagens=False, hist=False):

    list_log = []

    session = HTMLSession()

    print(Fore.WHITE + "\nAmbiente em preparação, aguarde um momento...")

    if validation["w3c"]:
        w3c = W3c(erros_encontrado[ERRO_W3C], erro_validacao[ERRO_VALIDACAO_W3C])

    if validation["coluna_lateral"]:
        coluna_lateral = ColunaLateral(
            erros_encontrado[ERRO_COLUNA_LATERAL],
            erro_validacao[ERRO_VALIDACAO_COLUNA_LATERAL],
        )

    if validation["mapa_do_site"]:
        mapa_do_site = MapaDoSite(
            erros_encontrado[ERRO_MAPA_SITE],
            erro_validacao[ERRO_VALIDACAO_MAPA_SITE],
        )

    if validation["menu"]:
        menu = MenuHeaderFooter(erros_encontrado[ERRO_MENU], erro_validacao[ERRO_VALIDACAO_MENU])

    if validation["page_speed"]:
        page_speed = PageSpeed(erros_encontrado[ERRO_PAGESPEED], erro_validacao[ERRO_VALIDACAO_PAGESPEED])

    if validation["texto"]:
        texto = Texto(erros_encontrado[ERRO_TEXTO], erro_validacao[ERRO_VALIDACAO_TEXTO])

    if validation["description"]:
        description = Description(
            erros_encontrado[ERRO_DESCRIPTION_1],
            erros_encontrado[ERRO_DESCRIPTION_2],
            erro_validacao[ERRO_VALIDACAO_DESCRIPTION],
        )

    if validation["imagem"]:
        imagem = Imagens(
            erros_encontrado[ERRO_IMAGENS_1],
            erros_encontrado[ERRO_IMAGENS_2],
            erros_encontrado[ERRO_IMAGENS_3],
            erro_validacao[ERRO_VALIDACAO_IMAGENS],
        )

    if validation["title"]:
        title = Title(
            erros_encontrado[ERRO_TITLE_1],
            erros_encontrado[ERRO_TITLE_2],
            erros_encontrado[ERRO_TITLE_3],
            erros_encontrado[ERRO_TITLE_4],
            erros_encontrado[ERRO_TITLE_5],
            erro_validacao[ERRO_VALIDACAO_TITLE],
        )

    if validation["mpi"]:
        mpi = Mpi(
            erros_encontrado[ERRO_MPI_1],
            erros_encontrado[ERRO_MPI_2],
            erros_encontrado[ERRO_MPI_3],
            erros_encontrado[ERRO_MPI_4],
            erros_encontrado[ERRO_MPI_5],
            erros_encontrado[ERRO_MPI_6],
            erros_encontrado[ERRO_MPI_7],
            erro_validacao[ERRO_VALIDACAO_MPI],
        )

    if validation["scroll_horizontal"]:
        scroll_horizontal = ScrollHorizontal(erros_encontrado[ERRO_SCROLL], erro_validacao[ERRO_VALIDACAO_SCROLL])

    arquivo = Arquivo()
    urls = arquivo.ler_urls_sitesTXT()

    if len(urls) > 0:

        for Url in Array["validation"].keys():
            if Array["validation"][Url]:
                print(Fore.WHITE + " Status: " + Fore.GREEN + "ON" + Fore.WHITE + " -> {}".format(Url))
            else:
                print(Fore.WHITE + " Status: " + Fore.RED + "OFF" + Fore.WHITE + " -> {}".format(Url))

        print(" Ambiente configurado com sucesso.")

        print(
            f"\nForam recuperados ({len(urls)}) projetos para validação\n{arquivo.listar(urls)}"
        ) if not hist else None

        try:

            for url in urls:

                if not hist:
                    arquivo.historico_validacao(url)
                else:
                    array_json = arquivo.ler_json(caminho="./Modulos/WebCache/__hist")

                    try:
                        print(f"\nForam recuperados ({len(array_json)}) projetos através do histórico de validação")
                        for num, item in enumerate(array_json):
                            print(f"[{num + 1 }] {item}")
                        print(Fore.YELLOW + "\nSelecione um projeto: ")
                        opcao = int(input("$ "))
                        if opcao not in range(0, len(array_json) + 1):
                            print(ERRO[503])
                        else:
                            url = array_json[opcao - 1]

                    except Exception as erro:
                        print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-")
                        return None

                page_exists = False
                r = session.get(url)

                try:
                    if r.html.find("head title")[0].text.split(" ")[0] != "404":
                        page_exists = True

                except Exception as erro:
                    print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-")
                    print(Fore.YELLOW + f"\nAviso: {ERRO[416]}")

                finally:

                    if page_exists:

                        print(Fore.YELLOW + f"\nProjeto em validação => {url}")

                        try:

                            if os.path.isfile(
                                f"./Modulos/WebCache/{arquivo.url_projeto_mpitemporario(url)}__cache.json"
                            ):
                                cache_links = str(
                                    input(" Você deseja utilizar o cache dos links da validação anterior? (y / n): ")
                                ).lower()
                                if cache_links in ["n", "y"]:
                                    links = (
                                        Links(
                                            url,
                                            erros_encontrado[ERRO_LINK],
                                            erro_validacao[ERRO_VALIDACAO_LINK],
                                            DEFAULT,
                                        ).links_site
                                        if "n" in cache_links
                                        else arquivo.ler_json(
                                            caminho=f"./Modulos/WebCache/{arquivo.url_projeto_mpitemporario(url)}__cache",
                                            validacao_json=False,
                                        )
                                    )
                                print(cache_links)
                            else:
                                links = Links(
                                    url, erros_encontrado[ERRO_LINK], erro_validacao[ERRO_VALIDACAO_LINK], DEFAULT
                                ).links_site

                            msm = Fore.GREEN + " Validação em andamento"

                            create_file = True

                            for pagina in tqdm(links["Todos"], desc=msm, unit=" links", leave=False):
                                item = Item(pagina, erro_validacao[ERRO_VALIDACAO_ITEM])

                                if validation["w3c"]:
                                    threading.Thread(target=w3c.verifica, args=(pagina,)).start()

                                if validation["texto"]:
                                    threading.Thread(
                                        target=texto.verifica,
                                        args=(
                                            pagina,
                                            item.texto_pagina,
                                        ),
                                    ).start()

                                if validation["imagem"]:
                                    threading.Thread(
                                        target=imagem.verifica,
                                        args=(
                                            pagina,
                                            item.imagens,
                                        ),
                                    ).start()

                                if validation["coluna_lateral"]:
                                    threading.Thread(
                                        target=coluna_lateral.verifica,
                                        args=(
                                            pagina,
                                            item.aside_links,
                                        ),
                                    ).start()

                                if validation["description"]:
                                    threading.Thread(
                                        target=description.verifica,
                                        args=(
                                            pagina,
                                            item.description,
                                            item.h1,
                                        ),
                                    ).start()

                                if validation["mapa_do_site"]:
                                    threading.Thread(
                                        target=mapa_do_site.verifica,
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
                                            item.h1,
                                            item.h2,
                                            item.titulo_strong,
                                            item.h3,
                                        ),
                                    ).start()

                                if validation["scroll_horizontal"]:
                                    scroll_horizontal.verifica(pagina)

                                if pagina in links["MPI"]:
                                    if validation["mpi"]:
                                        threading.Thread(
                                            target=mpi.verifica,
                                            args=(
                                                pagina,
                                                item.description,
                                                item.imagens_mpi,
                                                item.h1,
                                                item.h2_mpi,
                                                item.paragrafos_mpi,
                                                item.imagens_mpi,
                                            ),
                                        ).start()

                                if pagina == url:
                                    if validation["menu"]:
                                        threading.Thread(
                                            target=menu.verifica,
                                            args=(
                                                item.menu_top_texts,
                                                item.menu_footer_texts,
                                                item.menu_top_links,
                                                item.menu_footer_links,
                                            ),
                                        ).start()

                                    if validation["page_speed"]:
                                        try:
                                            random = sample(range(0, len(links["MPI"])), 3)
                                            page_speed.verifica(
                                                [
                                                    pagina,
                                                    links["MPI"][random[0]],
                                                    links["MPI"][random[1]],
                                                    links["MPI"][random[2]],
                                                ]
                                            )
                                        except Exception as erro:
                                            print(
                                                f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-"
                                                if developer
                                                else f"{ Fore.RED }MPI: Não foi possível resgatar nenhuma palavra-chave."
                                            )
                                            create_file = False
                                            break

                            if create_file:
                                # arquivo.arquivo_validacao_json(erros_encontrado, url)
                                arquivo.arquivo_validacao(erros_encontrado, erro_validacao, url, json=True)

                                print(
                                    Fore.GREEN + " OK" + Fore.WHITE + f" -> Validação do projeto."
                                    if create_file
                                    else Fore.RED + " ERRO" + Fore.WHITE + f" -> {ERRO[505]}."
                                )

                        except Exception as erro:
                            print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-" if developer else None)
                            break

                    else:
                        print(
                            f"{Fore.YELLOW}\nProjeto em validação => {url}\n{Fore.RED} 404{Fore.WHITE} -> {ERRO[414]}"
                        )

        except Exception as erro:
            print(ERRO[501])
            print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-" if developer else None)

        finally:
            if validation["scroll_horizontal"]:
                scroll_horizontal.fechar

            if len(list_log) > 0:
                print("\n" + ERRO[505])
                for projetos in list_log:
                    print(f" => {projetos}")
    else:
        print(
            Fore.YELLOW
            + '\nAviso: Você não possui projetos para validar.\nDigite "sites" para adicionar novos projetos.'
        )