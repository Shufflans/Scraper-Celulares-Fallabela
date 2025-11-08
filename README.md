# Scraper-Celulares-Fallabela.
Scraper sencillo para extraer información de todos los celulares de la página web Fallabela, obteniendo información a tiempo real.

Este proyecto obtiene información en tiempo real desde el endpoint JSON directamente de la página Falabella Chile, extrayendo datos de celulares (marca, nombre, precio y URL) y exportándolos a Excel.

# Características.
Como caraceterísticas de este proyecto tenemos:
- Extraer datos directamente desdes la API de Fallabela, sin la necesidad de utilizar Selenium, ni BeautifulSoup.
- Exportar a un Excel para poder analizarlo o poder hacer precios comparativos.
- Filtro de productos no deseados, en este caso, filtrar todo lo que no sea u celular.

# Librerías utlizadas.
- Pandas.
- Requests.
