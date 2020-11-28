import threading
import os.path
from ... import *
from requests_html import HTMLSession
from tqdm.auto import tqdm
from os import listdir, makedirs

arquivo = Arquivo()

class Links:
    def __init__(self, url, links404, erroLink, RastrearLinks=True):
        self.url = url
        self.links404 = links404
        self.erroLink = erroLink
        self.RastrearLinks = RastrearLinks
        self.session = HTMLSession()
        self.linksConfirmados = {'Todos':[self.url], 'Mapa Site':[], 'MPI':[]}

        makedirs('./Modulos/WebCache') if not os.path.isdir('./Modulos/WebCache') else None

    def links_site(self):
        if self.RastrearLinks:
            self.rastrear(self.url)

        r = self.session.get(self.url + 'mapa-site')
        mapaSite = r.html.find('.sitemap li a')

        if self.RastrearLinks:
            for linkMapaDoSite in mapaSite:
                self.linksConfirmados['Mapa Site'].append(linkMapaDoSite.attrs['href'])
        else:
            for linkMapaDoSite in mapaSite:
                self.linksConfirmados['Mapa Site'].append(linkMapaDoSite.attrs['href'])
                self.linksConfirmados['Todos'].append(linkMapaDoSite.attrs['href'])

        subMenuInfo = r.html.find('.sitemap ul.sub-menu-info li a')
        for linkMPI in subMenuInfo:
            self.linksConfirmados['MPI'].append(linkMPI.attrs['href'])

        self.valida_404(self.linksConfirmados['Todos'])
        arquivo.escreve_json(self.linksConfirmados, arquivo=f'./Modulos/WebCache/{self.url_base(self.url, False)}__cache.json')

        return self.linksConfirmados

    def valida_url(self, url):
        if '?' not in url and '#' not in url and '.jpg' not in url and '.jpeg' not in url and '.png' not in url and '.png' not in url and '.pdf' not in url and 'tel:' not in url and 'mailto:' not in url:
            return True
        else:
            return False

    def rastrear(self, url):
        links = [url]

        for link in tqdm(links, unit=' links', desc='Rastreando e categorizando os links', leave=False):
            try:
                r = self.session.get(link)
                pageLinks = r.html.absolute_links

            except:
                self.erroLink.append(link)
            
            else:
                for pageLink in pageLinks:
                    if self.url_base(self.url) in pageLink and self.valida_url(pageLink):
                        if pageLink not in links and link not in self.erroLink:
                            links.append(pageLink)

        self.linksConfirmados['Todos'] = links.copy()
        links.clear()

    def valida_404(self, urls):
        for url in tqdm(urls, unit=' links', desc='Verificando se há links levando para página 404', leave=False):
            try: 
                location = self.session.head(url).headers['Location']
                
            except:
                continue
            else:
                if '/404' in location:
                    self.links404.append(url)
                    self.linksConfirmados['Todos'].remove(url)

    def url_base(self, limpaUrl, mpitemporario=True):
        limpaUrl = limpaUrl.split('//')
        limpaUrl = limpaUrl[1].split('/')
        return limpaUrl[0] if mpitemporario else [x for x in limpaUrl if x][-1]