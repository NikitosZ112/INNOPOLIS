from model import WikipediaH3Parser

if __name__ == "__main__":
    # URL страницы Википедии о Python
    WIKI_URL = "https://ru.wikipedia.org/wiki/Python"

    parser = WikipediaH3Parser(WIKI_URL)
    if parser.run():
        print("Парсинг успешно завершен!")
    else:
        print("Произошла ошибка при парсинге. Проверьте логи для деталей.")