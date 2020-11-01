from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
from ..Construct import *
import re

mascara = Mascara()  

class SequenciaH2:

	def __init__(self, erro):
		self.erro = erro

	def ajusta(self, html, url):
		content = []
		try:
			soup = BeautifulSoup(mascara.Aplicar(html), "html.parser")

			tipoMPI = '.mpi-content, .tabs-content' if len(soup.find_all('div', class_="mpi-content")) > 0 else 'article'

			for p in soup.select(tipoMPI):

				element = p.select('h2 + h2')

				if element:
					for h2 in element:
						h2.name = 'p'
						h2.string = h2.string.capitalize()
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