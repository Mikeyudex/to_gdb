import logging
import os
import sys

def setup_logger(log_file):
    # Configurar el formato de los logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configurar el manejador de archivos para escribir en un archivo de texto
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Configurar el manejador de la consola para mostrar los logs en la ventana de comandos
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Crear un logger y establecer el nivel de registro deseado (por ejemplo, DEBUG, INFO, WARNING, ERROR)
    logger = logging.getLogger('flask_logger')
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    return logger

# Directorio donde se guardarán los logs
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_directory, exist_ok=True)

# Ruta completa al archivo de logs
log_file = os.path.join(log_directory, 'flask_app.log')

# Configurar el logger y obtener una instancia del logger configurado
logger = setup_logger(log_file)
