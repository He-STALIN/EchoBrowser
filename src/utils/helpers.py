"""Вспомогательные функции для EchoBrowser"""

from urllib.parse import urljoin, urlparse
import json
from pathlib import Path


def is_valid_url(url: str) -> bool:
    """Проверить, является ли строка валидным URL (кроме file://)"""
    try:
        result = urlparse(url)
        # Игнорируем file://, считаем его локальным путём
        if result.scheme == 'file':
            return False
        return all([result.scheme, result.netloc])
    except:
        return False

def format_url(url: str) -> str:
    """Форматировать URL для отправки в браузер"""
    url = url.strip()
    
    if not url:
        return ""
    
    # Проверяем, не локальный ли это файл
    if url.startswith('file://'):
        return url  # оставляем как есть
    
    # Если это обычный URL
    if is_valid_url(url):
        return url
    
    # Если выглядит как домен
    if "." in url and " " not in url:
        return f"https://{url}"
    
    # Иначе поиск в Google
    return f"https://www.google.com/search?q={url}"


def load_json_file(file_path: Path) -> dict:
    """Загрузить JSON файл"""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
    return {}


def save_json_file(file_path: Path, data: dict) -> bool:
    """Сохранить JSON файл"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False
