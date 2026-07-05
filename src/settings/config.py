"""Конфигурация и управление настройками"""

import json
from pathlib import Path
from typing import Any
import config as global_config
from src.utils import load_json_file, save_json_file


class Settings:
    """Управление настройками браузера"""
    
    # Стандартные настройки
    DEFAULT_SETTINGS = {
        "search_engine": "https://www.google.com/search?q=",
        "home_page": "home",
        "show_bookmarks_bar": True,
        "javascript_enabled": True,
        "plugins_enabled": True,
        "history_enabled": True,
        "theme": "light",
        "font_size": 100,
    }
    
    def __init__(self):
        self.config_file = global_config.CONFIG_FILE
        self.settings = self._load_settings()
    
    def _load_settings(self) -> dict:
        """Загрузить настройки из файла"""
        settings = load_json_file(self.config_file)
        
        # Заполнить отсутствующие параметры стандартными значениями
        for key, value in self.DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = value
        
        return settings
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получить значение настройки"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Установить значение настройки и сохранить"""
        self.settings[key] = value
        return self.save()
    
    def save(self) -> bool:
        """Сохранить настройки в файл"""
        return save_json_file(self.config_file, self.settings)
    
    def reset_to_defaults(self) -> bool:
        """Сбросить на стандартные значения"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        return self.save()


# Глобальный экземпляр
settings = Settings()
