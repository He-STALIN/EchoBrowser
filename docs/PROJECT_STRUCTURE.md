# Структура проекта EchoBrowser

Полное описание всех файлов и папок в проекте.

## Корневая папка

```
EchoBrowser
├── .editorconfig          # Настройки редактора
├── .gitignore             # Исключения git
├── .vscode                # Конфигурация VS Code
│   ├── extensions.json
│   └── settings.json
├── LICENSE                # MIT лицензия
├── config.py              # Главная конфигурация приложения
├── data                   # Ресурсы приложения
│   ├── cfg
│   ├── icons
│   │   └── favicon.svg
│   ├── resources
│   │   ├── home.html      # Главная страница
│   │   └── search.html    # Заготовка для своей страницы поиска
│   └── styles             # Стилизация приложения
│       ├── dark.qss
│       └── light.qss
├── docs                   # Документация
│   ├── ARCHITECTURE.md       # Описание архитектуры
│   ├── CHANGELOG.md          # История изменений
│   ├── CONTRIBUTING.md       # Как помочь проекту
│   ├── CONTRIBUTORS.md       # Список участников
│   ├── DEVELOPMENT.md        # Руководство разработчика
│   ├── PROJECT_STRUCTURE.md  # Этот файл
│   └── README.md             # Главная документация
├── main.py                   # Точка входа в приложение
├── requirements.txt
├── src                       # Код приложения
│   ├── settings
│   │   ├── config.py
│   │   └── settings_dialog.py
│   ├── ui
│   │   ├── main_window.py
│   │   ├── navigation.py
│   │   ├── styles.py
│   │   └── tab_manager.py
│   └── utils
│       ├── __init__.py
│       ├── helpers.py
│       ├── home_page.py
│       ├── logger.py
│       └── parser.py
└── tools                     # инструменты для разработки (планируются)
    └── requirements.in
```

## Подробное описание

### Корневые файлы

#### main.py
```python
"""Точка входа в приложение"""
```
- Инициализирует приложение PyQt6
- Создает главное окно
- Запускает главный цикл событий

#### dev_run.py
```python
"""Запуск в режиме разработки с дополнительными логами"""
```
- Включает режим отладки
- Выводит информацию о системе
- Используется для разработки и отладки

#### config.py
```python
"""Глобальная конфигурация браузера"""
```
- Параметры окна (размер, название)
- Пути к ресурсам
- Параметры браузера (поисковая система, user agent)
- Флаги отладки

#### requirements.txt
```
PyQt6>=6.0.0
PyQtWebEngine>=6.0.0
```
- Зависимости Python
- Версии пакетов

---

### Папка src/ - Исходный код

#### src/ui/main_window.py
Главное окно браузера (~400 строк)

**Классы:**
- `MainWindow` - главное окно (наследует QMainWindow)

**Основные методы:**
- `init_ui()` - инициализация интерфейса
- `create_menu_bar()` - создание меню
- `setup_shortcuts()` - установка горячих клавиш
- `navigate_to_url()` - навигация по URL
- `new_tab()` - создание новой вкладки
- `open_settings()` - открытие диалога настроек

**Сигналы:**
- Подключается к сигналам из `TabManager` и `NavigationBar`

#### src/ui/tab_manager.py
Управление вкладками (~200 строк)

**Классы:**
- `BrowserTab` - отдельная вкладка браузера (наследует QWebEngineView)
- `TabManager` - менеджер вкладок (наследует QTabWidget)

**BrowserTab методы:**
- `load_url()` - загрузить URL

**TabManager методы:**
- `new_tab()` - создать новую вкладку
- `close_tab()` - закрыть вкладку
- `get_current_tab()` - получить текущую вкладку
- `close_all_tabs()` - закрыть все вкладки

**Сигналы:**
- `tab_url_changed` - URL текущей вкладки изменился

#### src/ui/navigation.py
Панель навигации (~150 строк)

**Классы:**
- `NavigationBar` - панель навигации (наследует QWidget)

**Компоненты:**
- Кнопка "Назад" (←)
- Кнопка "Вперед" (→)
- Кнопка "Обновить" (⟳)
- Кнопка "Домой" (⌂)
- Адресная строка (QLineEdit)
- Кнопка "Перейти"

**Методы:**
- `set_url()` - установить URL в адресной строке
- `set_back_enabled()` - включить/отключить кнопку назад
- `set_forward_enabled()` - включить/отключить кнопку вперед

**Сигналы:**
- `navigate_to_url` - пользователь ввел URL
- `back_clicked` - нажата кнопка "Назад"
- `forward_clicked` - нажата кнопка "Вперед"
- `reload_clicked` - нажата кнопка "Обновить"
- `home_clicked` - нажата кнопка "Домой"

#### src/utils/home_page.py
Главная страница браузера (~100 строк)

**Функции:**
- `get_home_page_html()` - получить HTML главной страницы
- `save_home_page()` - сохранить HTML в файл
- `get_home_page_url()` - получить file:// URL главной страницы

**Содержание главной страницы:**
- Логотип браузера
- Поисковая строка
- Информация о браузере
- Карточки функций

---

### Папка src/settings/ - Модуль настроек

#### src/settings/__init__.py
```python
from .config import settings, Settings
from .settings_dialog import SettingsDialog

__all__ = ['settings', 'Settings', 'SettingsDialog']
```
- Экспортирует основные классы модуля

#### src/settings/config.py
Система управления настройками (~100 строк)

**Классы:**
- `Settings` - управление настройками браузера

**Стандартные настройки:**
```python
{
    "search_engine": "https://www.google.com/search?q=",
    "home_page": "home",
    "show_bookmarks_bar": True,
    "javascript_enabled": True,
    "plugins_enabled": True,
    "history_enabled": True,
    "theme": "light",
    "font_size": 100,
}
```

**Методы:**
- `get(key, default)` - получить значение
- `set(key, value)` - установить значение
- `save()` - сохранить в JSON файл
- `reset_to_defaults()` - сбросить на стандартные

**Глобальный экземпляр:**
```python
settings = Settings()  # Используется во всем приложении
```

#### src/settings/settings_dialog.py
Диалог настроек (~250 строк)

**Классы:**
- `SettingsDialog` - диалог настроек (наследует QDialog)

**Вкладки:**
1. **Основное** (General)
   - Выбор поисковой системы
   - Главная страница
   - Сохранение истории

2. **Приватность** (Privacy)
   - Включение JavaScript
   - Включение плагинов
   - Кнопка очистки кэша

3. **Внешний вид** (Appearance)
   - Выбор темы (светлая, темная, авто)
   - Размер шрифта (50-200%)
   - Показывать панель закладок

**Методы:**
- `load_settings()` - загрузить текущие значения
- `save_and_close()` - сохранить и закрыть
- `reset_to_defaults()` - сбросить на стандартные

---

### Папка src/ui/ - UI компоненты

**Переменные:**
- `MAIN_STYLESHEET` - светлая тема (CSS для Qt)
- `DARK_STYLESHEET` - темная тема (CSS для Qt)

**Функции:**
- `get_stylesheet(theme)` - получить стиль для темы

**Стилизованные элементы:**
- Главное окно (QMainWindow)
- Панель инструментов (QToolBar)
- Текстовые поля (QLineEdit)
- Кнопки (QPushButton)
- Вкладки (QTabBar, QTabWidget)
- Менеджер вкладок (QTabWidget)
- Строка состояния (QStatusBar)
- Меню (QMenuBar, QMenu)

---

### Папка src/utils/ - Вспомогательные функции

#### src/utils/__init__.py
```python
from .helpers import is_valid_url, format_url, load_json_file, save_json_file

__all__ = ['is_valid_url', 'format_url', 'load_json_file', 'save_json_file']
```

#### src/utils/helpers.py
Утилиты (~60 строк)

**Функции:**
- `is_valid_url(url)` - проверить валидность URL
- `format_url(url)` - отформатировать URL или запрос
- `load_json_file(path)` - загрузить JSON файл
- `save_json_file(path, data)` - сохранить JSON файл

---

### Папка data/ - Ресурсы

#### data/resources/
Папка для ресурсов приложения

- `home.html` - главная страница (создается автоматически)

---

### Папка .vscode/ - Конфигурация VS Code

#### .vscode/settings.json
Рекомендуемые параметры VS Code
- Включение linting (flake8)
- Форматирование (black)
- Линейки на 80 и 100 символов
- Исключение папок

#### .vscode/extensions.json
Рекомендуемые расширения
- Python
- Pylance
- Rainbow Indent
- GitLens
- GitHub Copilot
- Qt For Python

---

### Документация

#### README.md
Главная документация проекта
- Описание браузера
- Особенности
- Структура проекта
- Горячие клавиши
- Примеры использования
- Планы развития


#### ARCHITECTURE.md
Описание архитектуры проекта
- Слои приложения
- Иерархия классов
- Поток данных
- Qt сигналы
- Безопасность
- Производительность

#### DEVELOPMENT.md
Руководство разработчика
- Создание новых модулей
- Практические примеры
- Тестирование
- Лучшие практики
- Расширение функциональности

#### CONTRIBUTING.md
Как помочь проекту
- Кодекс поведения
- Процесс вклада
- Требования к коду
- Сообщение об ошибках
- Конвенция коммитов

#### CONTRIBUTORS.md
Список участников проекта
- Основатели
- Контрибьютеры
- Как добавиться в список

#### CHANGELOG.md
История изменений
- Версия 0.1.0 (текущая)
- Планы для будущих версий

#### LICENSE
MIT лицензия

#### PROJECT_STRUCTURE.md
Этот файл - полное описание структуры

---

### Конфигурационные файлы

#### .gitignore
Исключения для git
- Python кэш и compiled файлы
- Виртуальные окружения
- IDE файлы
- JSON конфигурация
- Логи

#### .editorconfig
Стиль кода для редакторов
- Кодировка UTF-8
- Длина строк
- Стиль отступов

---

## Таблица соответствия модулей и функций

| Модуль | Класс | Основная функция |
|--------|-------|------------------|
| main.py | - | Точка входа |
| config.py | - | Конфигурация |
| main_window.py | MainWindow | Главное окно |
| tab_manager.py | TabManager | Управление вкладками |
| tab_manager.py | BrowserTab | Отдельная вкладка |
| navigation.py | NavigationBar | Адресная строка |
| home_page.py | - | Главная страница |
| settings/config.py | Settings | Управление настройками |
| settings_dialog.py | SettingsDialog | Диалог настроек |
| styles.py | - | Стили приложения |
| helpers.py | - | Вспомогательные функции |

---

## Зависимости между модулями

```
main.py
  │
  ├─→ config.py (глобальная конфигурация)
  └─→ ui/main_window.py (главное окно)
      ├─→ .tab_manager.py (вкладки)
      │   └─→ .navigation.py (сигналы)
      ├─→ .navigation.py (адресная строка)
      ├─→ utils/home_page.py (главная страница)
      ├─→ settings/ (диалог настроек)
      │   └─→ settings/config.py (конфигурация)
      └─→ .styles.py (стили)
```

---

## Как навигировать по проекту

1. **Хочу добавить функцию** → `DEVELOPMENT.md`
2. **Хочу понять архитектуру** → `ARCHITECTURE.md`
3. **Хочу примеры кода** → `API_EXAMPLES.md`
4. **Хочу помочь проекту** → `CONTRIBUTING.md`
5. **Хочу установить браузер** → `INSTALL.md`

---

## Статистика проекта

| Метрика | Значение |
|---------|----------|
| Основных модулей | 8 |
| Классов | 8 |
| Строк кода | ~2000 |
| Документации | ~5000 строк |
| Файлов конфигурации | 3 |
| Тестов | 0 (планируется) |

---

**Последнее обновление**: 05-07-2026
