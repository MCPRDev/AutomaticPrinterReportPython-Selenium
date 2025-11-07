import os
import time
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from logger import configurar_logger_temporal
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class automate_python_script_report():
    def __init__(self, ip):

        self.logger = configurar_logger_temporal()

        self.printer_admin_user = "Usuario_Administrador_Reemplazar" #User printer debe ser admin
        self.printer_admin_password = "Super_Secure_Password" #Password printer debe ser admin

        self.ip = ip

        login_web = f"https://{ip}/properties/authentication/login.php" #Pagina de login principal
        self.usage_report_web = f"https://{ip}/properties/accounting/usageReport.php?from=Acct_Home" #Pagina donde se descarga el reporte

        try:
            service = Service(executable_path=r"\\hostname\usuario\ChromeDriver\chromedriver.exe") # Ruta donde se ubica el chrome driver, esta debe estar establecida de acceso publico

            user_log_in_windows = os.getlogin()
            if ip == "ip_determinada":
                carpeta_impresora_1 = f"{str(ip)}_Impresora_1"
                path = Path(f"C:\\Users\\{user_log_in_windows}\\Documents\\{carpeta_impresora_1}")
                if path.exists():
                    self.logger.info("Carpeta " + carpeta_impresora_1 + " existe, utilizandola para descargar reporte")
                    self.download_path = str(path)
                else:
                    path.mkdir(parents=True, exist_ok=True)
                    self.logger.info("Carpeta " + carpeta_impresora_1 + " no existe, creandola")
                    self.download_path = str(path)
            
            else:
                carpeta_impresora_2 = f"{str(ip)}_impresora_2"
                path = Path(f"C:\\Users\\{user_log_in_windows}\\Documents\\{carpeta_impresora_2}")
                if path.exists():
                    self.logger.info("Carpeta " + carpeta_impresora_2 + " existe, utilizandola para descargar reporte")
                    self.download_path = str(path)
                else:
                    path.mkdir(parents=True, exist_ok=True)
                    self.logger.info("Carpeta " + carpeta_impresora_2 + "no existe, creandola")
                    self.download_path = str(path)
            

            self.old_items = set(os.listdir(self.download_path)) # obtenemos los archivos actuales en la carpeta, por si acaso hay archivos demas y verificar cual es el archivo actual

            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument('--ignore-ssl-errors=yes') #Ignorar certificados
            options.add_argument('--ignore-certificate-errors') #Ignorar certificiados
            options.add_argument('--headless') #Ignorar certificiados
            options.add_experimental_option("prefs", {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get(login_web)
        except Exception as e:
            self.logger.error(f"Error Init autodownload_report: {e}")
    
    def login(self):
        try:
            login_web_user_name = "frmwebUsername" #Id del elemento en la aplicacion web
            login_web_password_name = "frmwebPassword" #Id del elemento en la aplicacion web

            login_user = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, login_web_user_name))
            )


            login_password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, login_web_password_name))
            )

            login_user.send_keys(self.printer_admin_user)
            login_password.send_keys(self.printer_admin_password, Keys.ENTER)

            self.logger.info(f"Log in exitoso de: {self.ip}")
            return True
        except Exception as e:
            self.logger.error(f"Error Login: {e}")
            return False

    def log_out(self):
        try:
            log_out_profile_id = "LogoutLink" #Boton para expandir la bandeja de Profile
            log_out_web_button_id = "log-out" #ID para el boton de desconectarse

            log_out_profile_button = self.driver.find_element(By.ID, log_out_profile_id)
            log_out_profile_button.click()

            log_out_button = WebDriverWait(self.driver, 10).until( 
                EC.element_to_be_clickable((By.ID, log_out_web_button_id))
                )
            log_out_button.click()
            time.sleep(2)
            self.logger.info(f"Log out exitoso de: {self.ip}")
            return True
        except Exception as e:
            self.logger.error(f"Error log out: {e}")
            return False

    def download_csv(self):
        try:
            self.driver.get(self.usage_report_web)
            download_report_id = "download-report" #ID de boton para descargar el reporte de la impresora

            download_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, download_report_id))
            )
            download_button.click()
            self.logger.info("Descargando...")
        except Exception as e:
            self.logger.error(f"Error Download: {e}")

    def obtener_archivo_descargado(self, timeout=120):
        tiempo = 0
        while tiempo < timeout:
            archivos_actuales = set(os.listdir(self.download_path))
            nuevos = archivos_actuales - self.old_items
            for archivo in nuevos:
                if not archivo.endswith(".crdownload") and archivo.endswith(".csv"):  # Asegura que esté completo
                    self.logger.info(f"Archivo Obtenido: {archivo}")
                    path_archivo = self.download_path + "\\" + archivo
                    self.logger.info(f"Path archivo: {path_archivo}")
                    return path_archivo
            time.sleep(1)
            tiempo += 1
        self.logger.error("Sin archivo retornado, error")
        return None

    def giving_path(self):
        try:
            path = self.download_path
            self.logger.info(f"Path obtenido: {path}")
            return path
        except Exception as e:
            self.logger.error(f"Error obteniendo path: {e}")
            return None


    def close_driver(self):
        self.logger.info("Chrome Driver Cerrado Cerrado.")
        self.driver.close()
    
    
#if __name__ == "__main__":
#    automate = automate_python_script_report("123.123.123.123")
#    automate.login()
#    time.sleep(2)
#    automate.download_csv()
#    time.sleep(2)
#    path = automate.giving_path()
#    archivo = automate.obtener_archivo_descargado()
#    time.sleep(2)
#    automate.log_out()
#    automate.close_driver()