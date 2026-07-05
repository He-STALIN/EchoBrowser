"""Главное окно браузера"""

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QKeySequence, QIcon, QPixmap

from src.ui.tab_manager import TabManager
from src.ui.navigation import NavigationBar
from src.ui.styles import get_stylesheet
from src.settings.settings_dialog import SettingsDialog, settings
from src.utils import get_home_page_url
import config

class MainWindow(QMainWindow):
    """Главное окно браузера"""
    
    def __init__(self):
        super().__init__()
        
        # Базовые параметры окна
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(f"{config.DATA_DIR}/icons/favicon.svg"))
        
        # Инициализация UI
        self.init_ui()
        self.apply_theme()
        self.FullScreenEN = False
        
        # Загрузить главную страницу
        self.load_home_page()
    
    def init_ui(self):
        """Инициализировать интерфейс"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Панель навигации
        self.navigation_bar = NavigationBar()
        self.navigation_bar.navigate_to_url.connect(self.navigate_to_url)
        self.navigation_bar.back_clicked.connect(self.go_back)
        self.navigation_bar.forward_clicked.connect(self.go_forward)
        self.navigation_bar.reload_clicked.connect(self.reload_page)
        self.navigation_bar.home_clicked.connect(self.load_home_page)
        self.navigation_bar.settings_clicked.connect(self.open_settings)
        self.navigation_bar.new_tab_clicked.connect(self.new_tab)
        layout.addWidget(self.navigation_bar)

        # Менеджер вкладок
        self.tab_manager = TabManager()
        self.tab_manager.tab_url_changed.connect(self._on_tab_url_changed)
        self.tab_manager.fullscreen_request.connect(self.on_fullscreen_requested)
        layout.addWidget(self.tab_manager)
        
        central_widget.setLayout(layout)
        
        # Меню
        #self.create_menu_bar()
    
    def create_menu_bar(self):
        """Создать меню браузера"""
        menubar = self.menuBar()
        
        # Меню файла
        file_menu = menubar.addMenu("Файл")
        
        new_tab_action = file_menu.addAction("Новая вкладка")
        new_tab_action.triggered.connect(lambda checked=False: self.new_tab())
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        
        # Меню редактирования
        edit_menu = menubar.addMenu("Правка")
        
        back_action = edit_menu.addAction("Назад")
        back_action.triggered.connect(self.go_back)
        back_action.setShortcut(QKeySequence.StandardKey.Back)
        
        forward_action = edit_menu.addAction("Вперед")
        forward_action.triggered.connect(self.go_forward)
        forward_action.setShortcut(QKeySequence.StandardKey.Forward)
        
        close_tab_action = edit_menu.addAction("Закрыть вкладку")
        close_tab_action.triggered.connect(self.close_current_tab)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        
        edit_menu.addSeparator()
        
        reload_action = edit_menu.addAction("Обновить")
        reload_action.triggered.connect(self.reload_page)
        reload_action.setShortcut(QKeySequence.StandardKey.Refresh)
        
        # Меню вида
        view_menu = menubar.addMenu("Вид")
        
        home_action = view_menu.addAction("Главная страница")
        home_action.triggered.connect(self.load_home_page)
        home_action.setShortcut(QKeySequence("Alt+Home"))
        
        view_menu.addSeparator()
        
        fullscreen_action = view_menu.addAction("Полноэкранный режим")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        fullscreen_action.setShortcut(QKeySequence.StandardKey.FullScreen)
        
        # Меню инструментов
        tools_menu = menubar.addMenu("Инструменты")
        
        settings_action = tools_menu.addAction("Настройки")
        settings_action.triggered.connect(self.open_settings)
        
        # Меню помощи
        help_menu = menubar.addMenu("Справка")
        
        about_action = help_menu.addAction("О браузере")
        about_action.triggered.connect(self.show_about)
    
    def setup_shortcuts(self):
        """Установить глобальные горячие клавиши"""
        # Горячие клавиши назначаются через QAction, чтобы избежать конфликтов.
        pass
    
    def apply_theme(self):
        """Применить тему к приложению"""
        theme = settings.get("theme", "light")
        stylesheet = get_stylesheet(theme)
        self.setStyleSheet(stylesheet)
    
    def new_tab(self, url: str = "about:blank"):
        """Создать новую вкладку"""
        self.tab_manager.new_tab(url)
    
    def close_current_tab(self):
        """Закрыть текущую вкладку"""
        index = self.tab_manager.currentIndex()
        self.tab_manager.close_tab(index)
    
    def navigate_to_url(self, url: str):
        """Перейти по URL"""
        current_tab = self.tab_manager.get_current_tab()
        if current_tab:
            current_tab.load_url(url)
    
    def go_back(self):
        """Перейти назад"""
        current_tab = self.tab_manager.get_current_tab()
        if current_tab:
            current_tab.back()
    
    def go_forward(self):
        """Перейти вперед"""
        current_tab = self.tab_manager.get_current_tab()
        if current_tab:
            current_tab.forward()
    
    def reload_page(self):
        """Обновить страницу"""
        current_tab = self.tab_manager.get_current_tab()
        if current_tab:
            current_tab.reload()
    
    def load_home_page(self):
        """Загрузить главную страницу"""
        home_url = get_home_page_url()
        self.navigate_to_url(home_url)
    
    def _on_tab_url_changed(self, url: str):
        """Обработка изменения URL в текущей вкладке"""
        self.navigation_bar.set_url(url)
    
    def open_settings(self):
        """Открыть диалог настроек"""
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec() == settings_dialog.accepted:
            self.apply_theme()
    
    def toggle_fullscreen(self):
        """Переключить полноэкранный режим"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def show_about(self):
        """Показать информацию о браузере"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "О браузере EchoBrowser",
            f"EchoBrowser v0.1.0\n\n"
            f"Современный браузер на PyQt6\n\n"
            f"© 2024 Echo Project\n"
            f"Все права защищены"
        )
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.tab_manager.close_all_tabs()
        event.accept()

    def on_fullscreen_requested(self):
        # Разрешаем полноэкранный режим
        # Переключаем окно в полноэкранный режим
        print(self.FullScreenEN)
        if self.FullScreenEN:
            print("trying to normal mode")
            self.showNormal()
            self.FullScreenEN = False
        else:
            print("Trying to fullscreen Mode")
            self.FullScreenEN = True
            self.showFullScreen()
