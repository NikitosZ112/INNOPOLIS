# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# class Browser:
#     def __init__(self, start_url):
#         self.driver = webdriver.Chrome()
#         self.driver.get(start_url)
#
#     def find_element(self, by, value):
#         return self.driver.find_element(by, value)
#
#     def find_elements(self, by, value):
#         return self.driver.find_elements(by, value)
#
#     def click_element(self, by, value):
#         self.find_element(by, value).click()
#
#     def close(self):
#         self.driver.quit()
#
#
# class BookScraper:
#     def __init__(self, start_url):
#         self.browser = Browser(start_url)
#         self.books = []
#
#     def scrape_books_from_page(self):
#         book_elements = self.browser.find_elements(By.CSS_SELECTOR, 'article.product_pod')
#         for book in book_elements:
#             title = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('title')
#             price = book.find_element(By.CSS_SELECTOR, 'div.product_price p.price_color').text
#             rating = book.find_element(By.CSS_SELECTOR, 'p.star-rating').get_attribute('class').split()[-1]
#             self.books.append({'title': title, 'price': price, 'rating': rating})
#
#     def go_to_next_page(self):
#         try:
#             self.browser.click_element(By.CSS_SELECTOR, 'li.next a')
#             return True
#         except Exception:
#             return False
#
#     def scrape_all_pages(self):
#         while True:
#             self.scrape_books_from_page()
#             if not self.go_to_next_page():
#                 break
#     def save_to_csv(self, filename):
#         with open(filename, 'w', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=['title', 'price', 'rating'])
#             writer.writeheader()
#             writer.writerows(self.books)
#     def close_browser(self):
#         self.browser.close()
#
# if __name__ == '__main__':
#     start_url = 'http://books.toscrape.com/'
#     scraper = BookScraper(start_url)
#
#     try:
#         print("Начинаем парсинг сайта...")
#         scraper.scrape_all_pages()
#         scraper.save_to_csv('books.csv')
#         print("Парсинг завершён. Данные сохранены в файл 'books.csv'.")
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#     finally:
#         scraper.close_browser()
import time

# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/login")
#
# # Ввод логина и пароля
# driver.find_element(By.ID, "username").send_keys("tomsmith")
# driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
#
# # Нажатие кнопки "Login"
# driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
#
# # Проверка успешного входа
# success_message = driver.find_element(By.CSS_SELECTOR, ".flash.success").text
# assert "You logged into a secure area!" in success_message


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
#
# # Открываем браузер и переходим на страницу с выпадающим списком
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/dropdown")
#
# # Находим элемент выпадающего списка
# dropdown = Select(driver.find_element(By.ID, "dropdown"))
#
# # Выбираем элемент по его значению
# dropdown.select_by_value("2")  # Выбираем Option 2
#
# # Проверяем, что элемент действительно выбран
# selected_option = dropdown.first_selected_option.text
#
# time.sleep(3)
# print(selected_option == "Option 2")

# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# # Открываем браузер и переходим на страницу с чекбоксами
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/checkboxes")
#
# # Находим первый чекбокс
# checkbox1 = driver.find_element(By.XPATH, "//input[1]")
#
# # Если чекбокс не отмечен, отмечаем его
# if not checkbox1.is_selected():
#     checkbox1.click()
#
# # Проверяем, что чекбокс действительно отмечен
# print(checkbox1.is_selected())
# time.sleep(30)




# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.alert import Alert
#
# # Открываем браузер и переходим на страницу с alert-окнами
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/javascript_alerts")
#
# # Взаимодействие с простым alert
# driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
# time.sleep(5)
# alert = Alert(driver)
# alert.accept()  # Принимаем alert
#
#
# # Взаимодействие с confirm alert
# driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
# time.sleep(5)
# alert = Alert(driver)
# alert.dismiss()  # Отклоняем confirm
#
#
# # Взаимодействие с prompt alert
# driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
# time.sleep(5)
# alert = Alert(driver)
# alert.send_keys("Задница")  # Вводим текст
# alert.accept()  # Принимаем prompt
#
#
# # Проверка результата взаимодействия
# result = driver.find_element(By.ID, "result").text
# print(result)



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
#
# # Открываем браузер и переходим на страницу загрузки файлов
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/upload")
#
# # Находим элемент для выбора файла
# upload_element = driver.find_element(By.ID, "file-upload")
#
# # Отправляем путь к файлу для загрузки
# file_path = os.path.abspath("test.xml")  # Указываем путь к файлу
# upload_element.send_keys(file_path)
#
# # Нажимаем кнопку загрузки
# driver.find_element(By.ID, "file-submit").click()
#
# # Проверяем успешную загрузку
# uploaded_file_name = driver.find_element(By.ID, "uploaded-files").text
# print(uploaded_file_name)


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# # Открываем браузер и переходим на страницу с динамическими элементами
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/add_remove_elements/")
# time.sleep(2)
#
# # Добавляем элементы (кнопки "Delete")
# add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
# for _ in range(3):  # Добавим 3 кнопки
#     add_button.click()
# time.sleep(2)
#
# # Проверяем, что добавилось 3 кнопки
# delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
# assert len(delete_buttons) == 3
# time.sleep(2)
#
# # Удаляем один элемент
# delete_buttons[0].click()
# time.sleep(2)
#
# # Проверяем, что осталось 2 кнопки
# delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
# print(delete_buttons)
# time.sleep(2)

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# # Открываем браузер и переходим на страницу
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/windows")
# time.sleep(2)
#
# # Кликаем на ссылку для открытия новой вкладки
# driver.find_element(By.LINK_TEXT, "Click Here").click()
# time.sleep(2)
#
# # Переключаемся на новую вкладку
# time.sleep(1)  # Небольшая пауза для открытия новой вкладки
# new_window = driver.window_handles[1]  # Получаем идентификатор новой вкладки
# driver.switch_to.window(new_window)
# time.sleep(2)
#
# # Проверяем заголовок новой вкладки
# assert "New Window" in driver.title
# time.sleep(2)
#
# # Закрываем новую вкладку и возвращаемся на исходную
# driver.close()
# driver.switch_to.window(driver.window_handles[0])  # Переключаемся обратно на первую вкладку
# time.sleep(2)



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
#
# # Открываем браузер и переходим на страницу перетаскивания
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/drag_and_drop")
# time.sleep(2)
#
# # Находим элементы для перетаскивания
# element_to_drag = driver.find_element(By.ID, "column-a")  # Элемент A
# target_element = driver.find_element(By.ID, "column-b")    # Элемент B
# time.sleep(2)
#
# # Используем ActionChains для перетаскивания
# actions = ActionChains(driver)
# actions.drag_and_drop(element_to_drag, target_element).perform()  # Перетаскиваем элемент A на элемент B
# time.sleep(2)
#
# # Проверка результата
# assert target_element.text == "A"  # Проверяем, что элемент A теперь в позиции B


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# # Настройка неявного ожидания
# driver = webdriver.Chrome()
# driver.implicitly_wait(10)  # Устанавливаем неявное ожидание на 10 секунд
#
# # Открываем страницу
# driver.get("http://the-internet.herokuapp.com/dynamic_loading/1")
# # Находим и кликаем на кнопку "Start"
# start_button = driver.find_element(By.CSS_SELECTOR, "#start > button")
# start_button.click()
# # time.sleep(5)
# # Ждем появления текста "Hello World!" и проверяем его
# hello_world_text = driver.find_element(By.CSS_SELECTOR, "#finish > h4").text
# assert hello_world_text == "Hello World!"
#
# # Закрываем драйвер
# driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# # Открываем браузер и переходим на страницу
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/login")
#
# # Находим элемент (кнопка "Login")
# login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
#
# # Проверяем, активна ли кнопка "Login"
# is_enabled = login_button.is_enabled()
#
# # Проверка результата
# assert is_enabled is True, "Кнопка 'Login' должна быть активна."
#
# # Закрываем драйвер
# driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# # Открываем браузер и переходим на страницу
# driver = webdriver.Chrome()
# driver.get("http://the-internet.herokuapp.com/tables")
#
# # Сортируем по столбцу "Last Name"
# last_name_header = driver.find_element(By.XPATH, "//table[@id='table1']//th[1]")
# last_name_header.click()
#
# # Ждем, пока таблица обновится
# time.sleep(3)  # Можно заменить на явное ожидание
#
# # Проверяем порядок строк
# rows = driver.find_elements(By.XPATH, "//table[@id='table1']//tbody/tr")
# sorted_last_names = [row.find_element(By.XPATH, ".//td[1]").text for row in rows]
#
# # Ожидаемый порядок (в случае сортировки по возрастанию)
# expected_order = sorted(sorted_last_names)
# assert sorted_last_names == expected_order, "Строки не отсортированы по фамилиям."
# time.sleep(3)
#
# # Повторная сортировка (по убыванию)
# last_name_header.click()
# time.sleep(3)
#
# # Проверяем обратный порядок строк
# rows = driver.find_elements(By.XPATH, "//table[@id='table1']//tbody/tr")
# sorted_last_names_desc = [row.find_element(By.XPATH, ".//td[1]").text for row in rows]
# time.sleep(3)
#
# # Ожидаемый порядок по убыванию
# expected_order_desc = sorted(sorted_last_names, reverse=True)
# assert sorted_last_names_desc == expected_order_desc, "Строки не отсортированы по фамилиям в порядке убывания."
# time.sleep(3)
# # Закрываем драйвер
# driver.quit()

