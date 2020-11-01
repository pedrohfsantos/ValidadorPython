from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
from ..Construct import *
import re

mascara = Mascara()  

class TituloDuplicado:

	def __init__(self, erro):
	    self.erro = erro

	def ajusta(self, html, url, r):
		content = []
		try:

			soup = BeautifulSoup(mascara.Aplicar(html), "html.parser")
			title = r.html.find('h1')[0].text

			tipoMPI = '.mpi-content, .tabs-content' if len(soup.find_all('div', class_="mpi-content")) > 0 else 'article'

			for item in soup.select(tipoMPI):
				
				if item.find_all('h2'):
					element_H2 = item.find_all('h2')
					for e in element_H2:
						if unidecode(e.string.lower().strip()) == unidecode(title):
							e.string = 'CONHEÇA MAIS SOBRE ' + e.string.strip()
				elif item.find_all('h3'):
					element_H3 = item.find_all('h3')
					for e in element_H3:
						if unidecode(e.string.lower().strip()) == unidecode(title):
							e.string = 'CONHEÇA MAIS SOBRE ' + e.string.strip()
				else:
					self.erro.append(f"=> {url}")
			
			for elem in soup.prettify(formatter=None):
				content.append(elem)
			value = ''.join(map(str, content))

			return mascara.Retirar(html)
			mascara.reset()

		except:
			mascara.reset()

	def arquivo(self, url):
	    url = url.split('//')[1].split('/')[-1].split(' ')[0]
	    return url