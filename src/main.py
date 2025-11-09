import requests
import pandas as pd
from pathlib import Path
# Shufflan
# Scraper de celulares en Fallabela.

celulares = 0
totalCelulares = 0
productos = []
# Recorremos las 70 páginas que existen dentro de la web.
for p in range(1, 70):
    url = f"https://www.falabella.com/s/browse/v1/listing/cl?page={p}&categoryId=cat2018&categoryName=Celulares-y-Telefonos&pgid=96&pid=15c37b0b-a392-41a9-8b3b-978376c700d5&zones=PCL184%2CPCL3651%2CPCL3887%2CINT_MLA%2CPCL4984%2CFALABELLA_FBY_BT_SDD%2CPCL2829%2CINT_360LION%2CPCL4980%2CPCL3505%2CREVERSE_RM_REDPROPIA%2CPCL2998%2CPCL4992%2CIKEA_RM_HD_24%2CPCL3031%2CPCL3577%2CHUB_SALIDA_DIRECTA_RM%2CPCL2120%2CPCL3687%2C13_MAIPU%2CPCL2830%2CPCL3099%2CPCL3661%2CINT_DHL%2CPCL4981%2CBX_R13_BASE%2CPCL226%2CSTARKEN_R13%2CPCL3041%2CFBY_RM_M%2CPCL2380%2CFEDEX_RM_URB%2CPCL2520%2CPCL5090%2CPCL3128%2CPCL2511%2CLOSC%2CPCL540%2CPCL1386%2CPCL5005%2CPCL3136%2CPCL109%2C2020%2CPCL1186%2CPCL3414%2C3045%2CPCL1486%2CPCL3882%2CINT_SUNYOU%2CPCL4982%2CPCL2890%2C130617%2CPCL25%2CCHILEXPRESS_8%2CPCL1839%2CPCL5126%2CFALABELLA_FBY_SDD%2CPCL2269%2CINT_CHILEXPRESS%2CPCL4983%2CZL_CERRILLOS%2CPCL1135%2CRM%2CPCL108%2CPCL94%2CFBY_BT_SALIDA_DIRECTA%2CPCL2288%2CCHILE_INTERNATIONAL%2CPCL1364%2C13%2CPCL861%2CPCL2792&latLong=%257B%2522latitude%2522%253A%2522-33.5%2522%252C%2522longitude%2522%253A%2522-70.71666666666667%2522%257D"
    resp = requests.get(url)
    # Si la web se encuentra disponible, ejecutamos el código.
    if resp.status_code == 200:
        # Creamos un JSON con los datos de la página.
        data = resp.json()
        # Comenzamos a iterar sobre los resultados que obtenemos, buscando lo que necesitamos, en este caso: "Nombre", "Marca", "Precio" y "Url" del producto.
        for item in data["data"]["results"]:
            marca = item.get("brand", "Sin marca")
            nombre = item.get("displayName", "Sin nombre")
            
            # Utilizamos un filtro para no ingresar al Excel, lo que no necesitamos.
            nombreMinus = nombre.lower()            
            palabras_excluir = ["bateria", "puerto", "chip", "camara", "cargador", "pack", "pantalla", "kit", "tripode", "batería"]

            valido = True
            for palabra in palabras_excluir:
                if palabra in nombreMinus:
                    valido = False
                    break

            precios = item.get("prices", [])
            urlP = item.get("url", "Sin url")
            
            if precios and valido:
                precios = precios[0].get("price")[0]
                
                # Si todo va bien, terminamos por crear un diccionario, para luego trabajarlo con Pandas y crear el Excel.
                productos.append({
                    "Marca" : marca,
                    "Nombre" : nombre,
                    "Precio" : precios,
                    "Url" : urlP
                })
            celulares += 1
            totalCelulares += 1
        # Mostramos por consola la página que estamos recorriendo y limpiamos el contador.
        print("======================================")
        print(f"Página {p} Recorrida correctamente!")
        print(f"Total de celulares: {celulares}")
        print("======================================\n")
        celulares = 0
    else:
        print("Error al acceder:", resp.status_code)
        

# Creamos la ruta para poder guardar el Excel dentro de la carpeta data. Así mantenemos un orden.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
excel_path = DATA_DIR / "productos_falabella.xlsx"

# Por último ordenamos todos los celulares, para que por defecto en el Excel esten ordenados de la A-Z por nombre de Marca. 
# y creamos un data frame para poder crear el Excel y exportarlo.
productos_ordenados = sorted(productos, key=lambda x: x["Marca"].lower())
df = pd.DataFrame(productos_ordenados)
df.to_excel(excel_path, index=False)
print("\n========================================================")
print("El Excel con los celulares ha sido creado correctamente.")
print(f"Hemos encontrado un total de: {totalCelulares}")
print("========================================================")
