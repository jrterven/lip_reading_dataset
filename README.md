# Creación de base de datos para lectura de labios
Este repositorio contiene el código fuente para generar una base de datos que puede ser usada para entrenar sistemas de reconocimiento de habla a partir de información visual. La alineación de texto y video tiene precisión de milisegundos gracias al motor de Audio-a-Texto de IBM. 
El procedimiento puede usarse para cualquier idioma simplemente usando videos en el idioma deseado.
La salida generada consiste en un archivo CSV con los siguientes campos:

| Anotación        | Descripción  | 
| ------------- |:-------------:|
| texto         | Texto hablado en el video |
| conf          | Nivel de confianza de la detección en un rango de 0 a 1       |
| start         | Tiempo inicial del video que contiene el texto en segundos.   |
| end           | Tiempo final del video que contiene el texto.                 |
| bounding_box  | Coordenadas de rectángulo de la cara en píxeles (x, y, ancho, alto)      |
| link          | Enlace de video de YouTube omitiendo el inicio (www.youtube.com)         |


# Procedimiento

## 1. Descargar los videos y colocarlos en un directorio.
Se pueden generar varios directorios para distintas categorias. E.g. noticias, blogs, etc.
## 2. Extraer el audio de los videos 
Para extraer el audio en archivo .wav ejecute el script **extract_wav_files.py**
```
python extract_wav_files.py --dir [directorio] --cat [categoria]
```
donde:
- *directorio* es la ruta la directorio principal del paso 1   
- *categoria* es la categorio (o subdirectorio). 

Por ejemplo si los videos estan dentro de *c:/videos/noticias* 
```
python extract_wav_files.py --dir c:/videos --cat noticias
```

## 3. Extraer texto de los videos
Para extraer el texto de los videos hacemos uso del motor **text-to-speech** de IBM.
Para poder ejecutar esta parte, se necesita crear una cuenta en [IBM Cloud](https://idaas.iam.ibm.com/idaas/mtfim/sps/authsvc?PolicyId=urn:ibm:security:authentication:asf:basicldapuser). Posteriormente se necesita crear un recurso de tipo **Speech to Text** para obtener el nombre de usuario y contraseña.
Una vez teniendo estos datos abra el archivo **extract_detailed_text_watson.py** y edite los campos **IBM_USERNAME** y **IBM_PASSWORD**. Luego ejecute el script como se muestra a continuación.
```
python extract_detailed_text_watson.py --dir [directorio] --cat [categoria]
```

## 4. Extraer subvideos
Una vez que se tienen los subtitulos de cada video. Ejecute **extract_subvideos2.py**
```
python extract_subvideos2.py --dir [directorio] --cat [categoria] --vids_log [archivo_log] --results_dir [directorio_de_resultados] --ann_file [archivo_de_anotaciones]
```
donde:
- *directorio* es la ruta la directorio principal del paso 1   
- *categoria* es la categorio (o subdirectorio). 
- *archivo_log* es el nombre del archivo donde se almacenan los nombres de los videos previamente procesados. Este archivo se crea (si no existe) y se guarda dentro de *directorio_de_resultados*.
- *directorio_de_resultados* ruta del directorio donde se desean almacenar los resultados
- *archivo_de_anotaciones* nombre del archivo donde se guardan las anotaciones.

**Publicacion**
Base de datos para reconocimiento de habla audio-visual. 
Mejia Kenneth, Perales Pamela,  Morales Raul, Córdova Diana, Romero Alejandro, Terven Juan.
En revision.

Licencia
----

MIT