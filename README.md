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


