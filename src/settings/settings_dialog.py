"""Диалог настроек браузера"""

from PyQt6.QtWidgets import(QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                            QWidget, QComboBox, QCheckBox, QSpinBox, QPushButton,
                            QGroupBox, QFormLayout, QSizePolicy)
from PyQt6.QtCore import Qt
from .config import settings


class SettingsDialog(QDialog):
    """Оверлейный диалог настроек (прозрачный фон, центральная карточка)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Сделать диалог без рамки и с прозрачным фоном (оверлей)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setWindowTitle("Настройки EchoBrowser")
        self.resize(1100, 700)
        self.setObjectName('SettingsDialog')

        self._build_ui()
        self.load_settings()

    def _build_ui(self):
        """Построить интерфейс с центральной карточкой на затемнённом фоне"""
        # Основной layout заполняет всё окно (оверлей)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Затемнённый фон (через стиль диалога) + центрируем карточку
        overlay_widget = QWidget(self)
        overlay_layout = QVBoxLayout(overlay_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(0)

        # Центрируем карточку по вертикали и горизонтали
        center_h = QHBoxLayout()
        center_h.addStretch()

        card = QWidget()
        card.setObjectName("settings_card")
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        # Вкладки
        tabs = QTabWidget()
        general_tab = self._create_general_tab()
        privacy_tab = self._create_privacy_tab()
        appearance_tab = self._create_appearance_tab()
        tabs.addTab(general_tab, "Основное")
        tabs.addTab(privacy_tab, "Приватность")
        tabs.addTab(appearance_tab, "Внешний вид")

        card_layout.addWidget(tabs)

        # Кнопки
        buttons_layout = QHBoxLayout()
        reset_btn = QPushButton("Сбросить на стандартные")
        reset_btn.clicked.connect(self.reset_to_defaults)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.save_and_close)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(reset_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)

        card_layout.addLayout(buttons_layout)

        center_h.addWidget(card)
        center_h.addStretch()

        overlay_layout.addStretch()
        overlay_layout.addLayout(center_h)
        overlay_layout.addStretch()

        main_layout.addWidget(overlay_widget)
    
    def _create_general_tab(self) -> QWidget:
        """Создать вкладку основных настроек"""
        widget = QWidget()
        layout = QFormLayout()
        
        # Поисковая система
        self.search_engine = QComboBox()
        self.search_engine.addItems([
            "Google",
            "Yandex",
            "Bing",
            "DuckDuckGo"
        ])
        layout.addRow("Поисковая система:", self.search_engine)
        
        # Главная страница
        self.home_page = QComboBox()
        self.home_page.addItems(["home", "about:blank"])
        layout.addRow("Главная страница:", self.home_page)
        
        # История
        self.history_enabled = QCheckBox("Сохранять историю")
        layout.addRow(self.history_enabled)
        
        widget.setLayout(layout)
        return widget
    
    def _create_privacy_tab(self) -> QWidget:
        """Создать вкладку приватности"""
        widget = QWidget()
        layout = QFormLayout()
        
        # JavaScript
        self.js_enabled = QCheckBox("Разрешить JavaScript")
        layout.addRow(self.js_enabled)
        
        # Плагины
        self.plugins_enabled = QCheckBox("Разрешить плагины")
        layout.addRow(self.plugins_enabled)
        
        group_box = QGroupBox("Кэширование")
        group_layout = QVBoxLayout()
        clear_cache_btn = QPushButton("Очистить кэш")
        # TODO: Реализовать очистку кэша
        group_layout.addWidget(clear_cache_btn)
        group_box.setLayout(group_layout)
        layout.addRow(group_box)
        
        widget.setLayout(layout)
        return widget
    
    def _create_appearance_tab(self) -> QWidget:
        """Создать вкладку внешнего вида"""
        widget = QWidget()
        layout = QFormLayout()
        
        # Тема
        self.theme = QComboBox()
        self.theme.addItems(["light", "dark", "auto"])
        layout.addRow("Тема:", self.theme)
        
        # Размер шрифта
        self.font_size = QSpinBox()
        self.font_size.setMinimum(50)
        self.font_size.setMaximum(200)
        self.font_size.setSuffix("%")
        layout.addRow("Размер шрифта:", self.font_size)
        
        # Показывать панель закладок
        self.bookmarks_bar = QCheckBox("Показывать панель закладок")
        layout.addRow(self.bookmarks_bar)
        
        widget.setLayout(layout)
        return widget
    
    def load_settings(self):
        """Загрузить текущие настройки в форму"""
        search_engines = {
            "https://www.google.com/search?q=": "Google",
            "https://yandex.ru/search?text=": "Yandex",
            "https://www.bing.com/search?q=": "Bing",
            "https://duckduckgo.com/?q=": "DuckDuckGo",
        }
        
        search_engine = settings.get("search_engine")
        if search_engine in search_engines:
            self.search_engine.setCurrentText(search_engines[search_engine])
        
        self.home_page.setCurrentText(settings.get("home_page", "home"))
        self.history_enabled.setChecked(settings.get("history_enabled", True))
        self.js_enabled.setChecked(settings.get("javascript_enabled", True))
        self.plugins_enabled.setChecked(settings.get("plugins_enabled", True))
        self.theme.setCurrentText(settings.get("theme", "light"))
        self.font_size.setValue(settings.get("font_size", 100))
        self.bookmarks_bar.setChecked(settings.get("show_bookmarks_bar", True))
    
    def save_and_close(self):
        """Сохранить настройки и закрыть диалог"""
        search_engines = {
            "Google": "https://www.google.com/search?q=",
            "Yandex": "https://yandex.ru/search?text=",
            "Bing": "https://www.bing.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
        }
        
        settings.set("search_engine", search_engines.get(self.search_engine.currentText()))
        settings.set("home_page", self.home_page.currentText())
        settings.set("history_enabled", self.history_enabled.isChecked())
        settings.set("javascript_enabled", self.js_enabled.isChecked())
        settings.set("plugins_enabled", self.plugins_enabled.isChecked())
        settings.set("theme", self.theme.currentText())
        settings.set("font_size", self.font_size.value())
        settings.set("show_bookmarks_bar", self.bookmarks_bar.isChecked())
        
        self.accept()
    
    def reset_to_defaults(self):
        """Сбросить на стандартные значения"""
        settings.reset_to_defaults()
        self.load_settings()
