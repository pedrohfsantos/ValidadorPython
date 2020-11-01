from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
from ..Construct import *
import re

mascara = Mascara()  

class Breadcrumb:

	def __init__(self, erro):
	    self.erro = erro

	def ajusta(self, html, url):		
		content = []

		try:
			soup = BeautifulSoup(mascara.Aplicar(html), "html.parser")

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

			return mascara.Retirar(value)
			mascara.reset()

		except:
			mascara.reset()

	def arquivo(self, url):
	    url = url.split('//')[1].split('/')[-1].split(' ')[0]
	    return url