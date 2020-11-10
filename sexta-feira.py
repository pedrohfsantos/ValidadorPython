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
    print('\nVersão atual: 1.0.1')
    print('Este terminal é exclusivo para interação com projetos em publicação.')
    print('Projeto em desenvolvimento. Estado de versão no momento: beta e atualmente alocado em pedrohfsantos/ValidadorPython no GitHub.')
    print('Digite "info" para visualizar esta aba novamente.')
    print('\nComandos de execução\n')
    print(' -v       Inicia o módulo de validação.')
    print(' -a       Inicia o módulo de ajustes.[BETA]')
    print('\nComandos de atalho\n')
    print(' sites    Abre o arquivo sites.txt')
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

        if not os.path.isfile('./sites.txt'):
            open('./sites.txt', 'w', encoding='utf-8').close()
        
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
            print('\n')

        elif argumento == 'sites':
            os.system('notepad sites.txt')
            # os.system('nano sites.txt')
            print('\n')

        elif argumento == 'clear':
            os.system('clear')
            clear()
            print(Message)

        elif argumento == 'var':
            print('Variáveis do sistema')
            for item in Array.keys():
                if 'validation' != item:
                    print(Fore.WHITE + f' {item}:' + Fore.YELLOW + ' {}'.format(Array[item]))
                else:
                    print(Fore.WHITE + f' {item}' + ' {')
                    for elem in Array['validation'].keys():
                        print(Fore.WHITE + f'  {elem}:', Fore.YELLOW + '{}'.format(Array['validation'][elem]))
                    print(Fore.WHITE + ' }')
            print('\n')

        else:
            print(f'$ {argumento}: ' + ERRO[302] + '\n' if len(argumento) > 0 and argumento != 'exit' else '')

    else:
        json.escreve_json(Array)