from Autodownload_report import automate_python_script_report
from auto_printer_report import combine_sheets
from logger import configurar_logger_temporal
import shutil
import time

logger = configurar_logger_temporal()

def encapsulamiento_report(ip):
        automate = automate_python_script_report(ip)
        time.sleep(2)
        
        if not automate.login():
            raise Exception(f"Fallo de login para IP: {ip}")
        
        time.sleep(1)
        try:
            automate.download_csv()
            time.sleep(2)
            archivo = automate.obtener_archivo_descargado()
            path_descargado = automate.giving_path()
            return archivo, path_descargado
        finally:
            time.sleep(1)
            automate.log_out()
            automate.close_driver()

def remove_mk(path):
    try:
        shutil.rmtree(path)
        logger.info(f"Carpeta {path} eliminada con éxito.")
    except OSError as e:
        logger.error(f"Error al eliminar la carpeta: {e}")

if __name__ == "__main__":
    ips = ["123.123.123.123", "321.321.321.321"] # Sustituir ips

    archivo_impresora_1_primero = None
    archivo_impresora_2_segundo = None

    logger.info("Iniciando proceso de reporte...")
    logger.info("IPs Registradas")
    logger.info(f"IP IMPRESORA REGISTRADA IMPRESORA 1 REGISTRADA: {ips[0]}")
    logger.info(f"IP IMPRESORA REGISTRADA IMPRESORA 2 REGISTRADA: {ips[1]}")

    try:
        logger.info(f"Trabajando IP: {ips[0]}")
        archivo_impresora_1_primero, path_registrado_1 = encapsulamiento_report(ips[0])

        logger.info(f"Trabajando IP: {ips[1]}")
        archivo_impresora_2_segundo, path_registrado_2 = encapsulamiento_report(ips[1])

        if archivo_impresora_1_primero is not None and archivo_impresora_2_segundo is not None:
             logger.info("Realizando reporte...")
             combine_sheets(archivo_impresora_1_primero, archivo_impresora_2_segundo)
             logger.info("Reporte finalizado con exito")
        
        if path_registrado_1 is not None and path_registrado_2 is not None:
            paths = [path_registrado_1, path_registrado_2]
            for p in range(len(paths)):
                remove_mk(paths[p])
                logger.info(f"Eliminando: {paths[p]}")
            logger.info(f"Se han eliminado con exito.")
            logger.info("Creador de reporte Version 1.0.0 Finalizado")

    except Exception as e:
        logger.info(f"Error Controller.py: {e}")