# Архитектура EchoBrowser

## Архитектурный паттерн

EchoBrowser использует **модульную архитектуру** с четким разделением ответственности. Каждый модуль отвечает за одну область функциональности и может быть независимо расширен или переписан.

```
┌─────────────────────────────────────────────────┐
│              main.py (Точка входа)              │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│          MainWindow (src/main_window.py)        │
│  - Главное окно браузера                        │
│  - Менеджер главного цикла                      │
│  - Обработка горячих клавиш                     │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼─────────────────────────┐
        ▼            ▼                         ▼
    ┌────────────┐   ┌──────────────────┐  ┌─────────────┐
    │ TabManager │   │  NavigationBar   │  │   Menus     │
    │ (вкладки)  │   │(панель навигации)│  │   (меню)    │
    └────┬───────┘   └──────────────────┘  └─────────────┘
         │
    ┌────▼────────────────┐
    │   BrowserTab        │
    │ (отдельная вкладка) │
    │ QWebEngineView      │
    └─────────────────────┘
```

## Слои приложения

### 1. **Presentation Layer (UI)**
Отвечает за отображение интерфейса:
- `main_window.py` - главное окно
- `navigation.py` - адресная строка и кнопки
- `ui/styles.py` - стили приложения

### 2. **Business Logic Layer**
Содержит основную логику работы браузера:
- `tab_manager.py` - управление вкладками
- `home_page.py` - логика главной страницы

### 3. **Settings Layer**
Управление конфигурацией:
- `settings/config.py` - чтение/запись настроек
- `settings/settings_dialog.py` - UI для настроек

### 4. **Utility Layer**
Вспомогательные функции:
- `utils/helpers.py` - функции общего назначения

## Иерархия классов

```
QMainWindow (PyQt6)
    │
    └── MainWindow
            │
            ├── TabManager (QTabWidget)
            │   └── BrowserTab (QWebEngineView) [многократно]
            │
            └── NavigationBar (QWidget)
                    ├── QLineEdit (адресная строка)
                    └── QPushButton[] (кнопки)

QDialog (PyQt6)
    │
    └── SettingsDialog
            ├── QTabWidget
            │   ├── GeneralTab
            │   ├── PrivacyTab
            │   └── AppearanceTab
            └── QPushButton[] (кнопки)
```

## Модульность и расширяемость

### Добавление новой функции

**Пример: История браузера**

1. Создать новый модуль `src/history/`
```
src/history/
├── __init__.py
├── history_manager.py    # Логика истории
└── history_ui.py         # UI элементы
```

2. Интегрировать в main_window.py
```python
from src.history import HistoryManager

class MainWindow(QMainWindow):
    def init_ui(self):
        self.history = HistoryManager()
        # ...
        current_tab.urlChanged.connect(self.history.add_entry)
```

### Добавление нового типа вкладки

Можно расширить `BrowserTab` для специальных типов вкладок:
```python
class DownloadsTab(BrowserTab):
    """Вкладка для управления загрузками"""
    def __init__(self):
        super().__init__("about:blank")
        # Специальная логика для загрузок
```

## Поток данных

### Навигация по URL

```
NavigationBar (ввод URL)
    │
    ├─► navigate_to_url signal
    │
    ▼
MainWindow.navigate_to_url()
    │
    ├─► BrowserTab.load_url()
    │
    ▼
QWebEngineView.setUrl()
    │
    ├─► urlChanged signal
    │
    ▼
TabManager._on_url_changed()
    │
    ├─► tab_url_changed signal
    │
    ▼
NavigationBar.set_url() (обновление адресной строки)
```

### Управление настройками

```
SettingsDialog
    │
    ├─► Пользователь меняет параметр
    │
    ▼
save_and_close()
    │
    ├─► settings.set(key, value)
    │
    ▼
Settings.save()
    │
    ├─► JSON файл сохраняется
    │
    ▼
MainWindow.apply_theme() (если нужно)
```

## Сигналы и слоты (Qt сигналы)

### Основные сигналы:

| Источник | Сигнал | Получатель | Действие |
|----------|--------|-----------|---------|
| NavigationBar | navigate_to_url | MainWindow | Загрузить URL |
| TabManager | tab_url_changed | NavigationBar | Обновить адресную строку |
| BrowserTab | titleChanged | TabManager | Обновить название вкладки |
| BrowserTab | urlChanged | MainWindow | Обновить статус-бар |
| NavigationBar | back_clicked | MainWindow | Перейти назад |
| NavigationBar | forward_clicked | MainWindow | Перейти вперед |

## Конфигурация и состояние

### Где хранится состояние:

- **Настройки пользователя**: `~/.EchoBrowser/settings.json`
- **Временные данные**: Память приложения (при закрытии теряются)

### Как добавить новое состояние:

```python
# 1. Добавить в Settings.DEFAULT_SETTINGS
DEFAULT_SETTINGS = {
    "my_setting": default_value,
}

# 2. Читать значение
value = settings.get("my_setting")

# 3. Сохранять значение
settings.set("my_setting", new_value)
```

## Безопасность и изоляция

- Каждая вкладка - отдельный `QWebEngineView` (изоляция контекста)
- Настройки хранятся локально в JSON
- Можно добавить валидацию входных данных в `utils/helpers.py`

## Производительность

### Оптимизация:

1. **Ленивая загрузка**: Вкладки создаются по требованию
2. **Кэширование**: Qt автоматически кэширует веб-контент
3. **Асинхронная загрузка**: PyQtWebEngine загружает страницы в отдельном потоке

### Возможные улучшения:

- Реализовать пул потоков для тяжелых операций
- Добавить механизм кэширования истории
- Оптимизировать загрузку стилей

## Тестирование

### Рекомендуемая структура тестов:

```
tests/
├── test_navigation.py       # Тесты навигации
├── test_tab_manager.py      # Тесты менеджера вкладок
├── test_settings.py         # Тесты настроек
└── test_helpers.py          # Тесты утилит
```

### Пример теста:

```python
import unittest
from src.utils import format_url

class TestFormatUrl(unittest.TestCase):
    def test_valid_url(self):
        self.assertEqual(
            format_url("https://example.com"),
            "https://example.com"
        )
    
    def test_domain_only(self):
        self.assertEqual(
            format_url("example.com"),
            "https://example.com"
        )
    
    def test_search_query(self):
        self.assertTrue(
            format_url("hello world").startswith("https://www.google.com/search")
        )
```

## Зависимости и управление версиями

### Ключевые зависимости:

```
PyQt6 >= 6.0.0
  └─ Основной фреймворк UI
     └─ Совместим с Python 3.7+

PyQtWebEngine >= 6.0.0
  └─ Встроенный браузер Chromium
     └─ Зависит от PyQt6
```

### Как обновить зависимости:

```bash
# Обновить все пакеты
pip install --upgrade -r requirements.txt

# Обновить конкретный пакет
pip install --upgrade PyQt6
```

## Будущие расширения

### Рекомендуемые модули для добавления:

1. **Закладки** (`src/bookmarks/`)
   - Сохранение и загрузка закладок
   - UI панель закладок

2. **История** (`src/history/`)
   - Логирование посещений
   - Поиск в истории

3. **Расширения** (`src/extensions/`)
   - API для расширений
   - Система плагинов

4. **Синхронизация** (`src/sync/`)
   - Синхронизация с облаком
   - Резервное копирование данных

## Заключение

EchoBrowser спроектирован как масштабируемый браузер, готовый к расширению. Модульная архитектура позволяет легко добавлять новые функции без изменения существующего кода, следуя принципу Open/Closed Principle (открыт для расширения, закрыт для модификации).
