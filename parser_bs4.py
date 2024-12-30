import re
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from utils import parse_article_text_bs4

URL = 'https://habr.com/ru/articles/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'искусственный интеллект', 'CAP']
HEADERS = Headers('chrome', 'lin').generate()

def main():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, features='lxml')

    articles = soup.find_all('article')

    for article in articles:
        title = article.find('a', attrs={'class': 'tm-title__link'}).\
            find('span').text
        content = article.find('div', attrs={'class': 'tm-article-snippet__lead'}).text  
        # content = article.find('div', attrs={'class': 'tm-article-body'}).text  
        date = article.find('time')['title']
        relative_link = article.find('a', attrs={'class': 'tm-title__link'})['href']
        link = 'https://habr.com' + relative_link

        patterns = KEYWORDS
        contains_python = parse_article_text_bs4(link, patterns, HEADERS)

        if not contains_python:
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    contains_python = True
                    break
            
        if contains_python:
            print(f'{date} - {title} - {link}')


if __name__ == '__main__':
    main()
