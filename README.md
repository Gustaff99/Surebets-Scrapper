
# Surebets-Scrapper 🇬🇧

## Overview

`Surebets-Scrapper` is a web scraping tool designed to identify surebets opportunities across various betting websites and notify the user with a sound alert. Despite the challenges in exploiting these opportunities due to rapidly changing odds, this project is intriguing and potentially useful to some users.

The project is entirely implemented in Python, using Selenium for web scraping.

## Key Features

- Scans multiple betting websites for odds.
- Automatically identifies surebets opportunities.
- Real-time audible alerts when a surebet is detected.
- Concurrent processing for efficient and quick scanning.

## Prerequisites

- Python 3.x
- Selenium
- Pygame
- concurrent.futures

## Installation

Before running the script, you need to install the required Python libraries. You can install these libraries using pip:

```bash
pip install selenium pygame
```

## How it works

The script uses Selenium to navigate through several betting websites, scrapes betting odds, and tries to identify arbitrage opportunities (surebets). When a surebet is found, the program alerts the user by playing a sound.

Here's a brief overview of the main functions:

- **Selenium Setup**: The script configures Selenium to run Chrome in headless mode.
- **Data Scraping**: It scrapes betting odds from different websites.
- **Data Processing**: The script includes functions to clean and process the scraped data, focusing on the players' names and the odds.
- **Arbitrage Calculation**: It calculates potential surebets based on the processed data.
- **Notification**: Upon identifying a surebet, the script plays a sound to notify the user.

## Usage

To execute the script, run:

```python
python surebets.py
```

Make sure to navigate to the script's directory before running the command or provide the full path to the script.

## Caution

This script is created for educational purposes only. Engaging in betting may involve financial risk. Users are responsible for any legal implications or losses incurred.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Warning

This project is for educational and entertainment purposes only. Gambling can be addictive and harmful. Gamble responsibly.


# Surebets-Scrapper 🇪🇸

## Descripción General

`Surebets-Scrapper` es una herramienta de rastreo web diseñada para identificar oportunidades de surebets (apuestas seguras) en diversos sitios web de apuestas, alertando al usuario mediante una señal sonora. A pesar de los desafíos que implica aprovechar estas oportunidades debido a la rápida fluctuación de las cuotas, este proyecto resulta fascinante y potencialmente útil para ciertos usuarios.

Este proyecto está completamente desarrollado en Python, utilizando Selenium para el rastreo web.

## Características Principales

- Rastreo de cuotas en múltiples sitios web de apuestas.
- Identificación automática de oportunidades de surebets.
- Alertas audibles en tiempo real cuando se detecta una surebet.
- Procesamiento concurrente para una exploración eficiente y rápida.

## Prerrequisitos

- Python 3.x
- Selenium
- Pygame
- Concurrent.futures

## Instalación

Antes de ejecutar el script, es necesario instalar las bibliotecas de Python requeridas. Puedes instalar estas bibliotecas utilizando pip:

```bash
pip install selenium pygame
```

## Cómo Funciona

El script utiliza Selenium para navegar a través de varios sitios web de apuestas, extrae las cuotas de apuestas y busca identificar oportunidades de arbitraje (surebets). Cuando se encuentra una surebet, el programa alerta al usuario reproduciendo un sonido.

Aquí tienes un resumen de las funciones principales:

- **Configuración de Selenium**: El script configura Selenium para ejecutar Chrome en modo sin cabeza (headless).
- **Extracción de Datos**: Raspa las cuotas de apuestas de diferentes sitios web.
- **Procesamiento de Datos**: El script incluye funciones para limpiar y procesar los datos extraídos, centrándose en los nombres de los jugadores y las cuotas.
- **Cálculo de Arbitraje**: Calcula las surebets potenciales basándose en los datos procesados.
- **Notificación**: Al identificar una surebet, el script reproduce un sonido para notificar al usuario.

## Uso

Para ejecutar el script, utiliza:

```python
python surebets.py
```

Asegúrate de navegar al directorio del script antes de ejecutar el comando o proporciona la ruta completa al script.

## Precaución

Este script se ha creado únicamente con fines educativos. Participar en apuestas puede conllevar un riesgo financiero. Los usuarios son responsables de cualquier implicación legal o pérdida incurrida.

## Contribuciones

Las solicitudes de extracción (pull requests) son bienvenidas. Para cambios importantes, por favor, abre primero un 'issue' para discutir lo que te gustaría modificar.

## Advertencia

Este proyecto es solo para fines educativos y de entretenimiento. El juego puede ser adictivo y conllevar riesgos financieros. Juega de manera responsable.
