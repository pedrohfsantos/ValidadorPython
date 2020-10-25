from Modulos.Validador import Validador
from Modulos.Ajustador import Ajustador
import os


print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n')

print('Para melhor experiência utilize o validador no GIT BASH')
print('Digite "info" para mais informações do validador\n')

print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n')

while True:
    argumento = input('Sexta-Feita: ').lower()

    if argumento == 'info':
        print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n')
        
        print(' -v      = Inicia o módulo de validação.\n')
        print(' sites   = Abre o arquivo sites.txt (Nesse arquivo é informado as URLs dos projetos que serão validados).\n')
        print(' info    = Exibe informações do validador.\n')
        print(' clear   = Limpa o terminal.\n')
        print(' exit    = Sai do programa.\n')

        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n')

    elif argumento == '-v':
        Validador()

    elif argumento == '-a':
        Ajustador()

    elif argumento == 'sites':
        os.system('nano sites.txt')

    elif argumento == 'clear':
        os.system('clear')

    elif argumento == 'exit':
        break

    else:
        continue