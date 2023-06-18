import math
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pygame

# Inicializar pygame
pygame.init()

bucle = True;
sonido = pygame.mixer.Sound("C:/Users/Gus/Desktop/Surebets/Sirena.mp3")

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
        return nombres[0]
    else:
        return nombre

#Funcion para comparar los resultados
def calcular_surebets(resultados_url1, resultados_url2, cantidad_inicial=100):
    print("Comparación de resultados:")
    valorcondecimales = True
    for jugador, odds_url1 in resultados_url1.items():
        if jugador in resultados_url2:
            while valorcondecimales:
                odds_url2 = resultados_url2[jugador]
                # Encontrar el valor más grande para odds1
                max_odds1 = max(float(odds_url1[0]), float(odds_url2[0]))
                # Encontrar el valor más grande para odds2
                max_odds2 = max(float(odds_url1[1]), float(odds_url2[1]))
                cantidad_apuesta_1 = (cantidad_inicial * max_odds2) / (max_odds1 + max_odds2)
                cantidad_apuesta_2 = cantidad_inicial - cantidad_apuesta_1
                cantidad_ganancia = (((cantidad_apuesta_2 * max_odds2) / 100) * cantidad_inicial) - cantidad_inicial
                if cantidad_apuesta_1.is_integer(): valorcondecimales = False
                else: cantidad_inicial = cantidad_inicial - 1
            if cantidad_ganancia > 0:
                print(f"Jugador: {jugador}")
                print("Valores de URL1:", odds_url1)
                print("Valores de URL2:", odds_url2)
                print("Máximo valor para odds1:", max_odds1)
                print("Máximo valor para odds2:", max_odds2)
                print()
                print("Apostando " + str(cantidad_inicial) + " se terminaría con una ganancia de " + str(cantidad_ganancia))
                print("Hay que apostar " + str(cantidad_apuesta_1) + " al primer participante y " + str(cantidad_apuesta_2) + " al segundo participante.")
                bucle = False
                if cantidad_apuesta_2.isinteger():
                    bucle = False
                else: 
                    nueva_cantidad_apuesta_1 = math.floor(cantidad_apuesta_1)
                    nueva_cantidad_apuesta_2 = (math.floor(cantidad_apuesta_1) / cantidad_apuesta_1) * cantidad_apuesta_2
                    if cantidad_apuesta_2.isinteger():
                        bucle = False
                    else: cantidad_inicial = cantidad_inicial - 1
                        
                # Reproducir el sonido
                sonido.play()
                # Esperar a que el sonido termine de reproducirse
                pygame.time.wait(int(sonido.get_length() * 100))
                # Detener todos los canales de sonido y finalizar pygame
                pygame.mixer.stop()
                pygame.quit()
    print("Fin de la comparación")

def procesar_url1(url):
    # Configuración de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Crear una instancia del driver de Selenium
    driver = webdriver.Chrome(options=options)
    # Navegar a la página
    driver.get(url)
    # Desplazarse hasta el final de la página
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1.25)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Esperar a que la página se cargue completamente
    wait = WebDriverWait(driver, 20)
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
    # Configuración de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Crear una instancia del driver de Selenium
    driver = webdriver.Chrome(options=options)
    # Navegar a la página
    driver.get(url)
    # Desplazarse hasta el final de la página
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1.25)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Esperar a que la página se cargue completamente
    wait = WebDriverWait(driver, 20)
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
    # Configuración de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Crear una instancia del driver de Selenium
    driver = webdriver.Chrome(options=options)
    # Navegar a la página
    driver.get(url)
    # Desplazarse hasta el final de la página
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1.25)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Esperar a que la página se cargue completamente
    wait = WebDriverWait(driver, 20)
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
url1 = 'https://sports.williamhill.es/betting/es-es/tenis/partidos'
url2 = 'https://www.betfair.es/sport/tennis'
url3 = 'https://www.jokerbet.es/apuestas-deportivas.html#/alltopevents/events/68'


while bucle:
    try:
        # Procesar URL1
        resultados_url1 = procesar_url1(url1)
        imprimir_resultados(resultados_url1, url1)
    except Exception as e:
        print("Fallo al obtener datos de williamhill, no se detectan apuestas en este momento")

    try:
        # Procesar URL2
        resultados_url2 = procesar_url2(url2)
        imprimir_resultados(resultados_url2, url2)
    except Exception as e:
        print("Fallo al obtener datos de betfair, no se detectan apuestas en este momento")
        
    try:
        # Procesar URL3
        resultados_url3 = procesar_url3(url3)
        imprimir_resultados(resultados_url3, url3)
    except Exception as e:
        print("Fallo al obtener datos de jockerbets, no se detectan apuestas en este momento")


    try:
        # Procesar surebets
        print(url1)
        print("y")
        print(url2)
        calcular_surebets(resultados_url1,resultados_url2,100)
        print(url1)
        print("y")
        print(url3)
        calcular_surebets(resultados_url1,resultados_url3,100)
        print(url2)
        print("y")
        print(url3)
        calcular_surebets(resultados_url2,resultados_url3,100)

    except Exception as e:
        print("Fallo al calcular surebets.")
    