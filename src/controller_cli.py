from Autodownload_report import automate_python_script_report
from auto_printer_report import combine_sheets
from logger import configurar_logger_temporal
import shutil
import time
from tqdm import tqdm
import os

logger = configurar_logger_temporal()

def encapsulamiento_report(ip):
        automate = automate_python_script_report(ip)
        time.sleep(3)
        
        if not automate.login():
            raise Exception(f"Fallo de login para IP: {ip}")
        
        time.sleep(2)
        try:
            automate.download_csv()
            time.sleep(3)
            archivo = automate.obtener_archivo_descargado()
            path_descargado = automate.giving_path()
            return archivo, path_descargado
        finally:
            time.sleep(2)
            automate.log_out()
            automate.close_driver()

def remove_mk(path):
    try:
        shutil.rmtree(path)
        logger.info(f"Carpeta {path} eliminada con éxito.")
    except OSError as e:
        logger.error(f"Error al eliminar la carpeta: {e}")

if __name__ == "__main__":
    ips = ["111.111.111.111", "222.222.222.222"]

    archivo_impresora_numero_1 = None
    archivo_impresora_numero_2 = None

    logger.info("Iniciando proceso de reporte...")
    logger.info("IPs Registradas")
    logger.info(f"IP IMPRESORA REGISTRADA IMPRESORA 1 REGISTRADA: {ips[0]}")
    logger.info(f"IP IMPRESORA REGISTRADA IMPRESORA 2 REGISTRADA: {ips[1]}")

    total_steps = 4
        
    terminal_width = shutil.get_terminal_size(fallback=(100, 24)).columns

    try:
        with tqdm(total=total_steps,
                  desc="Procesando",
                  ncols=terminal_width - 10,
                  bar_format="{l_bar} {percentage:3.0f}% |{bar}| {postfix}",
                  postfix={"task": "Iniciando..."}) as pbar:
            
            pbar.set_postfix(task=f"Descargando reporte impresora 1 (IP: Protegida...)")
            logger.info(f"Trabajando IP: {ips[0]}")
            archivo_impresora_numero_1, path_registrado_1 = encapsulamiento_report(ips[0])
            pbar.update(1)

            pbar.set_postfix(task=f"Descargando reporte impresora 2 (IP: Protegida...)")
            logger.info(f"Trabajando IP: {ips[1]}")
            archivo_impresora_numero_2, path_registrado_2 = encapsulamiento_report(ips[1])
            pbar.update(1)

            if archivo_impresora_numero_1 is not None and archivo_impresora_numero_2 is not None:
                pbar.set_postfix(task="Combinando reportes...")
                logger.info("Realizando reporte...")
                path_reporte_final = combine_sheets(archivo_impresora_numero_1, archivo_impresora_numero_2)
                logger.info("Reporte finalizado con exito")
            
            pbar.update(1)
            
            if path_registrado_1 is not None and path_registrado_2 is not None:
                pbar.set_postfix(task="Limpiando archivos temporales...")
                paths = [path_registrado_1, path_registrado_2]
                for p in range(len(paths)):
                    remove_mk(paths[p])
                    logger.info(f"Eliminando: {paths[p]}")
                logger.info(f"Se han eliminado con exito.")

            pbar.update(1)
            pbar.set_postfix(task="¡Completado!")
            pbar.set_description("✅ Proceso Finalizado")

            logger.info("Creador de reporte Version 1.0.0 Finalizado")
            print("\n" * 3) # Espaciado
            print("=" * terminal_width)
            if path_reporte_final:
                print("✅ PROCESO COMPLETADO CON ÉXITO ✅".center(terminal_width))
                print("=" * terminal_width)
                print("\nCopia la siguiente ruta del reporte final:")
                print(f"\n   {path_reporte_final}\n")
            else:
                print("⚠️ PROCESO FINALIZADO (RUTA DE REPORTE NO CAPTURADA) ⚠️".center(terminal_width))
                print("=" * terminal_width)
                print("\nEl script se ejecutó, pero la variable con la ruta final está vacía.")
                print("Asegúrate de que la función 'combine_sheets' retorne la ruta del archivo.")

    except Exception as e:
        logger.info(f"Error Controller.py: {e}", exc_info=True)
        print("\n" * 3)
        print("=" * terminal_width)
        print("❌ ERROR DURANTE LA EJECUCIÓN ❌".center(terminal_width))
        print("=" * terminal_width)
        print(f"\nDetalle del error: {e}\n")
        print("Revisa el archivo de log para más información.")
    finally:
        print("=" * terminal_width)
        print("El proceso ha terminado. Presiona 'Enter' para salir de la ventana.")
        input()