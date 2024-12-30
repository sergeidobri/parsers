import re
import requests
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def wait_element(browser, delay=3, by=By.TAG_NAME, value=None):
    try: 
        return WebDriverWait(browser, delay).until(
            expected_conditions.presence_of_element_located((by, value))
        )
    except TimeoutException:
        return None
    
def parse_article_text_selenium(driver, url, keywords):
    driver.get(url)
    content_article = wait_element(driver, by=By.CSS_SELECTOR, value='div.tm-article-body').text
    contains_python = False
    
    for pattern in keywords:
        if re.search(pattern, content_article, re.IGNORECASE):
            contains_python = True
            break
    
    return contains_python

def parse_article_text_bs4(url, keywords, headers):
    response_article = requests.get(url, headers=headers)
    soup_article = BeautifulSoup(response_article.text, features='lxml')
    content_article = soup_article.find('div', attrs={'class': 'tm-article-body'}).text  
    contains_python = False
    
    for pattern in keywords:
        if re.search(pattern, content_article, re.IGNORECASE):
            contains_python = True
            break
    
    return contains_python
