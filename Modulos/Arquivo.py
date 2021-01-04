import os, os.path, json, re, shutil, winreg, shlex, sys, webbrowser
from .Class.Config import *
from os import listdir, makedirs
from datetime import datetime
from pathlib import Path
from tqdm.auto import tqdm


class Arquivo:
    def __init__(self):
        if not os.path.isdir("./Projetos"):
            makedirs("./Projetos/")

        pastas = ["Projetos/JSON", "Projetos/Validação", "Projetos/Backup", "Modulos/WebCache/"]

        for pasta in pastas:
            if not os.path.isdir(f"{pasta}"):
                makedirs(f"{pasta}")

        if not os.path.isfile("./sites.txt"):
            open("./sites.txt", "w", encoding="utf-8").close()

    def ler_urls_sitesTXT(self):
        with open("sites.txt", "r") as sites:
            linha = sites.readlines()
            arrayUrl = [url.strip("\n").strip(" ") for url in linha]
            return arrayUrl

    def url_projeto_mpitemporario(self, limpa_url):
        limpa_url = limpa_url.split("//")
        limpa_url = limpa_url[1].split("/")
        limpa_url = [x for x in limpa_url if x]
        return limpa_url[-1]

    def arquivo_validacao(self, erros_encontrado, erro_validacao, site):
        log = [1 for erro in erro_validacao.values() if len(erro) > 0]

        with open(
            f"Projetos/Validação/{self.url_projeto_mpitemporario(site)}.txt",
            "w",
            encoding="utf-8",
        ) as arquivo:

            for titulo_erro, valores_erro in erros_encontrado.items():
                if len(valores_erro) > 0:
                    arquivo.write(f"{titulo_erro}: \n")

                    for valor_erro in valores_erro:
                        arquivo.write(f"=> {valor_erro} \n")

                    arquivo.write("\n")

                valores_erro.clear()

            if log:
                arquivo.write(f" =--=-=-= LOG DE ERRO DO VALIDADOR | PROJETO {site} =--=-=-= \n")
                for titulo_erro_validacao, valores_erro_validacao in erro_validacao.items():
                    if len(valores_erro_validacao) > 0:
                        arquivo.write(f"{titulo_erro_validacao}: \n")

                        for valor_erro_validacao in valores_erro_validacao:
                            arquivo.write(f"=> {valor_erro_validacao}\n")

                        arquivo.write("\n")

                    valor_erro_validacao.clear()

    def arquivo_validacao_json(self, erros_encontrado, site):
        with open(
            f"Projetos/JSON/{self.url_projeto_mpitemporario(site)}.json",
            "w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(erros_encontrado, arquivo, indent=4)

    def escreve_json(self, config, arquivo="./Config.json", method="w"):
        with open(arquivo, method, encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def ler_json(self, site=False, caminho="Projetos/JSON/", validacao_json=True, ler=False):
        path = caminho + site if site else caminho if validacao_json else caminho
        with open(f"{path if not ler else caminho}.json", "r", encoding="utf-8") as arquivoJson:
            dados = arquivoJson.read()
            return json.loads(dados)

    def lista_arquivos_json(self, pasta="Projetos/JSON/", ext="json"):
        listaArquivos = listdir(pasta)
        for keys, arquivo in enumerate(listaArquivos):
            if ext not in arquivo:
                del listaArquivos[keys]
        return listaArquivos

    def ler_arquivo(self, caminho):
        content = []
        try:
            with open(caminho + ".php", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for elem in lines:
                    content.append(elem)
                return "".join(map(str, content))
        except IOError:
            return False

    def criar_arquivo(self, body, projeto, funcao, arquivo, htdocs, backup=False, subs=False):

        DIR = {
            "backup": projeto + "/" + funcao + "/" + arquivo + ".php",
            "caminho": htdocs + projeto + "/" + arquivo + ".php",
        }
        Path(f"./Projetos/Backup/{projeto}/{funcao}/").mkdir(parents=True, exist_ok=True)
        body = (
            body.replace(f"<!-- {subs} -->", f"<?={subs}?>").re.sub(r"<\?=\s*\$caminho2\s*\?>", "", body)
            if subs
            else body
        )
        try:
            with open(DIR["caminho"], "w", encoding="utf-8") as f:
                f.write(body)
                f.write("</html>")
        except:
            return False

    def backup(self, site, erros):
        urlsBackup = []
        try:
            now = datetime.now()
            pasta = [
                f"./Projetos/Backup/{site}",
                f'./Projetos/Backup/{site}/{now.strftime("%d-%m-%Y-%H-%M-%S")}',
            ]
            for criar in pasta:
                if not os.path.isdir(criar):
                    makedirs(criar)

            listaUrlJson = self.ler_json(False, f"./Projetos/JSON/{site}")
            for item in listaUrlJson:
                if item in erros:
                    for url in listaUrlJson[item]:
                        urlsBackup.append(url)

            for arquivo in tqdm(
                set(urlsBackup), unit=" arquivos", desc=" Realizando backup dos arquivos necessários", leave=False
            ):
                arquivo = re.search(r"http.*?\S*[^: ]", arquivo).group(0)
                arquivo = "index" if arquivo.split("/")[-1] == "" else arquivo.split("/")[-1]

                configJson = self.ler_json(False, "./Config")
                arquivoOriginal = f"{configJson['localhost']}{site}/{arquivo}.php"
                shutil.copy(arquivoOriginal, pasta[1])
            return True
        except:
            return False

    def limpa_url(self, projeto, url):
        url = re.search(r"http.*?\S*[^: ]", url).group(0)
        url = "index" if url.split("/")[-1] == "" else url.split("/")[-1]
        return "../ {}/{}".format(projeto, url)

    def cache(self, valor=None, arquivo=None, remove=False):
        self.escreve_json(valor, arquivo=arquivo) if not remove else os.remove(remove)

    def caminho_chrome(self):
        result = None
        if winreg:
            for subkey in ["ChromeHTML\\shell\\open\\command", "Applications\\chrome.exe\\shell\\open\\command"]:
                try:
                    result = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, subkey)
                except WindowsError:
                    pass
                if result is not None:
                    result_split = shlex.split(result, False, True)
                    result = result_split[0] if result_split else None
                    if os.path.isfile(result):
                        break
                    result = None
        else:
            expected = "google-chrome" + (".exe" if os.name == "nt" else "")
            for parent in os.environ.get("PATH", "").split(os.pathsep):
                path = os.path.join(parent, expected)
                if os.path.isfile(path):
                    result = path
                    break
        return result

    def listar(self, array):
        content = []
        for key, value in enumerate(array):
            if len(array) > 0:
                content.append(f"[{key + 1}] {value}")
        return "\n".join(map(str, content))

    def Open(self, argumento, lista, localhost=False):

        path_chrome = sys.argv[0].split("sexta-feira.py")[0]
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(self.caminho_chrome()))
        try:
            if len(lista) > 0:
                print(self.listar(lista))
                opcao = int(input("\nNúmero do projeto: "))
                site = lista[opcao - 1]
                if opcao in range(0, len(lista) + 1):
                    if localhost:
                        URL = (
                            self.ler_json(False, "./Config")["url"] + "/"
                            if self.ler_json(False, "./Config")["url"][-1] != "/"
                            else self.ler_json(False, "./Config")["url"]
                        )
                        destino = URL + site.split(".txt")[0]
                        webbrowser.get("chrome").open(f"{destino}")
                    return (
                        webbrowser.get("chrome").open(f"{path_chrome}/Projetos/Validação/{site}")
                        if " chrome" in argumento
                        else os.system(f"notepad Projetos/Validação/{site}")
                    )
                else:
                    print("Aviso: Projeto não encontrado.")
            else:
                print("Erro: Você não possui projetos validados.")
        except:
            print("\nAviso: Não foi possível selecionar o projeto.")

        return False

    def historico_validacao(self, url):
        try:
            Caminho = "Modulos/WebCache/__hist"
            Links = self.ler_json(caminho=Caminho, ler=True) if os.path.isfile(Caminho + ".json") else [url]
            if url not in Links:
                Links.append(url) if os.path.isfile(Caminho + ".json") else None
            self.escreve_json(Links, arquivo=Caminho if Caminho[-5] == '.json' else Caminho + ".json")
        
        except:
            print("\nAviso: O histórico de validação não foi salvo.")

        finally:
            print("\nAviso: histórico de validação salvo.")