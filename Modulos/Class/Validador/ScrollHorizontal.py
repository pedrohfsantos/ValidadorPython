from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class ScrollHorizontal:
    def __init__(self, erro, erroValidador):
        self.erro = erro
        self.erroValidador = erroValidador
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.driver.set_window_size(350, 568)

    def verifica(self, pagina):
        try:
            self.driver.get(pagina)
            windowWidth = self.driver.execute_script("return document.body.clientWidth")
            documentWidth = self.driver.execute_script("return document.body.scrollWidth")
        except:
            self.erroValidador.append(pagina)

        finally:
            if windowWidth < documentWidth:
                self.erro.append(pagina)

    @property
    def fechar(self):
        self.driver.close()
        self.driver.quit()