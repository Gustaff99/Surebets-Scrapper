import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Crear una instancia del driver de Selenium
driver = webdriver.Chrome(options=options)

# URL del sitio web a analizar
url = 'https://online-elderecho-com.ubu-es.idm.oclc.org/seleccionProducto.do;jsessionid=35BF361977337886614D2834329B9FAC.TC_ONLINE04?producto=DOCTR&javascriptInicial=presentarMarginalMemento(%27*%27,%27ES%27,%272012/901157%27)#%2FpresentarMemento.do%3Fnref%3D2012%2F901157%26producto%3DDOCTR%26marginal%3D%26rnd%3D0.4520664566970889'

# Navegar a la página
driver.get(url)

# Esperar a que la página se cargue completamente
time.sleep(10)  # Esperar 10 segundos adicionales

wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))

# Ejecutar JavaScript para obtener todos los elementos del DOM
script = """
var elements = document.getElementsByTagName("*");
var classNames = new Set();
for (var i = 0; i < elements.length; i++) {
    var classList = elements[i].classList;
    for (var j = 0; j < classList.length; j++) {
        classNames.add(classList[j]);
    }
}
return Array.from(classNames);
"""
class_names = driver.execute_script(script)

# Imprimir los nombres de clase encontrados
print("Nombres de clase encontrados en la página:")
for class_name in class_names:
    print(class_name)

# Cerrar el driver de Selenium
driver.quit()
