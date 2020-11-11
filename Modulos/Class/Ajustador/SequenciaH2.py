from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
import re

class SequenciaH2:

	def __init__(self, erro):
		self.erro = erro

	def ajusta(self, html, url):

		content = []
		dic		= []

		def mask(html, chave):

		    msk = '!!!PHP!!!'

		    def remove(e):
		        dic.append(e.group())
		        return msk

		    def add(e):
		        return dic.pop(0)

		    try:
		        body = re.sub(r"<\?.*\?>", remove, html)
		        soup = BeautifulSoup(body, "html.parser")
		        mask = re.sub(msk, remove, str(soup.prettify(formatter=None))) if chave else re.sub(msk, add, str(soup.prettify(formatter=None)))
		    except:
		        mask = False

		    return mask

		try:
			soup = BeautifulSoup(mask(html, True), "html.parser")

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

			return mask(value, False)

		except:
			return False

	def arquivo(self, url):
	    url = url.split('//')[1].split('/')[-1].split(' ')[0]
	    return url