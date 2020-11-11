from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
import re

class Breadcrumb:

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

			for wrapper in soup.select('div.wrapper'):

				soup.find('h1').extract()

				tag = soup.new_tag('div')
				tag.string = '<!-- $caminhoBread2 -->'

				wrapper.insert_before(tag)

			for e in elements:
				if '$h1' in e:
					del elements[elements.index(e)]
			
			for elem in soup.prettify(formatter=None):
				content.append(elem)
			value = ''.join(map(str, content))

			return mask(value, False)

		except:
			return False

	def arquivo(self, url):
	    url = url.split('//')[1].split('/')[-1].split(' ')[0]
	    return url