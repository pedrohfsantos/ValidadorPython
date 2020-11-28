from PIL import Image
from ..Config import localhost

class Imagem:
    def __init__(self, erro):
        self.erro = erro

    def ajusta(self, site, imagem):
        imagem_local = self.trata_url_imagem(site, imagem)
        nova_imagem = self.calcula_nova_dimensao(imagem_local)
    
        nova_imagem.save(imagem_local, optimize=True, quality=70)

    def trata_url_imagem(self, site, url):
        i = url.find(site)
        return localhost + url[i:]

    def calcula_nova_dimensao(self, imagem):
        imagem  = Image.open(imagem)
        largura, altura = imagem.size

        if(largura > 800):
            return imagem.resize((800, round(800 * altura / largura)), Image.LANCZOS)

        elif(altura > 800):
            return imagem.resize((round(largura * 800 / altura), 800), Image.LANCZOS)

        else:
            return imagem