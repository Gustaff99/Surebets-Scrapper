import math
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pygame
import concurrent.futures

# Inicializar pygame
pygame.init()

bucle = True
sonido = pygame.mixer.Sound(r"c:\Users\Gus\Desktop\Surebets-scrapper\Sirena.mp3")

# Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Función para modificar el nombre de los jugadores en la URL1
def modificar_nombre_jugador_url1(nombre):
    nombres = nombre.split(" ")
    if len(nombres) > 1:
        return nombres[-1]
    else:
        return nombre
    
# Funcion para limpiar /
def replace_pattern(text):
    pattern = r" / . "  # Patrón de dos espacios seguidos de cualquier carácter
    replacement = "/"  # Reemplazo por un solo espacio
    return re.sub(pattern, replacement, text)

# Función para modificar el nombre de los jugadores en la URL2
def modificar_nombre_jugador_url2(nombre):
    nombres = replace_pattern(nombre.replace(" •", "")).split(" ")
    if len(nombres) > 1:
        return " ".join(nombres[1:])
    else:
        return nombre

def modificar_nombre_jugador_url3(nombre):
    nombres = nombre.split(",")
    if len(nombres) > 1:
        nombres = nombre.split(" ")
        return nombres[0]
    else:
        return nombre


#Calcular si el numero tiene decimales
def tiene_decimales(numero):
    return isinstance(numero, float) or isinstance(numero, complex)


#Funcion para comparar los resultados
def calcular_surebets(resultados_url1, resultados_url2, cantidad_inicial=102):
    print("Comparación de resultados:")
    valorcondecimales = True
    for jugador, odds_url1 in resultados_url1.items():
        if jugador in resultados_url2:
            odds_url2 = resultados_url2[jugador]
            # Encontrar el valor más grande para odds1
            max_odds1 = max(float(odds_url1[0]), float(odds_url2[0]))
            # Encontrar el valor más grande para odds2
            max_odds2 = max(float(odds_url1[1]), float(odds_url2[1]))
            cantidad_apuesta_1 = (cantidad_inicial * max_odds2) / (max_odds1 + max_odds2)
            cantidad_apuesta_2 = cantidad_inicial - cantidad_apuesta_1
            cantidad_ganancia = (((cantidad_apuesta_2 * max_odds2) / 100) * cantidad_inicial) - cantidad_inicial
            
            if tiene_decimales(cantidad_apuesta_1) or tiene_decimales(cantidad_apuesta_2):
                if abs(math.floor(cantidad_apuesta_1) - cantidad_apuesta_1) < abs((math.floor(cantidad_apuesta_1) + 1) - cantidad_apuesta_1):
                    cantidad_apuesta_1 = math.floor(cantidad_apuesta_1)
                    cantidad_apuesta_2 = math.floor(cantidad_apuesta_2) + 1
                    cantidad_inicial = cantidad_apuesta_1 + cantidad_apuesta_2
                    cantidad_ganancia = (((cantidad_apuesta_2 * max_odds2) / 100) * cantidad_inicial) - cantidad_inicial
                else:
                    cantidad_apuesta_1 = math.floor(cantidad_apuesta_1) + 1
                    cantidad_apuesta_2 = math.floor(cantidad_apuesta_2)
                    cantidad_inicial = cantidad_apuesta_1 + cantidad_apuesta_2
                    cantidad_ganancia = (((cantidad_apuesta_2 * max_odds2) / 100) * cantidad_inicial) - cantidad_inicial

            if cantidad_ganancia > 1:
                print(f"Jugador: {jugador}")
                print("Valores de URL1:", odds_url1)
                print("Valores de URL2:", odds_url2)
                print("Máximo valor para odds1:", max_odds1)
                print("Máximo valor para odds2:", max_odds2)
                print()
                print("Apostando " + str(cantidad_inicial) + " se terminaría con una ganancia de " + str(cantidad_ganancia))
                print("Hay que apostar " + str(cantidad_apuesta_1) + " al primer participante y " + str(cantidad_apuesta_2) + " al segundo participante.")
                bucle = False
                        
                # Reproducir el sonido
                sonido.play()
                # Esperar a que el sonido termine de reproducirse
                pygame.time.wait(int(sonido.get_length() * 500))
                # Detener todos los canales de sonido y finalizar pygame
                pygame.mixer.stop()
                pygame.quit()
    print("Fin de la comparación")

def procesar_url1(url):
    # Crear una instancia del driver de Selenium
    driver = webdriver.Chrome(options=options)
    # Navegar a la página
    driver.get(url)
    # Desplazarse hasta el final de la página
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Esperar a que la página se cargue completamente
    wait = WebDriverWait(driver, 20)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    # Esperar a que los elementos estén presentes en la página
    jugadores_odds = {}
    jugadores_elementos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btmarket__link-name--ellipsis")))
    odd_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "betbutton__odds")))
    # Asociar cada equipo con sus dos siguientes valores de odds
    for i in range(len(jugadores_elementos) - 1):
        jugador_element = jugadores_elementos[i]
        jugador = jugador_element.text
        if " v " in jugador:
            jugador_1, jugador_2 = jugador.split(" v ")
        else:
            jugador_1, jugador_2 = "", ""
        # Modificar el nombre del jugador 1
        jugador_1 = modificar_nombre_jugador_url1(jugador_1)
        # Abreviar el nombre del jugador 2
        jugador_2 = modificar_nombre_jugador_url1(jugador_2)
        odd1 = odd_elements[i * 2].text
        odd2 = odd_elements[i * 2 + 1].text if i * 2 + 1 < len(odd_elements) else ""
        jugadores_odds[(jugador_1, jugador_2)] = [odd1, odd2]
    # Cerrar el driver de Selenium
    driver.quit()
    return jugadores_odds

def procesar_url2(url):
    # Crear una instancia del driver de Selenium
    driver = webdriver.Chrome(options=options)
    # Navegar a la página
    driver.get(url)
    # Desplazarse hasta el final de la página
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Esperar a que la página se cargue completamente
    wait = WebDriverWait(driver, 20)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    # Esperar a que los elementos estén presentes en la página
    jugadores_odds = {}
    jugadores_elementos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "team-name")))
    odd_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-runner-price")))
    # Asociar cada equipo con sus dos siguientes valores de odds
    numeroiteraciones = (len(jugadores_elementos) - 1) // 2
    for i in range(0, numeroiteraciones, 2):
        jugador_element1 = jugadores_elementos[i]
        jugador_element2 = jugadores_elementos[i + 1]
        jugador1 = modificar_nombre_jugador_url2(jugador_element1.text.replace(" •", ""))
        jugador2 = modificar_nombre_jugador_url2(jugador_element2.text.replace(" •", ""))
        odd1 = odd_elements[i].text
        odd2 = odd_elements[i + 1].text if i + 1 < len(odd_elements) else ""
        if odd1 != " " and odd2 != " ":
            jugadores_odds[(jugador1, jugador2)] = [odd1, odd2]
    # Cerrar el driver de Selenium
    driver.quit()
    return jugadores_odds

def procesar_url3(url):
    # Crear una instancia del driver de Selenium
    driver = webdriver.Chrome(options=options)
    # Navegar a la página
    driver.get(url)
    # Desplazarse hasta el final de la página
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Esperar a que la página se cargue completamente
    wait = WebDriverWait(driver, 20)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    #Carga los resultados de la pagina
    # Navegar a la página
    driver.get(url)
    # Esperar a que los elementos estén presentes en la página
    jugadores_odds = {}
    jugadores_elementos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".asb-flex-col.asb-pos-wide")))
    odd_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".asb-flex-cc.asb-unshrink._asb_price-block-content-price")))
    # Asociar cada equipo con sus dos siguientes valores de odds
    numeroiteraciones = (len(jugadores_elementos) - 1) // 2
    salto = False
    for i in range(0, numeroiteraciones, 2):
        if not salto:
            salto = True
            continue
        jugador_element1 = jugadores_elementos[i]
        jugador_element2 = jugadores_elementos[i + 1]
        jugador1 = modificar_nombre_jugador_url3(jugador_element1.text)
        jugador2 = modificar_nombre_jugador_url3(jugador_element2.text)
        # Verificar si hay suficientes elementos en odd_elements
        if i < len(odd_elements):
            odd1 = odd_elements[i - 2].text
        else:
            odd1 = ""
        if i + 1 < len(odd_elements):
            odd2 = odd_elements[i - 1].text
        else:
            odd2 = ""
        if odd1 != "" and odd2 != "":
            jugadores_odds[(jugador1, jugador2)] = [odd1, odd2]
        # Realizar el salto en la siguiente iteración
        salto = False


    # Cerrar el driver de Selenium
    driver.quit()

    return jugadores_odds

def imprimir_resultados(jugadores_odds, url):
    print(f'Equipos y sus dos siguientes valores de odds ({url}):')
    for jugador, odds in jugadores_odds.items():
        print(jugador, odds)
                

# URL del sitio web a analizar
url1 = 'https://sports.williamhill.es/betting/es-es/tenis'
url2 = 'https://www.betfair.es/sport/tennis'
url3 = 'https://www.jokerbet.es/apuestas-deportivas.html#/alltopevents/events/68'



while bucle:
    
    # Crear un ThreadPoolExecutor con un máximo de 3 hilos
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Ejecutar las funciones de procesamiento de URL en paralelo
        futuros = [executor.submit(procesar_url1, url1), executor.submit(procesar_url2, url2), executor.submit(procesar_url3, url3)]
    
     # Obtener los resultados de los procesos de escaneo
    try:
        resultados_url1 = futuros[0].result()
        resultados_url2 = futuros[1].result()
        resultados_url3 = futuros[2].result()
        
        # Imprimir los resultados y realizar el cálculo de surebets
        imprimir_resultados(resultados_url1, url1)
        imprimir_resultados(resultados_url2, url2)
        imprimir_resultados(resultados_url3, url3)
        
        calcular_surebets(resultados_url1, resultados_url2, 100)
        calcular_surebets(resultados_url1, resultados_url3, 100)
        calcular_surebets(resultados_url2, resultados_url3, 100)

    except Exception as e:
        print("Fallo al obtener los resultados de las URL.")
    