from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from ..Config import binary

class ScrollHorizontal:
    def __init__(self, erro, erroValidador):
        self.erro = erro
        self.erroValidador = erroValidador
        options = Options()
        options.add_argument('--headless')
        options.binary = binary
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = False
        self.driver = webdriver.Firefox(options=options, capabilities=cap, executable_path="WebDriver/geckodriver.exe")
        self.driver.set_window_size(350, 568)

    def verifica(self, pagina):
        try:
            self.driver.get(pagina)
            windowWidth = self.driver.execute_script('return document.body.clientWidth')
            documentWidth = self.driver.execute_script('return document.body.scrollWidth')
        except:
            self.erroValidador.append(pagina)

        finally:
            if windowWidth < documentWidth:
                self.erro.append(pagina)

    def fechar(self):
        self.driver.close()
        self.driver.quit()