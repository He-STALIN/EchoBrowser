"""Менеджер вкладок браузера"""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PyQt6.QtCore import pyqtSignal, QUrl, Qt
from PyQt6.QtWidgets import QMainWindow
import sys

from src.utils import format_url, get_home_page_url
import config

def _setup_params(self):
    self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
    self.setAutoFillBackground(True)

    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, config.USE_GPU_RENDER
    )
    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, config.FULLSCREEN_SUPPORT_EN
    )

    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.LocalStorageEnabled, config.LOCAL_STORAGE_EN
    )

class BrowserTab(QWebEngineView):
    """Отдельная вкладка браузера"""
    
    title_changed = pyqtSignal(str)
    url_changed = pyqtSignal(str)
    FS_request = pyqtSignal()
    
    def __init__(self, url: str = "about:blank"):
        super().__init__()
        
        # Подключить сигналы
        self.titleChanged.connect(self._on_title_changed)
        self.urlChanged.connect(self._on_url_changed)

        _setup_params(self) #? Выносим параменты в отдельную функцию, чтобы избежать путаницы в писанине кода

        QWebEngineProfile.defaultProfile().setHttpUserAgent(config.CUSTOM_UA)
        self.page().fullScreenRequested.connect(self.FS_request.emit)
        
        # Загрузить страницу
        if url != "about:blank":
            self.setUrl(QUrl(format_url(url)))
        else:
            self.setUrl(QUrl(get_home_page_url()))
    
    def _on_title_changed(self, title: str):
        """Обработка изменения заголовка"""
        self.title_changed.emit(title if title else "Новая вкладка")
    
    def _on_url_changed(self, url: QUrl):
        """Обработка изменения URL"""
        self.url_changed.emit(url.toString())
    
    def load_url(self, url: str):
        """Загрузить URL"""
        formatted_url = format_url(url)
        self.setUrl(QUrl(formatted_url))


class TabManager(QTabWidget):
    """Менеджер вкладок браузера"""
    
    tab_url_changed = pyqtSignal(str)  # URL текущей вкладки изменился
    fullscreen_request = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        
        # Подключить сигналы
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self._on_current_changed)
        
        # Создать первую вкладку
        self.new_tab()
    
    def new_tab(self, url: str = "about:blank") -> BrowserTab:
        """Создать новую вкладку"""
        tab = BrowserTab(url)
        
        # Подключить сигналы вкладки
        tab.title_changed.connect(lambda title: self._update_tab_title(tab, title))
        tab.url_changed.connect(self.tab_url_changed.emit)
        tab.FS_request.connect(self.fullscreen_request.emit)
        
        # Добавить в менеджер
        index = self.addTab(tab, "Загрузка...")
        self.setCurrentIndex(index)
        
        return tab
    
    def _update_tab_title(self, tab: BrowserTab, title: str):
        """Обновить название вкладки"""
        index = self.indexOf(tab)
        if index != -1:
            # Обрезать длинные названия
            short_title = title[:30] + "..." if len(title) > 30 else title
            self.setTabText(index, short_title)
    
    def _on_current_changed(self, index: int):
        """Обработка смены текущей вкладки"""
        if index != -1:
            tab = self.widget(index)
            if tab:
                self.tab_url_changed.emit(tab.url().toString())
    
    def close_tab(self, index: int):
        """Закрыть вкладку"""
        if self.count() == 1:
            # Если это последняя вкладка, создать новую
            # self.new_tab()
            sys.exit()
        self.removeTab(index)
    
    def get_current_tab(self) -> BrowserTab:
        """Получить текущую вкладку"""
        return self.currentWidget()
    
    def close_all_tabs(self):
        """Закрыть все вкладки"""
        while self.count() > 0:
            self.removeTab(0)