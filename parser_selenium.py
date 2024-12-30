import re
import time
from utils import wait_element, parse_article_text_selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL = 'https://habr.com/ru/articles/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'искусственный интеллект', 'CAP']

def main():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--fullscreen')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    driver.get(URL)
    time.sleep(1)

    articles = driver.find_elements(by=By.TAG_NAME, value='article')
    data = []

    # парсинг статей
    for article in articles:
        title = wait_element(article, by=By.CLASS_NAME, value='tm-title__link')
        if title is None:
            continue
        title = title.text
        link = wait_element(article, by=By.CSS_SELECTOR, value='a.tm-title__link').get_attribute('href')
        content = wait_element(article, by=By.CSS_SELECTOR, value='div.tm-article-snippet__lead').text
        date = wait_element(article, by=By.TAG_NAME, value='time').get_attribute('title')
        data.append({
            'link': link,
            'title': title,
            'content': content,
            'date': date
        })

    # проверка включения ключевых слов
    for data_one_article in data:
        link = data_one_article['link']
        title = data_one_article['title']
        content = data_one_article['content']
        date = data_one_article['date']

        patterns = KEYWORDS
        contains_python = parse_article_text_selenium(driver, link, patterns)

        if not contains_python:
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    contains_python = True
                    break
            
        if contains_python:
            print(f'{date} - {title} - {link}')
        
    driver.close()

if __name__ == '__main__':
    main()
