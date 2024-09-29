import os
import shutil
import hashlib
from ebooklib import epub

# Función para calcular el hash del archivo y detectar duplicados
def calcular_hash(archivo):
    hash_sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Crear directorio si no existe
def crear_directorio_si_no_existe(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)

# Extraer los metadatos (autor, título, año) del archivo epub
def extraer_metadatos_epub(archivo):
    libro = epub.read_epub(archivo)
    titulo = None
    autor = None
    año = None

    for item in libro.get_metadata('DC', 'title'):
        titulo = item[0]
    for item in libro.get_metadata('DC', 'creator'):
        autor = item[0]
    for item in libro.get_metadata('DC', 'date'):
        año = item[0][:4]  # Extrae los primeros 4 caracteres para obtener el año

    return autor, titulo, año

# Función para convertir el autor en formato "Apellido(s), Nombre(s)"
def formato_autor(autor):
    if autor:
        partes = autor.split()
        if len(partes) > 1:
            apellido = partes[-1]
            nombres = " ".join(partes[:-1])
            return f"{apellido}, {nombres}"
    return autor

# Registrar errores en un archivo de texto
def registrar_error(ruta, archivo, error):
    with open("errores.txt", "a") as f:
        f.write(f"Error en {ruta}/{archivo}: {error}\n")

# Mover y renombrar libros (procesar solo los primeros 100)
def mover_y_renombrar_libros(directorio_aordenar, directorio_ordenado):
    hashes_archivos = set()
    libros_procesados = 0
    max_libros = 100000

    for root, dirs, files in os.walk(directorio_aordenar):
        for file in files:
            if libros_procesados >= max_libros:
                print(f"Se han procesado los primeros {max_libros} libros.")
                return  # Detiene el proceso después de 100 libros

            if file.endswith(".epub"):
                ruta_completa = os.path.join(root, file)

                try:
                    # Extraer autor, título y año desde los metadatos del archivo epub
                    autor, titulo, año = extraer_metadatos_epub(ruta_completa)

                    if not autor or not titulo:
                        raise ValueError("Metadatos faltantes (autor o título)")

                    autor_formateado = formato_autor(autor)
                    if not autor_formateado:
                        raise ValueError("No se pudo formatear el nombre del autor")

                    # Usar el formato "(1998)" para el año, o dejar en blanco si no está disponible
                    año_formateado = f"({año})" if año else ""

                    # Crear carpeta por autor dentro de la carpeta "ordenados"
                    directorio_autor = os.path.join(directorio_ordenado, autor_formateado)
                    crear_directorio_si_no_existe(directorio_autor)

                    # Renombrar el archivo según el formato "Autor - Título - (Año)"
                    nuevo_nombre = f"{autor_formateado} - {titulo} {año_formateado}.epub".replace("/", "-")  # Evitar barras en nombres
                    nueva_ruta = os.path.join(directorio_autor, nuevo_nombre)

                    # Calcular hash para evitar duplicados
                    hash_actual = calcular_hash(ruta_completa)
                    if hash_actual not in hashes_archivos:
                        shutil.move(ruta_completa, nueva_ruta)  # Mover y renombrar el archivo
                        hashes_archivos.add(hash_actual)
                        libros_procesados += 1
                    else:
                        print(f"Duplicado encontrado y eliminado: {ruta_completa}")

                except Exception as e:
                    # Registrar error en errores.txt
                    registrar_error(root, file, str(e))

# Especificar las rutas de las carpetas "aordenar" y "ordenados"
directorio_base = os.getcwd()  # Asume que el script está en la raíz de las carpetas
directorio_aordenar = os.path.join(directorio_base, "aordenar")
directorio_ordenado = os.path.join(directorio_base, "ordenados")

# Procesar los libros
mover_y_renombrar_libros(directorio_aordenar, directorio_ordenado)

