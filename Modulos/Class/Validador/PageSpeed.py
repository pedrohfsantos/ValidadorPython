import random
import threading
import json
import re
from requests_html import HTMLSession
from Modulos.Class.Config import localhost, urlmpitemporario 
from tqdm.auto import tqdm



class PageSpeed:
    def __init__(self, erro, erroValidador):
        self.apiKey = 'AIzaSyDFsGExCkww5IFLzG1aAnfSovxSN-IeHE0'
        self.session = HTMLSession()
        self.erro = erro
        self.erroValidador = erroValidador

    def pagespeed(self, pagespeedUrl, apiKey):
        try:
            mobileUrl = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={self.ajuste_link_pageSpeed(pagespeedUrl)}&category=performance&locale=pt_BR&strategy=mobile&key={apiKey}'
            desktopUrl = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={self.ajuste_link_pageSpeed(pagespeedUrl)}&category=performance&locale=pt_BR&strategy=desktop&key={apiKey}'
            mobileRequest = self.session.get(mobileUrl)
            jsonDataM = json.loads(mobileRequest.text)
            desktopRequest = self.session.get(desktopUrl)
            jsonDataD = json.loads(desktopRequest.text)
            
        except:
            self.erroValidador.append(pagespeedUrl)

        finally:
            mobileScore = int(float(jsonDataM['lighthouseResult']['categories']['performance']['score']) * 100)
            if mobileScore < 90:
                self.erro.append(f'{pagespeedUrl} - Mobile: {mobileScore}')

            desktopScore = int(float(jsonDataD['lighthouseResult']['categories']['performance']['score']) * 100)
            if desktopScore < 90:
                self.erro.append(f'{pagespeedUrl} - Desktop: {desktopScore}')

    def verifica(self, links):
        for pagespeedUrl in tqdm(links, unit=' links', desc='Validando PageSpeed', leave=False):
            threading.Thread(
                target=self.pagespeed,
                args=(
                    pagespeedUrl,
                    self.apiKey
                    )).start()

    def ajuste_link_pageSpeed(self, link):
        link = self.url_urlmpitemporario(link)
        link = link.replace(':', '%3A')
        link = link.replace('/', '%2F')
        return link


    def url_urlmpitemporario(self, url):
        if 'localhost/' in url:
            htdocs = re.search(r'^.*?htdocs\/(.*)', localhost)
            htdocs = '' if not htdocs.group(1) else htdocs.group(1)
            url = re.sub(r'https?:\/\/.*?\/' + htdocs, urlmpitemporario, url)
            return url
        else:
            return url