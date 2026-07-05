import requests
from bs4 import BeautifulSoup
#import config

"""def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/140.0.0.0 EchoBrowser/1.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    
    # Ищем блоки результатов по структуре
    for item in soup.select('div[data-hveid]'):
        title_tag = item.select_one('h3')
        if not title_tag:
            continue
        
        link_tag = item.select_one('a')
        if not link_tag:
            continue
        
        # Извлекаем ссылку
        link = link_tag.get('href', '')
        if link.startswith('/url?q='):
            link = link.split('/url?q=')[1].split('&')[0]
        elif link.startswith('http'):
            pass
        else:
            continue
        
        # Описание
        desc_tag = item.select_one('div[data-sncf]') or item.select_one('div[style*="line-height"]')
        desc = desc_tag.text.strip() if desc_tag else ''
        
        results.append({
            'title': title_tag.text.strip(),
            'link': link,
            'desc': desc
        })
        print(results)
        
        if len(results) >= 10:
            break
    
    return results"""

def search_google(query):
    session = requests.Session()
    
    # Заголовки как у реального браузера
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/140.0.0.0 EchoBrowser/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
    })
    
    # Делаем первый запрос, чтобы получить куки
    session.get("https://www.google.com/")
    
    # Теперь ищем
    url = f"https://www.google.com/search?q={query}"
    response = session.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    for h3 in soup.find_all('h3'):
        parent = h3.find_parent('a')
        if not parent:
            continue
        link = parent.get('href', '')
        if link.startswith('/url?q='):
            link = link.split('/url?q=')[1].split('&')[0]
        elif not link.startswith('http'):
            continue
        desc_tag = h3.find_next('div')
        desc = desc_tag.text.strip() if desc_tag else ''
        results.append({
            'title': h3.text.strip(),
            'link': link,
            'desc': desc
        })
        if len(results) >= 10:
            break
    
    return results