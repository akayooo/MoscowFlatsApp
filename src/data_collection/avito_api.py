from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException
import os

# Укажите абсолютный путь к geckodriver
gecko_path = '/home/akayo/Рабочий стол/TechProg/src/data_collection/geckodriver'

# Проверка существования файла
if not os.path.isfile(gecko_path):
    raise FileNotFoundError(f"Файл geckodriver не найден по пути: {gecko_path}")

# Проверка прав доступа
if not os.access(gecko_path, os.X_OK):
    os.chmod(gecko_path, 0o755)

service = Service(executable_path=gecko_path)

try:
    driver = webdriver.Firefox(service=service)
    driver.get('https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA')
except WebDriverException as e:
    print(f"Ошибка при запуске веб-драйвера: {e}")
finally:
    driver.quit()