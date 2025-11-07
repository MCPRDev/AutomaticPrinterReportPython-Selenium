# 🤖 Generador Automático de Reportes de Impresora

Este proyecto es una herramienta de automatización en Python diseñada para extraer, procesar y consolidar reportes de uso de impresoras directamente desde su interfaz de administración web.

Automatiza la tediosa tarea de iniciar sesión en múltiples impresoras, descargar los reportes de contabilidad de uso (en formato `.csv`), seleccionar columnas específicas, y unificar los datos en un solo archivo `.xlsx` con hojas separadas para cada impresora.

## 📋 Características Principales

* **Automatización Web:** Utiliza **Selenium** para navegar la interfaz web de las impresoras.
* **Ejecución Silenciosa:** Se ejecuta en modo **headless** (sin interfaz gráfica) para no interrumpir al usuario y para ocultar las credenciales en pantalla durante el proceso.
* **Procesamiento de Datos:** Utiliza **Pandas** para filtrar, renombrar y ordenar las columnas de interés de los reportes crudos.
* **Reporte Unificado:** Combina los datos de dos (o más) impresoras en un único archivo Excel (`.xlsx`), guardado automáticamente en el Escritorio del usuario.
* **Interfaz CLI Amigable:** Muestra una barra de progreso limpia en la terminal (usando `tqdm`) para informar al usuario sobre el estado del proceso en tiempo real.
* **Manejo de Errores y Limpieza:** Incluye logging robusto, manejo de excepciones, y borrado automático de archivos y carpetas temporales al finalizar.

## ⚙️ Cómo Funciona (Arquitectura)

El flujo de trabajo está orquestado por `controller_cli.py` y se divide en tres fases claras:

1.  **Fase 1: Adquisición de Datos (Selenium)**
    * El script (`autodownload_report.py`) inicia un `ChromeDriver` en modo headless.
    * Navega a la IP de la Impresora 1.
    * Inicia sesión con las credenciales de administrador.
    * Navega a la página de reportes de uso y descarga el archivo `.csv`.
    * Espera a que la descarga se complete (verificando que no sea un `.crdownload`) y cierra la sesión de forma segura.
    * Repite el proceso para la Impresora 2.

2.  **Fase 2: Procesamiento de Datos (Pandas)**
    * El script (`auto_printer_report.py`) toma los dos archivos `.csv` descargados.
    * Para cada archivo, lee el `.csv`, omite la primera fila (metadatos/títulos irrelevantes) y selecciona solo las columnas de interés usando sus índices (ej. `[0, 3, 5, 10]`).
    * Renombra las columnas a un formato legible (ej. "Nombre de Cuenta", "Total impresiones negro") y ordena los datos alfabéticamente.

3.  **Fase 3: Consolidación y Limpieza**
    * Se crea un nuevo archivo Excel (`Reporte_impresoras_AAAA-MM-DD.xlsx`) en el Escritorio del usuario.
    * El reporte procesado de la Impresora 1 se guarda en la hoja "Printer\_1".
    * El reporte procesado de la Impresora 2 se guarda en la hoja "Printer\_2".
    * El script elimina las carpetas y archivos `.csv` temporales creados durante la descarga para no dejar basura.
    * La CLI muestra un mensaje de éxito con la ruta exacta al archivo final.

## 🛠️ Requisitos Previos

Antes de ejecutar el script, necesitas:

* **Python 3.x**
* **Google Chrome** (El navegador debe estar instalado).
* **ChromeDriver** (Debe ser compatible con tu versión de Google Chrome).
    * Puedes descargarlo desde: [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)

## 🚀 Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar `autodownload_report.py` (¡Muy Importante!):**
    Abre el archivo `autodownload_report.py` y modifica las siguientes variables:

    ```python
    # Línea 24: Credenciales de administrador de la impresora
    self.printer_admin_user = "TuUsuarioAdmin"
    self.printer_admin_password = "TuPasswordSeguro"

    # Línea 34: Ruta al ChromeDriver que descargaste
    # ¡IMPORTANTE! Usa doble barra invertida (\\) en Windows o una ruta absoluta
    service = Service(executable_path=r"C:\\Ruta\\Completa\\A\\chromedriver.exe")

    # Línea 41: IP de la primera impresora
    # Debe coincidir con la primera IP en la lista de controller_cli.py
    if ip == "111.111.111.111": 
        # ...
    ```

    > **Nota:** Si la interfaz web de tu impresora (los IDs de los botones) es diferente, deberás actualizar los selectores de ID en los métodos `login()`, `log_out()` y `download_csv()`.

5.  **Configurar `controller_cli.py`:**
    Abre el archivo `controller_cli.py` y define las IPs de tus impresoras en la lista `ips`:

    ```python
    # Línea 32: Actualiza esta lista con las IPs de tus impresoras
    if __name__ == "__main__":
        ips = ["111.111.111.111", "222.222.222.222"] 
        # ...
    ```

6.  **Configurar `auto_printer_report.py` (Opcional):**
    Si tu reporte CSV tiene una estructura diferente, ajusta los índices de las columnas que quieres extraer y sus nombres:

    ```python
    # Línea 14: Índices de las columnas (empezando en 0) a extraer
    indices_deseados = [0, 3, 5, 10]
    
    # Línea 18: Nombres para las nuevas columnas (debe coincidir en número)
    columnas_escritor = [
        "Nombre de Cuenta",
        "Total de impresiones impresas y copias negro",
        "Uso copias negro",
        "Uso impresiones negro"
    ]
    ```

## ▶️ Uso

Una vez que todo esté configurado, simplemente ejecuta el script `controller_cli.py` desde tu terminal (asegúrate de tener el entorno virtual activado):

```bash
python controller_cli.py
Verás la barra de progreso en acción. Al finalizar, el script imprimirá la ruta completa al archivo Excel generado en tu Escritorio.
✅ Proceso Finalizado: 100% |██████████| {postfix="¡Completado!"}
...
=====================================================================
✅ PROCESO COMPLETADO CON ÉXITO ✅
=====================================================================

Copia la siguiente ruta del reporte final:

   C:\Users\TuUsuario\Desktop\Reporte_impresoras_2025-11-06.xlsx

=====================================================================
El proceso ha terminado. Presiona 'Enter' para salir de la ventana.
