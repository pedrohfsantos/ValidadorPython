from requests_html import HTMLSession


class Links:
    def __init__(self, url, links404, erroLink, Recursion=True):
        self.url = url
        self.links404 = links404
        self.erroLink = erroLink
        self.Recursion = Recursion
        self.session = HTMLSession()
        self.links = []
        self.linksConfirmados = {'Todos':[self.url], 'Mapa Site':[], 'MPI':[]}
        self.linksDaPagina = self.session.get(self.url).html.absolute_links
        # self.linksDaPagina = self.session.get(self.url).html.xpath('//a[not(@rel="nofollow")]/@href') # Pega os links que não tenha o nofollow


    def links_site(self):
        if self.Recursion:
            self.recursividade(self.linksDaPagina)

        r = self.session.get(self.url + 'mapa-site')
        mapaSite = r.html.find('.sitemap li a')

        if self.Recursion:
            for linkMapaDoSite in mapaSite:
                self.linksConfirmados['Mapa Site'].append(linkMapaDoSite.attrs['href'])

        else:
            for linkMapaDoSite in mapaSite:
                self.linksConfirmados['Mapa Site'].append(linkMapaDoSite.attrs['href'])
                self.linksConfirmados['Todos'].append(linkMapaDoSite.attrs['href'])

        subMenuInfo = r.html.find('.sitemap ul.sub-menu-info li a')
        for linkMPI in subMenuInfo:
            self.linksConfirmados['MPI'].append(linkMPI.attrs['href'])
    
        return self.linksConfirmados


    def ValidaUrl(self, url):
        if '?' not in url and '#' not in url and '.jpg' not in url and '.jpeg' not in url and '.png' not in url and '.png' not in url and '.pdf' not in url and 'tel:' not in url and 'mailto:' not in url:
            return True
        else:
            return False


    def url_base(self, limpaUrl):
        limpaUrl = limpaUrl.split('//')
        limpaUrl = limpaUrl[1].split('/')
        return limpaUrl[0]

    def recursividade(self, LinksPagina):
        for link in LinksPagina:
            if self.url_base(self.url) in link and self.ValidaUrl(link):
                self.links.append(link)


        for link in self.links:
            if link not in self.linksConfirmados['Todos'] and link not in self.links404 and link not in self.erroLink:
                if self.valida_404(link):
                    try:
                        r = self.session.get(link)
                        pageLinks = r.html.absolute_links
                        # pageLinks = r.html.xpath('//a[not(@rel="nofollow")]/@href') # Pega os links que não tenha o nofollow
                    
                    except:
                        self.erroLink.append(link)
                    
                    else:
                        self.linksConfirmados['Todos'].append(link)
                        self.recursividade(pageLinks)


    def valida_404(self, url):
        try: 
            location = self.session.head(url).headers['Location']
            
        except:
            return True

        else:
            if '/404' in location:
                self.links404.append(url)
                return False
