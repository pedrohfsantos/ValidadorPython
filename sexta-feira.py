from Modulos.Validador import Validador
from Modulos.Ajustador import Ajustador
from colorama import Fore, Style, init
from datetime import datetime
import os

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

    print(Fore.YELLOW + 'Digite "info" para obter a lista de comandos nativos')
    argumento = input('$ ').lower()

    if argumento  == 'info':
        Info()
        print('\n')

    elif argumento == '-v':
        Validador()
        print('\n')

    elif argumento == '-a':
        print('\nMódulo:' + Fore.GREEN + ' Ajustador\n')
        Ajustador()

    elif argumento == 'sites':
        os.system('nano sites.txt')
        print('\n')

    elif argumento == 'clear':
        clear()
        print(Message)

    else:
        print(f'$ {argumento}: Comando inválido.\n' if len(argumento) > 0 else '')