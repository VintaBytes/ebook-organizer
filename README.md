# Organizador de colecciones de libros en formato ePub.
Este proyecto es ideal para aquellos que deseen automatizar la organización de grandes colecciones de libros electrónicos, basándose en metadatos precisos y evitando duplicados.

<span><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/></span>

### Descripción del proyecto

Este proyecto consiste en un **script Python** diseñado para organizar y gestionar archivos de libros electrónicos en formato **EPUB**. El objetivo principal del script es mover, renombrar y organizar los libros en función de los metadatos presentes en cada archivo, como el nombre del autor, el título de la obra y el año de publicación. A continuación, se detalla lo que realiza el script:

#### 1. **Qué hace el script:**
   - **Recorre carpetas** en busca de archivos **EPUB**.
   - **Extrae los metadatos** del archivo EPUB, como el **autor**, el **título** y el **año de publicación**.
   - **Organiza los libros** en subcarpetas por autor, utilizando el formato **"Apellido(s), Nombre(s)"**.
   - **Renombra los archivos** utilizando el formato **"Autor - Título - (Año)"**.
   - **Elimina duplicados** comparando los archivos mediante un **hash**.
   - Si encuentra un problema (como la falta de metadatos), **registra el error** en un archivo de texto llamado **errores.txt**.
   - **Procesa un número limitado de libros** en una sola ejecución, basado en un máximo definido.

#### 2. **Cómo maneja las carpetas:**
   - El script está ubicado en una carpeta raíz que contiene dos subcarpetas:
     - **"aordenar"**: Es donde se almacenan los libros pendientes de procesar. Puede tener todos los niveles de subcarpetas que sea necesario.
     - **"ordenados"**: Es la carpeta donde se moverán los libros después de ser organizados.
   - A medida que procesa cada libro, crea una **subcarpeta** dentro de "ordenados" con el nombre del autor.
   - El archivo es renombrado y movido a la subcarpeta correspondiente. Si el autor tiene varios libros, todos se agrupan en la misma carpeta.

#### 3. **Librerías utilizadas:**
   - **os**: Para interactuar con el sistema de archivos, como listar directorios y mover archivos.
   - **shutil**: Para mover archivos entre carpetas y realizar otras operaciones de gestión de archivos.
   - **hashlib**: Para generar hashes de los archivos y detectar duplicados.
   - **ebooklib**: Para leer los archivos EPUB y extraer los metadatos (autor, título, y año de publicación).


### 4. **Análisis del Código**

El código comienza importando las librerías necesarias. `os` se utiliza para interactuar con el sistema de archivos, permitiendo navegar entre directorios y realizar operaciones como listar archivos o combinar rutas. `shutil` se emplea para mover archivos entre carpetas, mientras que `hashlib` genera hashes únicos para los archivos, lo que permite identificar y eliminar duplicados. Por último, `ebooklib` es la librería especializada que facilita la lectura de los archivos EPUB y la extracción de sus metadatos, como el autor, el título y el año de publicación.

```python
import os
import shutil
import hashlib
from ebooklib import epub
```

En cuanto a las funciones auxiliares, `calcular_hash` es responsable de generar un hash único para cada archivo EPUB. Este hash se genera utilizando el algoritmo SHA-256 y se calcula leyendo el archivo en fragmentos de 8192 bytes, una técnica útil para evitar problemas de rendimiento cuando se procesan archivos grandes.

```python
def calcular_hash(archivo):
    hash_sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
```

Luego, `crear_directorio_si_no_existe` verifica si una carpeta en una ruta específica ya existe; si no, la función crea dicha carpeta, lo cual es esencial para organizar los libros por autor dentro de la carpeta "ordenados".

```python
def crear_directorio_si_no_existe(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)
```

La función `extraer_metadatos_epub` utiliza `ebooklib` para extraer los metadatos clave de cada archivo EPUB: el título, el autor y el año de publicación. Si alguno de estos datos no se encuentra disponible en el archivo, la función devuelve `None` en lugar del valor correspondiente.

```python
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
```

Por su parte, `formato_autor` es la encargada de transformar el nombre completo del autor en el formato "Apellido(s), Nombre(s)", reordenando las partes del nombre para ajustarse al formato deseado. Si el formato no puede ser transformado correctamente, el nombre original es retornado sin cambios.

```python
def formato_autor(autor):
    if autor:
        partes = autor.split()
        if len(partes) > 1:
            apellido = partes[-1]
            nombres = " ".join(partes[:-1])
            return f"{apellido}, {nombres}"
    return autor
```

El script también cuenta con la función `registrar_error`, que abre o crea un archivo llamado `errores.txt` y agrega una línea con la descripción de cualquier problema que ocurra durante el procesamiento. Esta función es útil para tener un registro de los archivos que no pudieron ser procesados correctamente.

```python
def registrar_error(ruta, archivo, error):
    with open("errores.txt", "a") as f:
        f.write(f"Error en {ruta}/{archivo}: {error}\n")
```

El núcleo del script reside en la función `mover_y_renombrar_libros`, que recorre de manera recursiva el directorio "aordenar" buscando archivos EPUB. Si encuentra un archivo, extrae sus metadatos mediante la función `extraer_metadatos_epub`. Si no se puede extraer el título o el autor, se lanza una excepción y se registra el error en `errores.txt`.

```python
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
                    autor, titulo, año = extraer_metadatos_epub(ruta_completa)
                    if not autor or not titulo:
                        raise ValueError("Metadatos faltantes (autor o título)")
```

Una vez que se han extraído y validado los metadatos, se crea el formato del autor (usando `formato_autor`) y del año. Si el año está disponible, se coloca entre paréntesis; si no, se deja en blanco. El archivo es renombrado con el formato "Autor - Título - (Año)", y luego es movido a la carpeta correspondiente dentro de "ordenados", creando la carpeta del autor si es necesario.

```python
                    autor_formateado = formato_autor(autor)
                    if not autor_formateado:
                        raise ValueError("No se pudo formatear el nombre del autor")

                    año_formateado = f"({año})" if año else ""

                    directorio_autor = os.path.join(directorio_ordenado, autor_formateado)
                    crear_directorio_si_no_existe(directorio_autor)

                    nuevo_nombre = f"{autor_formateado} - {titulo} {año_formateado}.epub".replace("/", "-")
                    nueva_ruta = os.path.join(directorio_autor, nuevo_nombre)
```

Antes de mover un archivo, el script calcula su hash mediante `calcular_hash` y verifica si ese hash ya existe en un conjunto de hashes procesados, lo que permite evitar duplicados. Si el archivo es nuevo (no duplicado), se mueve y su hash es añadido al conjunto; en caso contrario, el archivo duplicado se omite y no se procesa.

```python
                    hash_actual = calcular_hash(ruta_completa)
                    if hash_actual not in hashes_archivos:
                        shutil.move(ruta_completa, nueva_ruta)  # Mover y renombrar el archivo
                        hashes_archivos.add(hash_actual)
                        libros_procesados += 1
                    else:
                        print(f"Duplicado encontrado y eliminado: {ruta_completa}")
```

Si ocurre algún error durante el procesamiento (por ejemplo, falta de metadatos), el error se registra en el archivo `errores.txt`.

```python
                except Exception as e:
                    registrar_error(root, file, str(e))
```

Finalmente, el script define las rutas base para las carpetas "aordenar" y "ordenados", asumiendo que el script está ubicado en la raíz del proyecto. Luego, llama a la función principal `mover_y_renombrar_libros` para iniciar el procesamiento de los libros, moviéndolos, renombrándolos y eliminando duplicados según sea necesario.

```python
directorio_base = os.getcwd()  # Asume que el script está en la raíz de las carpetas
directorio_aordenar = os.path.join(directorio_base, "aordenar")
directorio_ordenado = os.path.join(directorio_base, "ordenados")

mover_y_renombrar_libros(directorio_aordenar, directorio_ordenado)
```

Este proyecto ofrece una solución automatizada y eficiente para organizar grandes colecciones de libros EPUB, aprovechando los metadatos disponibles y manejando los errores y duplicados de manera sencilla.
