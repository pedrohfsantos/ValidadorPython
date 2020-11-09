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
		# try:

		soup = BeautifulSoup(mascara.Mask(html, True), "html.parser")
		title = re.search(r'\$h1\s*=\s*[\"\'](.*?)[\"\'\;]', html).group(1)
		tipoMPI = 'div' if soup.find_all('div', class_="mpi-content") else 'article'

		Element = [self.percorre(soup, tipoMPI, 'h2'), self.percorre(soup, tipoMPI, 'h3')]

		if Element[0]:

			for elem in soup.find_all('h2'):

				for i in elem:
					if unidecode(str(Element[0]).strip().lower()) == unidecode(i.string.lower().strip()):
						i.string = 'SAIBA MAIS SOBRE ' + i.string.upper().strip()

		for elem in soup.prettify(formatter=None):
			content.append(elem)
		value = ''.join(map(str, content))

		print(mascara.Mask(value, False))

		return mascara.Mask(value, False)

		# except:
		# 	return False

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