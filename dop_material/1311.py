from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# service = Service(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
# url = 'https://ya.ru'
# driver.get(url)
#
# time.sleep(3)
# driver.back()
#
# driver.refresh()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time



service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get('https://www.wikipedia.org')
url = driver.current_url

current_title = driver.title
print("Текущий заголовок страницы", current_title)

driver.quit()