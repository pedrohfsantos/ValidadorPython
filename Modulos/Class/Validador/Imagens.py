from requests_html import HTMLSession

class Imagens:
    def __init__(self, erroImgQuebrada, erroTamanho, erroTitleAlt, erroValidador):
        self.session = HTMLSession()
        self.erroImgQuebrada = erroImgQuebrada
        self.erroTamanho = erroTamanho
        self.erroTitleAlt = erroTitleAlt
        self.erroValidador = erroValidador

    def verifica(self, pagina, imagens):
        try:
            for imagem in imagens:
                if imagem.attrs['src'][0:4].lower() != 'http':
                    i = imagem.attrs['src'].find('http')
                    imagem.attrs['src'] = imagem.attrs['src'][i:]

                if str(self.session.head(imagem.attrs['src']).status_code) != '200':
                    self.erroImgQuebrada.append(f"{pagina}: {imagem.attrs['src']}")
                else:
                    self.tamanho_imagem(imagem)
                
                self.alt_title(imagem, pagina)

            repetida = self.duplicado(self.erroTamanho)
            if repetida: del self.erroTamanho[repetida]
        except:
            self.erroValidador.append(pagina)

    def tamanho_imagem(self, imagem):
        if "&imagem=" not in imagem.attrs['src']:
            tamanho = int(self.session.head(imagem.attrs['src']).headers['Content-Length']) / 1024
            if round(tamanho) > 200:
                self.erroTamanho.append(f"{imagem.attrs['src']}")
 
    def alt_title(self, imagem, pagina):
        try:
            if 'escrev' in imagem.attrs['alt'].lower():
                self.erroTitleAlt.append(f"{pagina} - src='{imagem.attrs['src']}' ALT com 'ESCREVA AQUI'")

            elif 'exemplo de mpi' in imagem.attrs['alt'].lower():
                self.erroTitleAlt.append(f"{pagina} - src='{imagem.attrs['src']}' ALT com 'Exemplo de MPI'")
        except:
            self.erroTitleAlt.append(f"{pagina} - src='{imagem.attrs['src']}' Imagem sem ALT")

        try:
            if 'escrev' in imagem.attrs['title'].lower():
                self.erroTitleAlt.append(f"{pagina} - src='{imagem.attrs['src']}' com TITLE 'ESCREVA AQUI'")

            elif 'exemplo de mpi' in imagem.attrs['title'].lower():
                self.erroTitleAlt.append(f"{pagina} - src='{imagem.attrs['src']}' com TITLE 'Exemplo de MPI'")
        except:
            self.erroTitleAlt.append(f"{pagina} - src='{imagem.attrs['src']}' - Imagem sem TITLE")

    def duplicado(self, lista):
        contagem = dict()
        for indice in lista:
            item = indice.strip()
            if item not in contagem.keys():
                contagem[item] = 1
            else:
                contagem[item] += 1

        for maxRepeticao in contagem.keys():
            if contagem[maxRepeticao] > 1:
                return maxRepeticao