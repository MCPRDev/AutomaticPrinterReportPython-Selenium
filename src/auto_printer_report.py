import pandas as pd
from datetime import date
import os
from pathlib import Path
from logger import configurar_logger_temporal

logger = configurar_logger_temporal()

def report_sorter(archive_name):
    try:

        df = pd.read_csv(archive_name, skiprows=1, header=None)

        indices_deseados = [0, 3, 5, 10]
        df_filtrado = df.iloc[:, indices_deseados]

        columnas_escritor = [
            "Nombre de Cuenta",
            "Total de impresiones impresas y copias negro",
            "Uso copias negro",
            "Uso impresiones negro"
        ]
        df_filtrado.columns = columnas_escritor

        df_ordenado = df_filtrado.sort_values(by="Nombre de Cuenta")
        logger.info(f"Realizando filtrado de hoja: {archive_name}")
        return df_ordenado

    except Exception as e:
        logger.error(f"Error report_sorter: {e}")
        return None


def combine_sheets(primer_documento_csv, segundo_documento_csv):

    home_dir = Path.home() 
    desktop_dir = None
    
    if os.name == 'nt': # Si es Windows
        
        opciones_escritorio = ["Desktop", "Escritorio"]
        
        for carpeta in opciones_escritorio:
            ruta_candidata = home_dir / carpeta
            if ruta_candidata.exists() and ruta_candidata.is_dir():
                desktop_dir = str(ruta_candidata)
                break
        
        if desktop_dir is None:
             desktop_dir = home_dir / "Desktop"
             logger.warning(f"No se encontró 'Desktop' ni 'Escritorio'. Usando la ruta por defecto: {desktop_dir}")

        else: # Linux, macOS, etc. (Donde casi siempre es "Desktop")
            desktop_dir = home_dir / "Desktop"


    current_date = date.today()
    nombre_archivo = f'Reporte_impresoras_{current_date}.xlsx'
    archivo_salida_combinado = desktop_dir / nombre_archivo

    impresora_1_sheet_name = "Printer_1"
    impresora_2_sheet_name = "Printer_2"

    logger.info(f"Procesando {primer_documento_csv}...")
    hoja_impresora_1 = report_sorter(primer_documento_csv)

    logger.info(f"Procesando {segundo_documento_csv}...")
    hoja_impresora_2 = report_sorter(segundo_documento_csv)

    if hoja_impresora_1 is not None and hoja_impresora_2 is not None:
        try:
            with pd.ExcelWriter(archivo_salida_combinado, engine='openpyxl') as writer:
                
                hoja_impresora_1.to_excel(
                    writer, 
                    sheet_name=impresora_1_sheet_name, 
                    index=False
                )
                
                hoja_impresora_2.to_excel(
                    writer, 
                    sheet_name=impresora_2_sheet_name, 
                    index=False
                )
            logger.info(f"Exitoso, se han creado el reporte: {archivo_salida_combinado}")
            return archivo_salida_combinado
        except Exception as e:
            logger.error(f"Error al guardar el archivo Excel combinado: {e}")
    else:
        logger.warning("No se pudo crear el archivo combinado porque uno o más archivos de entrada fallaron.")

#if __name__ == "__main__":
#    first = 'Documentazo2.csv'
#    second = 'Documentazo2.csv'
#    combine_sheets(first, second)