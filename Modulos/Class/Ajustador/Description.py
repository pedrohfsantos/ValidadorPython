from bs4 import BeautifulSoup
from unidecode import unidecode
from ..Config import localhost
import re


class Description:
    def __init__(self, erro):
        self.erro = erro

	def ajusta(self, title, html, a):
		content = []

		try:

			method = '.mpi-content > p, .tabs-content > p' if method else 'article > p'
			
			m 	= re.search(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", html)
			sub = re.sub(r'<.*>', '', m.group(0)).strip()
			space = m.group(0)
			
			html = re.sub(r'\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]', sub, html)
			html = html.replace(' , ', ', ') if space.find(' , ') >= 0 else html
			html = html.replace(' . ', ' ') if space.find(' . ') >= 0 else html

			
			soup = BeautifulSoup(mask(html, True), "html.parser")
			title = title.strip()
			
			currentDesc = session.get(self.url_replace(localhost, a)).html.find('head meta[name="description"]', first=True).attrs['content']
			
			descfix = True if unidecode(title.lower()) not in unidecode(currentDesc.lower()) or re.search(r'<.*>', m.group()) or m.group().find('  ') or not unidecode(m.group(0).lower()).find(unidecode(title.lower())) else False

			if descfix:			
				article = session.get(self.url_replace(localhost, a)).html.find(f'{method}')			
				for p in article:

					
					a = p.text.lower().find(unidecode(title).lower())
					b = unidecode(p.text).lower().find(title.lower())
					
					if b >= 0:
						if len(p.text[b:]) >= 125:
							desc = unidecode(p.text[b:]).strip()
							break
					elif a >= 0:
						if len(p.text[a:]) >= 125:
							desc = p.text[a:].strip()
							break

				if desc:
					if desc[-1] == '.' and len(desc) >= 140 and len(desc) <= 160 :
					    desc = desc.lower()
					else:
						while len(desc) > 145:
						    desc = desc.split(" ")
						    del desc[-1]
						    desc = " ".join(desc)

						desc.lower()
						desc += '... saiba mais.'.encode("latin1").decode("unicode_escape")

					desc = f'$desc				= "{desc.capitalize()}";'
					

				else:
					self.erro.append(f"=> {url}")

			else:
				self.erro.append(f"=> {url} - Description atual está correta")
			
			
			for elem in soup.prettify(formatter=None):
				content.append(elem)
			value = ''.join(map(str, content))

			value = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", desc, str(soup)) if desc else value

			return mascara(value, False)

		except:
			return False

	def url_replace(self, url, file):
		rewrite = 'http://mpitemporario.com.br/projetos/' + projeto + '/' if not file else 'http://mpitemporario.com.br/projetos/' + projeto + '/' + file
		return rewrite