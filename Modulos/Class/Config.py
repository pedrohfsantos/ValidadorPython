import os
from ..Arquivo import *

json = Arquivo()

ERRO_LINK = "Links levando para 404"
ERRO_W3C = "W3C"
ERRO_DESCRIPTION_1 = "Description com números de caracteres incorretos"
ERRO_DESCRIPTION_2 = "O H1 não foi encontrado na description"
ERRO_COLUNA_LATERAL = "Links duplicados na coluna lateral"
ERRO_MAPA_SITE = "Links não encontrados do Mapa no site"
ERRO_IMAGENS_1 = "Imagens quebradas"
ERRO_IMAGENS_2 = "Imagens acima de 200KB"
ERRO_IMAGENS_3 = "Imagens com erro ALT/TITLE"
ERRO_MENU = "Menu"
ERRO_PAGESPEED = "PageSpeed"
ERRO_SCROLL = "Scroll Horizontal"
ERRO_TITLE_1 = "Página sem H1"
ERRO_TITLE_2 = "Página com mais de 1 H1"
ERRO_TITLE_3 = "Titulo duplicado"
ERRO_TITLE_4 = "Titulo (H2/H3) igual H1"
ERRO_TITLE_5 = "Titulo (H1/H2/H3) com strong"
ERRO_MPI_1 = "H2 sem palavra chave"
ERRO_MPI_2 = "Elementos vazios na pagina"
ERRO_MPI_3 = "Description atual não foi encontrada no texto MPI"
ERRO_MPI_4 = "MPI paragrafos duplicado"
ERRO_MPI_5 = "Alterar P para UL>LI"
ERRO_MPI_6 = "Palavra chave sem strong"
ERRO_MPI_7 = "MPI sem imagens"
ERRO_TEXTO = "Pagina com lorem ipsum"

ERRO_VALIDACAO_LINK = "Não foi possível rastrear o link"
ERRO_VALIDACAO_ITEM = "Item não encontrado"
ERRO_VALIDACAO_W3C = "Não foi possível validar W3C"
ERRO_VALIDACAO_COLUNA_LATERAL = "Não foi possível validar Coluna lateral"
ERRO_VALIDACAO_MAPA_SITE = "Não foi possível validar Mapa do site"
ERRO_VALIDACAO_MENU = "Não foi possível validar Menu"
ERRO_VALIDACAO_PAGESPEED = "Não foi possível validar PageSpeed"
ERRO_VALIDACAO_SCROLL = "Não foi possível validar ScrollHorizontal"
ERRO_VALIDACAO_TEXTO = "Não foi possível validar Texto"
ERRO_VALIDACAO_DESCRIPTION = "Não foi possível validar Description"
ERRO_VALIDACAO_IMAGENS = "Não foi possível validar Imagens"
ERRO_VALIDACAO_TITLE = "Não foi possível validar Title"
ERRO_VALIDACAO_MPI = "Não foi possível validar MPI"

erro_validacao = {
    ERRO_VALIDACAO_LINK: [],
    ERRO_VALIDACAO_ITEM: [],
    ERRO_VALIDACAO_W3C: [],
    ERRO_VALIDACAO_COLUNA_LATERAL: [],
    ERRO_VALIDACAO_MAPA_SITE: [],
    ERRO_VALIDACAO_MENU: [],
    ERRO_VALIDACAO_PAGESPEED: [],
    ERRO_VALIDACAO_SCROLL: [],
    ERRO_VALIDACAO_TEXTO: [],
    ERRO_VALIDACAO_DESCRIPTION: [],
    ERRO_VALIDACAO_IMAGENS: [],
    ERRO_VALIDACAO_TITLE: [],
    ERRO_VALIDACAO_MPI: [],
}
erros_encontrado = {
    ERRO_LINK: [],
    ERRO_W3C: [],
    ERRO_DESCRIPTION_1: [],
    ERRO_DESCRIPTION_2: [],
    ERRO_COLUNA_LATERAL: [],
    ERRO_MAPA_SITE: [],
    ERRO_IMAGENS_1: [],
    ERRO_IMAGENS_2: [],
    ERRO_IMAGENS_3: [],
    ERRO_MENU: [],
    ERRO_PAGESPEED: [],
    ERRO_SCROLL: [],
    ERRO_TITLE_1: [],
    ERRO_TITLE_2: [],
    ERRO_TITLE_3: [],
    ERRO_TITLE_4: [],
    ERRO_TITLE_5: [],
    ERRO_MPI_1: [],
    ERRO_MPI_2: [],
    ERRO_MPI_3: [],
    ERRO_MPI_4: [],
    ERRO_MPI_5: [],
    ERRO_MPI_6: [],
    ERRO_MPI_7: [],
    ERRO_TEXTO: [],
}

ERRO = {
    300: "\nNão foi possível iniciar o módulo selecionado",
    302: "Comando inválido.\n",
    303: "Não foi possível iniciar a função.",
    404: "\nNão foi possível localizar o destino especificado.",
    414: "Por favor, verifique a alocação do projeto no servidor temporário.",
    416: "Falha de projeto 404 no servidor temporário.",
    500: "\nO arquivo está corrompido.",
    501: "\nAviso: O sistema não pôde executar as funções.",
    503: "\nNão foi possível selecionar o projeto informado.",
    504: "\nAviso: Não foi possível ajustar os arquivos abaixo:",
    505: 'Não foi possível identificar a classe "sub-menu-info" no mapa do site',
}

if os.path.isfile("./Config.json"):
    configJson = json.ler_json(False, "./Config")
    urlmpitemporario = configJson["url"]
    localhost = configJson["localhost"]
    validation = {
        "w3c": configJson["validation"]["w3c"],
        "coluna_lateral": configJson["validation"]["coluna_lateral"],
        "mapa_do_site": configJson["validation"]["mapa_do_site"],
        "menu": configJson["validation"]["menu"],
        "page_speed": configJson["validation"]["page_speed"],
        "texto": configJson["validation"]["texto"],
        "description": configJson["validation"]["description"],
        "imagem": configJson["validation"]["imagem"],
        "title": configJson["validation"]["title"],
        "mpi": configJson["validation"]["mpi"],
        "scroll_horizontal": configJson["validation"]["scroll_horizontal"],
    }

else:
    urlmpitemporario = "http://mpitemporario.com.br/projetos/"
    localhost = ""
    validation = {
        "w3c": True,
        "coluna_lateral": True,
        "mapa_do_site": True,
        "menu": True,
        "page_speed": True,
        "texto": True,
        "description": True,
        "imagem": True,
        "title": True,
        "mpi": True,
        "scroll_horizontal": True,
    }


Array = {
    "url": urlmpitemporario,
    "localhost": localhost,
    "validation": validation,
}
