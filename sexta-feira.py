from Modulos.Validador import Validador
from Modulos.Ajustador import Ajustador
from Modulos.Arquivo import Arquivo
from colorama import Fore, Style, init
from Modulos.Class.Config import *
import os

json = Arquivo()

# Colorama, auto resetar para White color
init(autoreset=True)
argumento   = ''
clear       = lambda: os.system('cls')

# Mensagem de apresentação
Message     = '\nBem vindo ao Sexta-feira!\n'

def Info():
    print('\nVersão atual: 1.0.4')
    print('Este terminal é exclusivo para interação com projetos em publicação.')
    print('Projeto em desenvolvimento. Estado de versão no momento: beta e atualmente alocado em pedrohfsantos/ValidadorPython no GitHub.')
    print('Digite "info" para visualizar esta aba novamente.')
    print('\n* Os níveis de precisão do validador é representado por baixo [B] e alto [A].')
    print('\nComandos de execução\n')
    print(' -a        Inicia o módulo de ajustes.   [A] [BETA]')
    print(' -v        Inicia o módulo de validação. [A]')
    print(' -vf       Para validações rápidas.      [B]')
    print('\nComandos de atalho\n')
    print(' clear     Limpa o terminal.')
    print(' exit      Encerra o programa.')
    print(' info      Exibe a lista completa de comandos.')
    print(' sites     Abre o arquivo sites.txt')
    print(' var       Exibir variáveis do sistema, Config.json')

print(Message)

while 'exit' not in argumento.lower():

    if os.path.isfile('./Config.json'):    
        if json.ler_json(False, './Config')['localhost'] == '' and json.ler_json(False, './Config')['binary'] == '':
            print(Fore.YELLOW + 'Especifique o caminho do seu htdocs')

            htdocs = str(input('$ '))
            htdocs = htdocs if htdocs[-1] == '\\' else htdocs + '\\'
            Array['localhost'] = htdocs
            json.escreve_json(Array)
            print('\n')

            print(Fore.YELLOW + 'Especifique o caminho do seu firefox.exe')

            firefox = str(input('$ '))
            Array['binary'] = firefox
            json.escreve_json(Array)
            print('\n')

        if not os.path.isfile('./sites.txt'):
            open('./sites.txt', 'w', encoding='utf-8').close()
        
        print(Fore.YELLOW + 'Digite "info" para obter a lista de comandos nativos')
        argumento = input('$ ').lower()

        if argumento == 'info':
            Info()
            print('\n')

        elif argumento == '-v' or argumento == '-vf':
            Validador(False) if 'f' in argumento else Validador()
            print('\n')

        elif argumento == '-a':
            print('\nMódulo:' + Fore.GREEN + ' Ajustador\n')
            Ajustador()
            print('\n')

        elif argumento == 'sites':
            os.system('notepad sites.txt')
            # os.system('nano sites.txt')
            print('\n')

        # elif argumento == 'config':
        #     os.system('notepad Config.json')
        #     json.escreve_json(Array)
        #     print('\n')

        elif argumento == 'clear':
            os.system('clear')
            clear()
            print(Message)

        elif argumento == 'var':
            print('Variáveis do sistema definidas em Config.json')
            for item in Array.keys():
                if 'validation' != item:
                    print(Fore.WHITE + f' {item}:' + ' {}'.format(Array[item]))
                else:
                    print(Fore.WHITE + f' {item}' if item != 'validation' else ' Módulos de Validação')
                    for elem in Array['validation'].keys():
                        status = Fore.GREEN + 'ON' if Array['validation'][elem] else Fore.RED + 'OFF'
                        print(f'  Status: {status}' + Fore.WHITE + f' {elem}')
            print('\n')

        else:
            print(f'$ {argumento}: ' + ERRO[302] + '\n' if len(argumento) > 0 and argumento != 'exit' else '')

    else:
        json.escreve_json(Array)
