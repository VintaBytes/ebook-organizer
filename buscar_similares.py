import os
from difflib import SequenceMatcher
import unicodedata

# Función para normalizar los nombres de los autores (eliminar acentos y caracteres especiales)
def normalizar_nombre(nombre):
    # Elimina acentos y convierte a minúsculas
    return unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('ASCII').lower()

# Función para comparar si dos nombres son similares (con un umbral ajustable)
def nombres_similares(nombre1, nombre2, umbral=0.85):
    nombre1_normalizado = normalizar_nombre(nombre1)
    nombre2_normalizado = normalizar_nombre(nombre2)
    return SequenceMatcher(None, nombre1_normalizado, nombre2_normalizado).ratio() > umbral

# Función principal que revisa las carpetas y genera un archivo de sugerencias de fusión
def generar_sugerencias_fusion(directorio_ordenado, archivo_salida="sugerencias_fusion.txt"):
    carpetas = [carpeta for carpeta in os.listdir(directorio_ordenado) if os.path.isdir(os.path.join(directorio_ordenado, carpeta))]
    fusion_sugerencias = []

    for i in range(len(carpetas)):
        carpeta1 = os.path.join(directorio_ordenado, carpetas[i])
        nombre_carpeta1 = carpetas[i]

        for j in range(i + 1, len(carpetas)):
            carpeta2 = os.path.join(directorio_ordenado, carpetas[j])
            nombre_carpeta2 = carpetas[j]

            # Verificar si los nombres de las carpetas son similares
            if nombres_similares(nombre_carpeta1, nombre_carpeta2):
                sugerencia = f'"{nombre_carpeta1}" puede fusionarse con "{nombre_carpeta2}"'
                print(sugerencia)  # Imprimir en la consola
                fusion_sugerencias.append(sugerencia)

    # Escribir las sugerencias en un archivo de salida
    with open(archivo_salida, "w") as f:
        for sugerencia in fusion_sugerencias:
            f.write(sugerencia + "\n")

    print(f"Proceso completo. Se generó el archivo {archivo_salida} con las sugerencias de fusión.")

# Especificar la carpeta "ordenados" y ejecutar el proceso
directorio_base = os.getcwd()
directorio_ordenado = os.path.join(directorio_base, "ordenados")
generar_sugerencias_fusion(directorio_ordenado)
