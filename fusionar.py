import os
import shutil

# Función para fusionar dos carpetas
def fusionar_carpetas(carpeta1, carpeta2):
    # Mover archivos de carpeta2 a carpeta1
    for archivo in os.listdir(carpeta2):
        archivo_origen = os.path.join(carpeta2, archivo)
        archivo_destino = os.path.join(carpeta1, archivo)
        
        # Si el archivo ya existe en carpeta1, renombrar para evitar colisión
        if os.path.exists(archivo_destino):
            nombre, extension = os.path.splitext(archivo)
            archivo_destino = os.path.join(carpeta1, f"{nombre}_duplicado{extension}")
        
        shutil.move(archivo_origen, archivo_destino)
    
    # Eliminar carpeta2 después de mover todos sus archivos
    os.rmdir(carpeta2)
    print(f"Carpeta '{carpeta2}' fusionada con '{carpeta1}' y eliminada.")

# Función principal que procesa el archivo de fusión
def procesar_fusion(archivo_fusion, directorio_ordenado):
    with open(archivo_fusion, "r") as f:
        lineas = f.readlines()
    
    for linea in lineas:
        if "puede fusionarse con" in linea:
            # Extraer las dos carpetas desde la línea del archivo
            partes = linea.replace('"', '').strip().split(' puede fusionarse con ')
            carpeta1 = os.path.join(directorio_ordenado, partes[0])
            carpeta2 = os.path.join(directorio_ordenado, partes[1])

            # Verificar que ambas carpetas existan
            if os.path.exists(carpeta1) and os.path.exists(carpeta2):
                fusionar_carpetas(carpeta1, carpeta2)
            else:
                print(f"Una de las carpetas no existe: {carpeta1} o {carpeta2}")

# Especificar la carpeta "ordenados" y el archivo de fusión
directorio_base = os.getcwd()
directorio_ordenado = os.path.join(directorio_base, "ordenados")
archivo_fusion = os.path.join(directorio_base, "sugerencias_fusion.txt")

# Ejecutar el proceso de fusión
procesar_fusion(archivo_fusion, directorio_ordenado)
