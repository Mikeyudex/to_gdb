
# Servicio export to GDB 

Servicio web encargado de ejecutar proceso de generar FGDB(File Geodatabase) a partir de una url de Feature Service.

## Requisitos del Sistema

- Python 3.8: Asegúrate de tener Python 3.8 instalado en tu sistema.
- Instalar virtualenv en windows o en linux venv.
- Paquetes requeridos: Instala los paquetes requeridos ejecutando `pip install -r requirements.txt`.

## Configuración

1. Clona el repositorio: `git clone https://github.com/tu_usuario/tu_repositorio.git`
2. Accede al directorio del proyecto: `cd tu_repositorio`
3. Crea y activa un entorno virtual (opcional): Recomendamos utilizar un entorno virtual para mantener las dependencias del proyecto aisladas del sistema global.
4. Instala las dependencias: `pip install -r requirements.txt`
5. Configura las variables de entorno: Si el proyecto utiliza variables de entorno, crea un archivo `.env` y configura las variables necesarias. Puedes tomar como base el archivo `.env.example` si está disponible.

## Ejecución

1. Ejecuta la aplicación: `python app.py`
2. Abre tu navegador web y accede a la URL: `http://localhost:{port}` (o la URL correspondiente si se especifica otra en la configuración)

## Uso

El servicio web ofrece los siguientes endpoints para interactuar con el proyecto:

Obtener información de usuario
Endpoint: /api/v1/export-gdb

Método: POST

Descripción: Obtiene la url de la gdb generada.

Ejemplo de uso:

POST /api/v1/export-gdb HTTP/1.1
Host: localhost:{port}
Content-Type: application/json

{
    "name": "pozos",
    "url_service": "https://arcgis-pliga-dev.is.arqbs.com/arcgis/rest/services/PIGA/PIGA_ALL_GEODB/MapServer/0/query",
    "project" : "EPSG:4326"
}

Respuesta exitosa:

HTTP/1.1 200 exited
Content-Type: application/json

{
    "success": true,
    "url_file": "https://objectstorage.us-phoenix-1.oraclecloud.com/p/aMaQWfhhVs0CMoDgms8JDya2K79Q-mKOD7mb-Ip-zY0WNcWNFSZYPZwSOJrlB2yR/n/axt4go93zyed/b/pliga-bucket/o/pozos_fdead55e-cb80-4a03-8c9e-a081d071893c.zip"
}


## Contribución

Si deseas contribuir al proyecto, sigue estos pasos:

1. Crea un branch: `git checkout -b mi-feature`
2. Realiza tus cambios y realiza commits: `git commit -m "Agrega nueva funcionalidad"`
3. Sube los cambios a tu repositorio: `git push origin mi-feature`
4. Abre una pull request en GitHub para revisar los cambios propuestos.

## Licencia

MIT.

## Contacto

Si tienes preguntas o comentarios sobre el proyecto, puedes contactarme a través de [miguel.garcia@ludycom.com] o abrir un issue en GitHub.

---
