import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Browser:
    def __init__(self, start_url):
        self.driver = webdriver.Chrome()
        self.driver.get(start_url)
        time.sleep(10)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)

    def click_element(self, by, value):
        self.find_element(by, value).click()

    def close(self):
        self.driver.quit()


class BookScraper:
    def __init__(self, start_url):
        self.browser = Browser(start_url)
        self.books = []

    def scrape_books_from_page(self):
        book_elements = self.browser.find_elements(By.CSS_SELECTOR, 'article.product_pod')
        for book in book_elements:
            title = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('title')
            price = book.find_element(By.CSS_SELECTOR, 'div.product_price p.price_color').text
            rating = book.find_element(By.CSS_SELECTOR, 'p.star-rating').get_attribute('class').split()[-1]
            self.books.append({'title': title, 'price': price, 'rating': rating})

    def go_to_next_page(self):
        try:
            self.browser.click_element(By.CSS_SELECTOR, 'li.next a')
            return True
        except Exception:
            return False

    def scrape_all_pages(self):
        while True:
            self.scrape_books_from_page()
            if not self.go_to_next_page():
                break
    def save_to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'price', 'rating'])
            writer.writeheader()
            writer.writerows(self.books)
    def close_browser(self):
        self.browser.close()

if __name__ == '__main__':
    start_url = 'http://books.toscrape.com/'
    scraper = BookScraper(start_url)

    try:
        print("Начинаем парсинг сайта...")
        scraper.scrape_all_pages()
        scraper.save_to_csv('books.csv')
        print("Парсинг завершён. Данные сохранены в файл 'books.csv'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        scraper.close_browser()
