import os
import hashlib
from difflib import SequenceMatcher

# Función para calcular el hash de un archivo
def calcular_hash(archivo):
    hash_sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Función para comparar si dos nombres son similares
def nombres_similares(nombre1, nombre2, umbral=0.7):
    return SequenceMatcher(None, nombre1.lower(), nombre2.lower()).ratio() > umbral

# Función para comparar si dos carpetas tienen los mismos libros
def comparar_contenido_carpeta(carpeta1, carpeta2):
    archivos1 = {archivo: calcular_hash(os.path.join(carpeta1, archivo)) for archivo in os.listdir(carpeta1) if archivo.endswith(".epub")}
    archivos2 = {archivo: calcular_hash(os.path.join(carpeta2, archivo)) for archivo in os.listdir(carpeta2) if archivo.endswith(".epub")}
    
    # Si ambos conjuntos de archivos son iguales (mismos nombres y hashes), consideramos que las carpetas son duplicadas
    return archivos1 == archivos2

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
                # Si los nombres son similares, comparar los archivos dentro de las carpetas
                if comparar_contenido_carpeta(carpeta1, carpeta2):
                    fusion_sugerencias.append(f'"{nombre_carpeta1}" puede fusionarse con "{nombre_carpeta2}"')

    # Escribir las sugerencias en un archivo de salida
    with open(archivo_salida, "w") as f:
        for sugerencia in fusion_sugerencias:
            f.write(sugerencia + "\n")

    print(f"Proceso completo. Se generó el archivo {archivo_salida} con las sugerencias de fusión.")

# Especificar la carpeta "ordenados" y ejecutar el proceso
directorio_base = os.getcwd()
directorio_ordenado = os.path.join(directorio_base, "ordenados")
generar_sugerencias_fusion(directorio_ordenado)
