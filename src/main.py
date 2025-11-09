# Shufflan
# Scraper de celulares en Fallabela.
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# --- Rutas ---
directorioBase = Path(__file__).resolve().parent.parent
directorioData = directorioBase / "data"
directorioOutput = directorioData / "outputs"
directorioData.mkdir(exist_ok=True)
directorioOutput.mkdir(exist_ok=True)

# --- Variables de control. ---
celulares = 0
totalCelulares = 0
productos = []

# --- Parámetros útiles --- 
fecha_str = datetime.now().strftime("%Y-%m-%d")
horaExacta = datetime.now().strftime("%Y-%m-%d_%H%M%S")
palabras_excluir = ["bateria", "puerto", "chip", "camara", "cargador", "pack", "pantalla", "kit", "tripode", "batería"]
fuente = "Fallabela"
categoria = "Celulares"

# --- Función para normalizar el precio (sin punto) ---
def quitarPunto(precio):
    try:
        if isinstance(precio, (int, float)):
            return precio
        texto = str(precio)
        texto = texto.replace(".","").replace(",","")
        return int(float(texto))
    except:
        return None

# --- Código Principal, Recorrido de las páginas ---
for p in range(1, 70):
    url = f"https://www.falabella.com/s/browse/v1/listing/cl?page={p}&categoryId=cat2018&categoryName=Celulares-y-Telefonos&pgid=96&pid=15c37b0b-a392-41a9-8b3b-978376c700d5&zones=PCL184%2CPCL3651%2CPCL3887%2CINT_MLA%2CPCL4984%2CFALABELLA_FBY_BT_SDD%2CPCL2829%2CINT_360LION%2CPCL4980%2CPCL3505%2CREVERSE_RM_REDPROPIA%2CPCL2998%2CPCL4992%2CIKEA_RM_HD_24%2CPCL3031%2CPCL3577%2CHUB_SALIDA_DIRECTA_RM%2CPCL2120%2CPCL3687%2C13_MAIPU%2CPCL2830%2CPCL3099%2CPCL3661%2CINT_DHL%2CPCL4981%2CBX_R13_BASE%2CPCL226%2CSTARKEN_R13%2CPCL3041%2CFBY_RM_M%2CPCL2380%2CFEDEX_RM_URB%2CPCL2520%2CPCL5090%2CPCL3128%2CPCL2511%2CLOSC%2CPCL540%2CPCL1386%2CPCL5005%2CPCL3136%2CPCL109%2C2020%2CPCL1186%2CPCL3414%2C3045%2CPCL1486%2CPCL3882%2CINT_SUNYOU%2CPCL4982%2CPCL2890%2C130617%2CPCL25%2CCHILEXPRESS_8%2CPCL1839%2CPCL5126%2CFALABELLA_FBY_SDD%2CPCL2269%2CINT_CHILEXPRESS%2CPCL4983%2CZL_CERRILLOS%2CPCL1135%2CRM%2CPCL108%2CPCL94%2CFBY_BT_SALIDA_DIRECTA%2CPCL2288%2CCHILE_INTERNATIONAL%2CPCL1364%2C13%2CPCL861%2CPCL2792&latLong=%257B%2522latitude%2522%253A%2522-33.5%2522%252C%2522longitude%2522%253A%2522-70.71666666666667%2522%257D"
    try:
        respuesta = requests.get(url, timeout=10)
        
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] Página {p} tardó demasiado, se omite.")
        time.sleep(1)
        continue

    if respuesta.status_code == 200:

        data = respuesta.json()
        # --- Extracción de los datos ---
        for item in data["data"]["results"]:
            marca = item.get("brand", "Sin marca")
            nombre = item.get("displayName", "Sin nombre")            
            nombreMinus = nombre.lower()

            # --- Filtrado de Datos ---
            if any(palabra in nombreMinus for palabra in palabras_excluir):
                continue

            precios = item.get("prices", [])
            urlP = item.get("url", "Sin url")
            
            precioValidar = None
            if precios:
                try:
                    precios = precios[0].get("price")
                    if isinstance(precios, (list)) and precios:
                        precioValidar = precios[0]
                    else:
                        precioValidar = None
                except:
                    precioValidar = None
                
            precioSinPunto = quitarPunto(precioValidar)
            
            # --- Validar si el precio es válido ---
            if precioSinPunto is not None:              
                productos.append({
                    "Marca" : marca,
                    "Nombre" : nombre,
                    "Precio" : precioSinPunto,
                    "Url" : urlP,
                    "Fecha" : fecha_str,
                    "Fuente" : fuente,
                    "Categoria" : categoria
                })
                celulares += 1
                totalCelulares += 1
                
        # --- Mostrar por Consola página y cantidad de productos ---
        print(f"Hemos vista la página {p} --> Cantidad de celulares encontrados: {celulares}")
        celulares = 0
        time.sleep(0.2)
    else:
        print("Error al acceder:", resp.status_code)

# --- Orden y creación de Excel ---
productos_ordenados = sorted(productos, key=lambda x: x["Marca"].lower())
df = pd.DataFrame(productos_ordenados)
nombreExcel = f"Celulares_Fallabela_{horaExacta}.xlsx"
rutaExcel = directorioOutput / nombreExcel
df.to_excel(rutaExcel, index=False)

# --- Resultado final ---
print(f"\n ========== Resultados ========== ")
print(f"Excel guardado en: {rutaExcel}")
print(f"Total de productos encontrados válidos: {len(productos)}")
print(f" ================================ ")
