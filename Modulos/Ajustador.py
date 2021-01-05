from .Class.Config import *
from .Class.Ajustador import *
from .Arquivo import Arquivo
from requests_html import HTMLSession
from tqdm.auto import tqdm
from colorama import Fore, Style, init

init(autoreset=True)


def Ajustador():

    session = HTMLSession()

    moduloAjusta = {
        "Description": True,
        "Imagem": True,
        "Strong": True,
        "Titulo duplicado": False,
        "Sequência de H2": False,
    }

    erroAjusta = {
        "Description": [],
        "Imagem": [],
        "Palavra chave sem strong": [],
        "Titulo (H2/H3) igual H1": [],
        "Titulo duplicado": [],
    }

    description = Description(erroAjusta["Description"])
    imagem = Imagem(erroAjusta["Imagem"])
    strong = Strong(erroAjusta["Palavra chave sem strong"])
    arquivo = Arquivo()

    arquivos = arquivo.lista_arquivos_json()

    if len(arquivos) > 0:

        print("\nMódulo:" + Fore.GREEN + " Ajustador\n")

        print(arquivo.listar(arquivos))

        while True:
            try:
                print(Fore.YELLOW + "\nSelecione um projeto para ajustar")
                opcao = int(input("$ "))
                if opcao in range(0, len(arquivos) + 1):
                    break
                else:
                    print(ERRO[503])
                    for key, value in enumerate(arquivos):
                        print(f"[{key + 1}] " + value.split(".json")[0])

            except Exception as erro:
                print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-")
                return

        site = arquivos[opcao - 1]
        site = site[:-5]
        urls = arquivo.ler_json(site)

        print(Fore.YELLOW + f"\nProjeto selecionado => [{opcao}] {site}")

        if arquivo.backup(site=site, erros=[ERRO_MPI_3, ERRO_MPI_6, ERRO_TITLE_3, ERRO_TITLE_4]):
            print(Fore.GREEN + " OK " + Fore.WHITE + "-> Backup dos arquivos necessários")
        else:
            print(Fore.RED + " ERRO " + Fore.WHITE + "-> Backup dos arquivos necessários")

        if moduloAjusta["Description"]:
            if len(urls[ERRO_MPI_3]) > 0:
                try:
                    for url in tqdm(urls[ERRO_MPI_3], unit=" arquivos", desc=f" {ERRO_MPI_3}", leave=False):
                        r = session.get(url)
                        description.ajusta(site, url, r)
                    print(Fore.GREEN + " OK " + Fore.WHITE + "-> " + ERRO_MPI_3)

                except Exception as erro:
                    print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-")
                    print(Fore.RED + " ERRO " + Fore.WHITE + "-> " + ERRO_MPI_3)

        if moduloAjusta["Strong"]:
            if len(urls[ERRO_MPI_6]) > 0:
                try:
                    for url in tqdm(urls[ERRO_MPI_6], unit=" arquivos", desc=f" {ERRO_MPI_6}", leave=False):
                        f = url.find(" - ")
                        r = session.get(url[:f])
                        strong.ajusta(site, url[:f], r)
                    print(Fore.GREEN + " OK " + Fore.WHITE + "-> " + ERRO_MPI_6)

                except Exception as erro:
                    print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-")
                    print(Fore.RED + " ERRO " + Fore.WHITE + "-> " + ERRO_MPI_6)

        if moduloAjusta["Imagem"]:
            if len(urls[ERRO_IMAGENS_2]) > 0:
                try:
                    for url in tqdm(urls[ERRO_IMAGENS_2], unit=" arquivos", desc=f" {ERRO_IMAGENS_2}", leave=False):
                        imagem.ajusta(site, url)
                    print(Fore.GREEN + " OK " + Fore.WHITE + "-> " + ERRO_IMAGENS_2)
                except Exception as erro:
                    print(f"\n -> { Fore.RED }{erro}{ Fore.WHITE } <-")
                    print(Fore.RED + " ERRO " + Fore.WHITE + "-> " + ERRO_IMAGENS_2)

        print(" Módulos finalizados.")

        log = False
        for erro in erroAjusta.keys():
            if len(erroAjusta[erro]) > 0:
                log = True
                break

        if len(erroAjusta[erro]) > 0:
            print(Fore.YELLOW + ERRO[504] + "\n")
            for errosItens in erroAjusta.keys():
                if len(erroAjusta[errosItens]) > 0:
                    print(f" {errosItens}:\n")

                    for errosValores in erroAjusta[errosItens]:
                        print(f"{arquivo.limpa_url(site, errosValores)}")

                erroAjusta[errosItens].clear()

    else:
        print(Fore.YELLOW + "\nAviso: Você não possui projetos para ajustar.")
