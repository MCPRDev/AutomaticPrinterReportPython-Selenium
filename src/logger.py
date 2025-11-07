import logging
import tempfile
import os
from datetime import datetime
from pathlib import Path

def configurar_logger_temporal():

    nombre_logger = f"printer_report"
    
    # 1. Definir la ruta del archivo de log en la carpeta temporal
    # tempfile.gettempdir() obtiene la ruta de la carpeta temporal (ej: /tmp o C:\Users\...\AppData\Local\Temp)
    carpeta_temp = Path(tempfile.gettempdir())
    
    # Creamos un nombre de archivo único para evitar conflictos
    # Usamos f-string para incluir el nombre de la aplicación
    nombre_archivo = f"{nombre_logger}_temp.log"
    archivo_log = carpeta_temp / nombre_archivo
    
    # 2. Configurar el logger principal (El orquestador)
    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.DEBUG) 

    # Evita la adición de handlers duplicados si se llama de nuevo
    if logger.handlers:
        return logger
    
    # 3. Formatter (El Estilo)
    # Define la estructura del mensaje
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - (%(name)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 4. Handlers (Los Destinos)
    
    # a) Handler para Archivo (FileHandler)
    # Envía todos los logs (DEBUG o superior) al archivo temporal
    file_handler = logging.FileHandler(archivo_log, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG) 
    file_handler.setFormatter(formatter)

    # 5. Conectar los handlers al logger
    logger.addHandler(file_handler)
    
    return logger