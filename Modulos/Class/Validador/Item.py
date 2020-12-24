from requests_html import HTMLSession


class Item:
    def __init__(self, url, erroValidador):
        self.url = url
        self.session = HTMLSession()
        self.r = self.session.get(self.url)
        self.erroValidador = erroValidador

    @property
    def h1(self):
        try:
            return self.r.html.find("h1")
        except:
            self.erroValidador.append(f"{self.url} - H1")

    @property
    def h2(self):
        try:
            return self.r.html.find("h2")
        except:
            self.erroValidador.append(f"{self.url} - H2")

    @property
    def h3(self):
        try:
            return self.r.html.find("h3")
        except:
            self.erroValidador.append(f"{self.url} - H3")

    @property
    def h2_mpi(self):
        try:
            return self.r.html.find("article h2")
        except:
            self.erroValidador.append(f"{self.url} - H2 MPI")

    @property
    def h3_mpi(self):
        try:
            return self.r.html.find("article h3")
        except:
            self.erroValidador.append(f"{self.url} - H3 MPI")

    @property
    def description(self):
        try:
            return self.r.html.find('head meta[name="description"]', first=True).attrs["content"]
        except:
            self.erroValidador.append(f"{self.url} - Description")

    @property
    def menu_top_texts(self):
        try:
            menuTopTexts = self.r.html.xpath("//header//nav/ul/li/a/text()")
            menuTopTexts.append("Mapa do site")
            return [item.lower() for item in menuTopTexts]
        except:
            self.erroValidador.append(f"{self.url} - Texto menu top")

    @property
    def menu_footer_texts(self):
        try:
            menuFooterTexts = self.r.html.xpath("//footer//nav/ul/li/a/text()")
            return [item.lower() for item in menuFooterTexts]
        except:
            self.erroValidador.append(f"{self.url} - Texto menu footer")

    @property
    def menu_top_links(self):
        try:
            menuTopLinks = self.r.html.xpath("//header//nav/ul/li/a/@href")
            menuTopLinks.append(menuTopLinks[0] + "mapa-site")
            return menuTopLinks
        except:
            self.erroValidador.append(f"{self.url} - Links menu top")

    @property
    def menu_footer_links(self):
        try:
            return self.r.html.xpath("//footer//nav/ul/li/a/@href")
        except:
            self.erroValidador.append(f"{self.url} - Links menu footer")

    @property
    def imagens(self):
        try:
            return self.r.html.find("body img")
        except:
            self.erroValidador.append(f"{self.url} - Imagens")

    @property
    def links(self):
        try:
            return self.r.html.xpath("//a/@href")
        except:
            self.erroValidador.append(f"{self.url} - Links")

    @property
    def aside_links(self):
        try:
            return self.r.html.xpath("//html//body//main//aside//nav//a/@href")
        except:
            self.erroValidador.append(f"{self.url} - Links aside")

    @property
    def imagens_mpi(self):
        try:
            return self.r.html.find("article ul.gallery img")
        except:
            self.erroValidador.append(f"{self.url} - Imagens MPI")

    @property
    def strongs_article(self):
        try:
            return self.r.html.find("article p strong")
        except:
            self.erroValidador.append(f"{self.url} - Strong article")

    @property
    def paragrafos_mpi(self):
        try:
            # return self.r.html.xpath('//article/p[not(@class)]')
            return self.r.html.find("article p:not(.content-call)")
        except:
            self.erroValidador.append(f"{self.url} - Paragrafos MPI")

    @property
    def texto_pagina(self):
        try:
            return self.r.html.xpath("//body//main//text()")
        except:
            self.erroValidador.append(f"{self.url} - Texto paginas")

    @property
    def titulo_strong(self):
        try:
            return self.r.html.find("h1 strong, article h2 strong, article h3 strong")
        except:
            self.erroValidador.append(f"{self.url} - Titulo Strong")
