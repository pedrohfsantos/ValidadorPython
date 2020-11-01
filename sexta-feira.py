from Modulos.Validador import Validador
from Modulos.Ajustador import Ajustador
from Modulos.Arquivo import Arquivo
from colorama import Fore, Style, init
from datetime import datetime
from Modulos.Class.Config import *
import os

json = Arquivo()

# Colorama, auto resetar para White color
init(autoreset=True)
argumento   = ''
clear       = lambda: os.system('cls')

# Mensagem de apresentação
Message     = '\nBem vindo ao Sexta-feira!\nPara melhor experiência, inicialize no Git Bash.\n'

def Info():
    print('Versão atual: 1.0.1')
    print('Este terminal é exclusivo para interação com projetos em publicação.')
    print('Projeto em desenvolvimento. Estado de versão no momento: beta e atualmente alocado em pedrohfsantos/ValidadorPython no GitHub.')
    print('Digite "info" para visualizar esta aba novamente.')
    print('\nComandos de execução')
    print(' -v       Inicia o módulo de validação.')
    print(' -a       Inicia o módulo de ajustes.           [BETA]')
    print('Comandos de atalho')
    print(' sites    Abre o arquivo sites.txt              [ext] [GIT BASH]')
    print(' info     Exibe a lista completa de comandos.')
    print(' clear    Limpa o terminal.')
    print(' exit     Encerra o programa.')

print(Message)

while 'exit' not in argumento.lower():

    if os.path.isfile('./Config.json'):

        if json.ler_json(False, './Config')['localhost'] == '' and json.ler_json(False, './Config')['binary'] == '':
            print(Fore.YELLOW + 'Especifique o caminho do seu htdocs')
            htdocs = str(input('$ '))
            Array['localhost'] = htdocs
            json.escreve_json(Array)
            print('\n')

            print(Fore.YELLOW + 'Especifique o caminho do seu firefox.exe')
            firefox = str(input('$ '))
            Array['binary'] = firefox
            json.escreve_json(Array)
            print('\n')

        print(Fore.YELLOW + 'Digite "info" para obter a lista de comandos nativos')
        argumento = input('$ ').lower()

        if argumento  == 'info':
            Info()
            print('\n')

        elif argumento == '-v':
            Validador()
            print('\n')

        elif argumento == '-a':    
            Ajustador()

        elif argumento == 'sites':
            os.system('nano sites.txt')
            print('\n')

        elif argumento == 'clear':
            clear()
            print(Message)

        else:
            print(f'$ {argumento}: ' + ERRO[302] if len(argumento) > 0 and argumento != 'exit' else '')

    else:
        json.escreve_json(Array)