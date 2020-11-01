from bs4 import BeautifulSoup
import re

msk = '!!!PHP!!!'
elements = []

class Mascara:

	def __init__(self):
		pass

	def Retirar(self, body):
		m = re.sub(r"<\?.*\?>", self.remove, body)
		soup = BeautifulSoup(m, "html.parser")
		mask = re.sub(msk, self.add, str(soup.prettify(formatter=None)))
		return mask

		del elements[:]

	def Aplicar(self, body):
		m = re.sub(r"<\?.*\?>", self.remove, body)
		soup = BeautifulSoup(m, "html.parser")
		mask = re.sub(msk, self.remove, str(soup.prettify(formatter=None)))
		return mask

	def remove(self, elem):
		elements.append(elem.group())
		return msk

	def add(self, elem):
		return elements.pop(0)