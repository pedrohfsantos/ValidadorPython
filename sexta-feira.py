import os
from Modulos.Validador import Validador
from Modulos.Ajustador import Ajustador
from Modulos.Arquivo import Arquivo
from colorama import Fore, Style, init
from Modulos.Class.Config import *

# Colorama, auto resetar para White color
arquivo = Arquivo()
init(autoreset=True)
argumento = ""
clear = lambda: os.system("cls")

# Mensagem de apresentação
Message = "\nBem vindo ao Sexta-feira!\n"


def Info():
    print("\nVersão atual: 1.0.5")
    print("Este terminal é exclusivo para interação com projetos em publicação.")
    print(
        "Projeto em desenvolvimento. Estado de versão no momento: beta e atualmente alocado em pedrohfsantos/ValidadorPython no GitHub."
    )
    print('Digite "info" para visualizar esta aba novamente.')
    print("\n* Os níveis de precisão do validador é representado por baixo [B] e alto [A].")
    print("\nComandos de execução\n")
    print(" -a              Inicia o módulo de ajustes.          [A] [BETA]")
    print(" -v              Inicia o módulo de validação.        [A]")
    print(" -vf             Para validações rápidas.             [B]")
    print(" -v hist         Inicia o módulo de validação através do histórico. [A]")
    print(" -v open         Abrir o arquivo .txt via notepad.")
    print(" -v open [arg]   Digite [chrome] como argumento para abrir no navegador.")
    print("                 Digite [chrome] [-l] para abrir o .txt e o projeto localhost.")
    print("\nComandos de atalho\n")
    print(" clear           Limpa o terminal.")
    print(" clear cache     Limpar o cache das validações")
    print(" exit            Encerra o programa.")
    print(" info            Exibe a lista completa de comandos.")
    print(" sites           Abre o arquivo sites.txt")
    print(" var             Exibir variáveis do sistema, Config.json")


print(Message)

while "exit" not in argumento.lower().strip():

    if os.path.isfile("./Config.json"):
        if arquivo.ler_json(False, "./Config")["localhost"] == "":
            print(Fore.YELLOW + "Especifique o caminho do seu htdocs")

            htdocs = str(input("$ "))
            htdocs = htdocs if htdocs[-1] == "\\" else htdocs + "\\"
            Array["localhost"] = htdocs
            arquivo.escreve_json(Array)
            print("\n")

        print(Fore.YELLOW + 'Digite "info" para obter a lista de comandos nativos')
        argumento = input("$ ").lower().strip()

        if argumento == "info":
            Info()
            print("\n")

        elif argumento == "-v" or argumento == "-vf":
            Validador(False) if "f" in argumento else Validador()
            print("\n")

        elif argumento == "-v hist":
            Validador(False, hist=True)
            print("\n")

        elif argumento == "-a":
            Ajustador()
            print("\n")

        elif argumento == "sites":
            os.system("notepad sites.txt")
            print("\n")

        elif argumento == "clear":
            os.system("clear")
            clear()
            print(Message)

        elif argumento == "clear cache":
            arquivo.limpa_cache()

        elif argumento == "var":
            arquivo.variaveis_sistema(Array)

        elif "-v open" == argumento or "-v open chrome" == argumento or "-v open chrome -l" == argumento:
            argl = True if " -l" in argumento else False
            arquivo.Open(argumento, arquivo.lista_arquivos_json(pasta="Validação", ext="txt"), localhost=argl)
            print("\n")

        else:
            print(f"$ {argumento}: {ERRO[302]}\n" if len(argumento) > 0 and argumento != "exit" else "")

    else:
        arquivo.escreve_json(Array)