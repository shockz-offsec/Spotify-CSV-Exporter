import os
import time
import platform
import json
import shutil
import logging
from datetime import datetime
import tarfile
import urllib.request
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService

def login(email, password):
    try:
        logging.info("Logging in...")
        driver.get('https://watsonbox.github.io/exportify/')
        get_started = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginButton"]')))
        driver.execute_script("arguments[0].click();", get_started)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-username"]')))
        # Email
        email_input = driver.find_element(By.XPATH, '//*[@id="login-username"]')
        email_input.send_keys(email)
        time.sleep(1)
        # Password
        password_input = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        password_input.send_keys(password)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        try:
            accept = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[3]/button')))
            driver.execute_script("arguments[0].click();", accept)
            logging.info("Successful login")
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/table/thead/tr/th[7]/button')))
            logging.info("Successful login")
        except:
            logging.error("Login failed")
            driver.execute_script("window.open('','_self').close();")
            driver.quit()
            exit(1)

    except Exception as e:
        logging.exception("An error has occurred in the authentication phase: %s", e)
        driver.execute_script("window.open('','_self').close();")
        driver.quit()
        exit(1)


def download():
    export_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/table/thead/tr/th[7]/button')))
    driver.execute_script("arguments[0].click();", export_all)

    logging.info("Downloading...")

    try:
        while True:
            # Find the ZIP file with .zip extension and without the temporary prefix
            filename = [filename for filename in os.listdir(download_path) if filename.endswith(".zip") and not filename.endswith(".crdownload")]
            
            if filename: # If you find a ZIP file
                filepath = os.path.join(download_path, filename[0]) # Gets the full path to the file
                size = os.path.getsize(filepath) # Gets the file size
                time.sleep(1)
                
                # Checks if the file size has stabilized in the last 30 seconds
                for _ in range(120):
                    if os.path.getsize(filepath) != size: # If the size has changed
                        size = os.path.getsize(filepath) # Update file size
                        time.sleep(1) 
                    else: # If the size has not changed
                        break # Exits the for loop
                else: # If the time limit is reached
                    logging.error("The ZIP file download could not be completed in the expected time.")
                break # Exits the for loop
            else: # If no ZIP file is found
                time.sleep(1)

    except Exception as e:
        logging.exception(f"Error while waiting for download: {e}")
    finally:
        time.sleep(5)

    # Close the browser
    try:
        driver.execute_script("window.open('','_self').close();")
        driver.quit()
    except:
        pass

    filename_path = max([os.path.join(download_path, f) for f in os.listdir(download_path)], key=os.path.getctime)
    logging.info(f"Export downloaded: {os.path.basename(filename_path)}")


if __name__ == "__main__":

    # Import config
    data = {}
    json_file_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config_spotify.json'))
    with open(json_file_path, encoding='utf-8') as file:
        data = json.load(file)

    ## Global variables ##
    today = datetime.today().strftime('%d-%m-%Y')
    log_dat = datetime.today().strftime('%Y-%m-%d')
    # Basic configuration of the registry
    if not os.path.exists(data["DEBUG_PATH"]):
        os.makedirs(data["DEBUG_PATH"], mode=0o777)

    logging.basicConfig(filename=os.path.join(data["DEBUG_PATH"], f'debug-{log_dat}.log'),
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    # Console registry configuration
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    ##################### Driver management #################

    # Download Firefox driver
    try:
        if platform.system() == 'Windows':
            driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
            if not os.path.isfile(driver_path):
                logging.info("Installing Geckodrive")
                url = 'https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-win64.zip'
                with urllib.request.urlopen(url) as response, open('geckodriver.zip', 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                with ZipFile('geckodriver.zip', 'r') as zipObj:
                    zipObj.extractall(os.getcwd())
                os.remove('geckodriver.zip')
            else:
                logging.info("Geckodrive ready!")
        else:
            driver_path = os.path.join(os.getcwd(), 'geckodriver')
            if not os.path.isfile(driver_path):
                logging.info("Installing Geckodriver")
                url = 'https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz'
                with urllib.request.urlopen(url) as response, open('geckodriver.tar.gz', 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                with tarfile.open('geckodriver.tar.gz', 'r:gz') as tarObj:
                    tarObj.extractall(os.getcwd())
                os.remove('geckodriver.tar.gz')
            else:
                logging.info("Geckodrive ready!")
    except Exception as e:
        logging.exception("An error occurred in the download phase of the webdriver: %s", e)

    # Driver options
    options = Options()
    # Configure download options in Firefox
    download_path = data["DOWNLOAD_PATH"]
    options.set_preference("browser.charset.default", "UTF-8")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_path)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
    options.add_argument("-headless")

    # Start Firefox driver
    try:
        if platform.system() == 'Windows':
            logging.info("Initializing the driver")
            firefox_service = FirefoxService(executable_path=driver_path)
            driver = webdriver.Firefox(service=firefox_service, options=options)
        else:
            logging.info("Initializing the driver")
            driver = webdriver.Firefox(executable_path=driver_path, options=options)
    except Exception as e:
        logging.exception("An error has occurred in the initialization phase of the webdriver: %s", e)

    ########################################################

    # Main workflow #
    login(data["EMAIL"], data["PASSWORD"])
    download()