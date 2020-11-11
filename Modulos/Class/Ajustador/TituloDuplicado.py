from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
import re

class TituloDuplicado:

	def __init__(self, erro):
	    self.erro = erro

	def ajusta(self, html, url, r):

		content = []
		dic     = []

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
			title = re.search(r'\$h1\s*=\s*[\"\'](.*?)[\"\'\;]', html).group(1)
			tipoMPI = 'div' if soup.find_all('div', class_="mpi-content") else 'article'

			Element = [self.percorre(soup, tipoMPI, 'h2'), self.percorre(soup, tipoMPI, 'h3')]

			if Element[0]:

				for elem in soup.find_all('h2'):

					for i, item in enumerate(elem):
						if i > 0:
							if unidecode(str(Element[0]).strip().lower()) == unidecode(item.string.lower().strip()):
								item.string = 'SAIBA MAIS SOBRE ' + item.string.upper().strip()

			for elem in soup.prettify(formatter=None):
				content.append(elem)
			value = ''.join(map(str, content))

			return mask(value, False)

		except:
			return False

	def arquivo(self, url):
	    url = url.split('//')[1].split('/')[-1].split(' ')[0]
	    return url

	def percorre(self, soup, mpi, elementString):
		elem = {'h2': [], 'h3': []} 
		content = []
		for item in soup.select(mpi):

			element = item.find_all(elementString)

			for Element in element:
				elem[elementString].append(Element.string)
			break

		return self.duplicado(elem[elementString])

			
	def duplicado(self, array):

		texto = array
		contagem = dict()

		for linha in texto:

		    palavra = linha.strip()

		    if palavra not in contagem.keys():
		        contagem[palavra] = 1
		    else:
		        contagem[palavra] += 1

		for Max in contagem.keys():
			if contagem[Max] > 1:
				return Max