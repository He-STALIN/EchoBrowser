# Руководство расширения EchoBrowser

Этот файл содержит примеры и инструкции по расширению браузера с новыми функциями.

## Быстрый старт расширения

### Шаг 1: Создание нового модуля

```bash
# Создайте папку для вашего модуля
mkdir src/your_feature
touch src/your_feature/__init__.py
touch src/your_feature/main.py
```

### Шаг 2: Реализация функциональности

**src/your_feature/main.py:**
```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal

class YourFeature(QWidget):
    """Описание вашей функции"""
    
    # Сигналы (если нужны)
    feature_triggered = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Инициализировать UI"""
        layout = QVBoxLayout()
        label = QLabel("Ваша функция здесь")
        layout.addWidget(label)
        self.setLayout(layout)
    
    def do_something(self):
        """Выполнить действие"""
        self.feature_triggered.emit("action_completed")
```

**src/your_feature/__init__.py:**
```python
from .main import YourFeature

__all__ = ['YourFeature']
```

### Шаг 3: Интеграция в MainWindow

**src/main_window.py:**
```python
from src.your_feature import YourFeature

class MainWindow(QMainWindow):
    def init_ui(self):
        # ... существующий код ...
        
        # Добавить вашу функцию
        self.your_feature = YourFeature()
        # Подключить сигналы
        self.your_feature.feature_triggered.connect(self.on_feature_triggered)
    
    def on_feature_triggered(self, action):
        """Обработка событий из вашей функции"""
        self.statusBar.showMessage(f"Произошло: {action}")
```

## Практические примеры

### Пример 1: История браузера

**src/history/history_manager.py:**
```python
from pathlib import Path
from datetime import datetime
import json

class HistoryManager:
    """Управление историей браузера"""
    
    def __init__(self):
        self.history_file = Path.home() / ".echobrowser" / "history.json"
        self.history_file.parent.mkdir(exist_ok=True, parents=True)
        self.history = self._load_history()
    
    def _load_history(self):
        """Загрузить историю из файла"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def add_entry(self, url: str, title: str):
        """Добавить запись в историю"""
        entry = {
            "url": url,
            "title": title,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(entry)
        self._save_history()
    
    def _save_history(self):
        """Сохранить историю"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_recent(self, limit=10):
        """Получить последние записи"""
        return self.history[-limit:]
    
    def search(self, query: str):
        """Поиск в истории"""
        return [h for h in self.history if query.lower() in h['url'].lower()]
    
    def clear(self):
        """Очистить историю"""
        self.history = []
        self._save_history()
```

**Интеграция в main_window.py:**
```python
from src.history import HistoryManager

class MainWindow(QMainWindow):
    def init_ui(self):
        # ...
        self.history = HistoryManager()
        
        # Добавить пункт меню для истории
        history_menu = self.menuBar().addMenu("История")
        history_menu.addAction("Открыть историю").triggered.connect(self.show_history)
        history_menu.addSeparator()
        history_menu.addAction("Очистить историю").triggered.connect(self.history.clear)
        
        # Отслеживать посещения
        self.tab_manager.tab_url_changed.connect(lambda url: self.history.add_entry(url, ""))
```

### Пример 2: Закладки

**src/bookmarks/bookmarks_manager.py:**
```python
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout
from src.utils import save_json_file, load_json_file
from pathlib import Path

class BookmarkManager:
    """Управление закладками"""
    
    def __init__(self):
        self.bookmarks_file = Path.home() / ".echobrowser" / "bookmarks.json"
        self.bookmarks_file.parent.mkdir(exist_ok=True, parents=True)
        self.bookmarks = self._load_bookmarks()
    
    def _load_bookmarks(self):
        return load_json_file(self.bookmarks_file) or {}
    
    def add_bookmark(self, url: str, title: str):
        """Добавить закладку"""
        self.bookmarks[title] = url
        self._save_bookmarks()
    
    def remove_bookmark(self, title: str):
        """Удалить закладку"""
        if title in self.bookmarks:
            del self.bookmarks[title]
            self._save_bookmarks()
    
    def get_all(self):
        """Получить все закладки"""
        return self.bookmarks
    
    def _save_bookmarks(self):
        """Сохранить закладки"""
        save_json_file(self.bookmarks_file, self.bookmarks)


class BookmarksDialog(QDialog):
    """Диалог для управления закладками"""
    
    def __init__(self, bookmark_manager, parent=None):
        super().__init__(parent)
        self.bookmark_manager = bookmark_manager
        self.setWindowTitle("Закладки")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Список закладок
        self.bookmarks_list = QListWidget()
        self.refresh_bookmarks()
        layout.addWidget(self.bookmarks_list)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete_bookmark)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def refresh_bookmarks(self):
        """Обновить список закладок"""
        self.bookmarks_list.clear()
        for title, url in self.bookmark_manager.get_all().items():
            item = QListWidgetItem(f"{title} ({url})")
            item.setData(256, title)  # Сохранить ключ в item
            self.bookmarks_list.addItem(item)
    
    def delete_bookmark(self):
        """Удалить выбранную закладку"""
        item = self.bookmarks_list.currentItem()
        if item:
            title = item.data(256)
            self.bookmark_manager.remove_bookmark(title)
            self.refresh_bookmarks()
```

### Пример 3: Расширенная навигация

**Добавление кнопки закладки в NavigationBar:**
```python
class NavigationBar(QWidget):
    bookmark_page = pyqtSignal(str)  # Сигнал для добавления закладки
    
    def init_ui(self):
        # ... существующий код ...
        
        # Кнопка добавления закладки
        self.bookmark_btn = QPushButton("☆")
        self.bookmark_btn.setMaximumWidth(40)
        self.bookmark_btn.clicked.connect(self.bookmark_page.emit)
        self.bookmark_btn.setToolTip("Добавить закладку (Ctrl+D)")
        layout.addWidget(self.bookmark_btn)
```

## Добавление настроек для функции

### Пример: Настройка размера истории

**src/settings/settings_dialog.py:**
```python
class SettingsDialog(QDialog):
    def _create_general_tab(self):
        # ... существующий код ...
        
        # История
        history_size_label = QLabel("Размер истории (дней):")
        self.history_size = QSpinBox()
        self.history_size.setValue(settings.get("history_days", 30))
        layout.addRow(history_size_label, self.history_size)
        
        # В методе save_and_close()
        settings.set("history_days", self.history_size.value())
```

**Использование в коде:**
```python
from src.settings import settings

history_days = settings.get("history_days", 30)
```

## Тестирование вашего расширения

```python
# tests/test_my_feature.py
import unittest
from src.your_feature import YourFeature

class TestYourFeature(unittest.TestCase):
    def setUp(self):
        self.feature = YourFeature()
    
    def test_initialization(self):
        self.assertIsNotNone(self.feature)
    
    def test_do_something(self):
        # Ваши тесты
        pass

if __name__ == '__main__':
    unittest.main()
```

## Запуск тестов

```bash
python -m pytest tests/
```

## Лучшие практики расширения

1. **Разделение ответственности**: Каждый модуль должен делать одно и делать это хорошо
2. **Использование сигналов**: Для коммуникации между модулями используйте Qt сигналы
3. **Конфигурируемость**: Позвольте пользователям настраивать вашу функцию
4. **Документация**: Описывайте, что делает ваш модуль
5. **Тестирование**: Пишите тесты для вашего кода
6. **Версионирование**: Отслеживайте изменения в CHANGELOG.md

## Контрольный список перед публикацией

- [ ] Код протестирован
- [ ] Документация написана
- [ ] Нет конфликтов с существующим кодом
- [ ] Следует стилю проекта
- [ ] Использует существующие утилиты
- [ ] Не нарушает модульность архитектуры

## Помощь и поддержка

Если вам нужна помощь:
1. Прочитайте [ARCHITECTURE.md](ARCHITECTURE.md)
2. Посмотрите на существующие модули как на примеры
3. Проверьте [README.md](README.md) для общей информации

Удачи в расширении EchoBrowser! 🚀
