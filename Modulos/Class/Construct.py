from bs4 import BeautifulSoup
import re

class Mascara:

	def __init__(self):
		pass

	def Mask(self, body, metodo):

		elements = []
		msk = '!!!PHP!!!'

		def remove(elem):
			elements.append(elem.group())
			return msk

		def add(elem):
			return elements.pop(0)
			del elements[:]

		def Aplicar(body):
			m = re.sub(r"<\?.*\?>", remove, body)
			soup = BeautifulSoup(m, "html.parser")
			mask = re.sub(msk, remove, str(soup.prettify(formatter=None)))
			return mask

		def Retirar(body):
			m = re.sub(r"<\?.*?\?>", remove, body)
			soup = BeautifulSoup(m, "html.parser")
			mask = re.sub(msk, add, str(soup.prettify(formatter=None)))
			return mask

		if metodo:
			Aplicar(body)
		else:
			Retirar(body)
			del elements[:]