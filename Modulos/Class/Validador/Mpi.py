from unidecode import unidecode

class Mpi:
    def __init__(self, erroH2ContemH1, erroElementosVazios, erroDescriptionMpi, erroParagrafoDuplicado, erroParagrafoLista, erroPalavraChaveSemStrong, erroImagensMPI, erroValidador):
        self.erroH2ContemH1 = erroH2ContemH1
        self.erroElementosVazios = erroElementosVazios
        self.erroDescriptionMpi = erroDescriptionMpi
        self.erroParagrafoDuplicado = erroParagrafoDuplicado
        self.erroParagrafoLista = erroParagrafoLista
        self.erroPalavraChaveSemStrong = erroPalavraChaveSemStrong
        self.erroImagensMPI = erroImagensMPI
        self.erroValidador = erroValidador

    def verifica(self, pagina, description, images, h1, h2, paragrafos, imagensMPI):
        try:
            self.h2_contem_H1(pagina, h1, h2)
            self.elementos_vazios(pagina, h1, h2, paragrafos)
            self.description_mpi(pagina, description, paragrafos)
            self.paragrafo_duplicado(pagina, paragrafos)
            self.paragrafo_lista(pagina, paragrafos)
            self.palavra_chave_sem_strong(pagina, h1, paragrafos)
            self.imagens_mpi(pagina, imagensMPI)
        except:
            self.erroValidador.append(pagina)

    def h2_contem_H1(self, pagina, h1, h2):
        for uniqueH2 in h2[:-1]:
            if unidecode(h1[0].text.lower()) in unidecode(uniqueH2.text.lower()):
                return
        self.erroH2ContemH1.append(pagina)

    def elementos_vazios(self, pagina, h1, h2, paragrafos):
        elementos = h1 + h2 + paragrafos

        for elementoVazio in elementos:
            if len(elementoVazio.text) < 6:
                self.erroElementosVazios.append(pagina)
                return

    def description_mpi(self, pagina, description, paragrafos):
        for p in paragrafos:
            descriptionErro = False if unidecode(description.replace("  ", " ")[:-35].lower()) in unidecode(p.text.replace("  ", " ").lower()) else True
            if not descriptionErro: return
        self.erroDescriptionMpi.append(pagina)

    def paragrafo_duplicado(self, pagina, paragrafos):
        todosParagrafos = []
        for p in paragrafos:
            todosParagrafos.append(p.text)

        if len(todosParagrafos) != len(set(todosParagrafos)):
            self.erroParagrafoDuplicado.append(pagina)

    def paragrafo_lista(self, pagina, paragrafos):
        for p in paragrafos:
            if p.text[-1] == ';' and pagina not in self.erroParagrafoLista:
                self.erroParagrafoLista.append(pagina)

    def palavra_chave_sem_strong(self, pagina, h1, paragrafos):
        paragrafoErro = []
        for p in paragrafos:
            strong = True if p.find('strong') else False
            h1InP = True if h1[0].text.lower() in p.text.lower() else False

            if strong != h1InP:
                paragrafoErro.append(f"{paragrafos.index(p) + 1}°")

        if len(paragrafoErro) > 0:
            self.erroPalavraChaveSemStrong.append(pagina + " - " + ", ".join(paragrafoErro) + " parágrafo sem strong na palavra chave")

    def imagens_mpi(self, pagina, imagensMPI):
        if len(imagensMPI) < 1:
            self.erroImagensMPI.append(pagina)