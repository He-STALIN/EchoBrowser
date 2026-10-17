"""Менеджер вкладок браузера"""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEngineFullScreenRequest, QWebEngineCookieStore
from PyQt6.QtNetwork import QNetworkCookie
from PyQt6.QtCore import pyqtSignal, QUrl, Qt
from PyQt6.QtGui import QIcon
import sys

from src.utils import format_url, get_home_page_url
from src.utils import default_logger as logger
from src.ui.contextMenu import ContextMenu
import config

def _setup_params(self: 'BrowserTab'):
    self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
    self.setAutoFillBackground(True)

    #? отрисовка через GPU
    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, config.USE_GPU_RENDER
    )

    #? Включаем возможность перехода в полноэкранный режим
    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, config.FULLSCREEN_SUPPORT_EN
    )

    #? разрешаем использование локального хранилища
    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.LocalStorageEnabled, config.LOCAL_STORAGE_EN
    )
    self.settings().setAttribute(
        QWebEngineSettings.WebAttribute.JavascriptEnabled, True
    )

    #? включаем сохранение куки
    QWebEngineProfile.defaultProfile().setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
    )

    QWebEngineProfile.defaultProfile().setPersistentStoragePath(
        str(config.COOKIES_DIR)
    )

    self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) #? указываем, чтобы использовал наше контекстное меню

    QWebEngineProfile.defaultProfile().setHttpUserAgent(config.CUSTOM_UA) #? устанавливаем кастомный UserAgent

    self.page().setDevToolsPage(self.page())

class BrowserTab(QWebEngineView):
    """Отдельная вкладка браузера"""
    
    title_changed = pyqtSignal(str)
    url_changed = pyqtSignal(str)
    FS_request = pyqtSignal(QWebEngineFullScreenRequest)
    LProgress = pyqtSignal(int)
    LStarted = pyqtSignal()
    LFinished = pyqtSignal()
    IChanged = pyqtSignal(QIcon)
    
    def __init__(self, url: str = "about:blank"):
        super().__init__()
        # Подключить сигналы
        self.titleChanged.connect(self._on_title_changed)
        self.urlChanged.connect(self._on_url_changed)
        self.loadProgress.connect(self.LProgress.emit)
        self.loadStarted.connect(self.LStarted.emit)
        self.loadFinished.connect(self.LFinished.emit)
        self.iconChanged.connect(self.IChanged.emit)
        self.page().fullScreenRequested.connect(self.FS_request.emit)

        self.contextmenu = ContextMenu(self)    #? Свое контекстное меню
        self.customContextMenuRequested.connect(self.contextmenu.show_at)

        self.cookies = CookieManager(self.page().profile().cookieStore())
        self.cookies.load_existing_cookies()

        _setup_params(self) #? Выносим параменты в отдельную функцию, чтобы избежать путаницы в писанине кода

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

    def _set_update_progress(self, progress: int):
        self.LProgress.emit(progress)


class CookieManager(QNetworkCookie):
    def __init__(self, cookie: QWebEngineCookieStore):
        super().__init__()
        self.cookie_store = cookie

    def add_cookie(self, name: str, value: str, domain: str, path: str, expires=None, secure: bool=False, http_only: bool=False):
        self.setName(name.encode())
        self.setValue(value.encode())
        self.setDomain(domain.encode())
        self.setPath(path.encode())
        if expires:
            self.setExpirationDate(expires.toPyDate())
        self.setHttpOnly(http_only)
        self.setSecure(secure)
        self.cookie_store.setCookie(self, QUrl(domain))

    def load_existing_cookies(self):
        self.cookie_store.loadAllCookies()
        # self.cookie_store.cookieAdded.connect(self.on_cookie_added)
        # self.cookie_store.cookieRemoved.connect(self.on_cookie_removed)

    def on_cookie_added(self, cookie):
        print(f"Кука добавлена: {cookie.name()} = {cookie.value()}")

    def on_cookie_removed(self, cookie):
        print(f"Кука удалена: {cookie.name()}")



class TabManager(QTabWidget):
    """Менеджер вкладок браузера"""
    
    tab_url_changed = pyqtSignal(str)  # URL текущей вкладки изменился
    fullscreen_request = pyqtSignal(QWebEngineFullScreenRequest)
    lProgress = pyqtSignal(int)
    lStarted = pyqtSignal()
    lFinished = pyqtSignal()
    state_update_require = pyqtSignal()
    state_update_recieve = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        
        # Подключить сигналы
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self._on_current_changed)
        self.state_update_require.connect(self._recive_update)
        
        # Создать первую вкладку
        self.new_tab()
    
    def new_tab(self, url: str = "about:blank") -> BrowserTab:
        """Создать новую вкладку"""
        logger.info("creating a new tab...")
        tab = BrowserTab(url)
        tab.page().history().canGoBack
        # Подключить сигналы вкладки
        tab.title_changed.connect(lambda title: self._update_tab_title(tab, title))
        tab.url_changed.connect(self.tab_url_changed.emit)
        tab.FS_request.connect(self.fullscreen_request.emit)
        tab.LProgress.connect(self.lProgress.emit)
        tab.LStarted.connect(self.lStarted.emit)
        tab.LFinished.connect(self._when_update_finished)
        tab.IChanged.connect(self._on_icon_changed)
        
        # Добавить в менеджер
        index = self.addTab(tab, "Загрузка...")
        self.setCurrentIndex(index)
        
        return tab

    def _recive_update(self):
        tab = self.get_current_tab()

        self.state_update_recieve.emit({
            "canBack": tab.history().canGoBack(),
            "canForward": tab.history().canGoForward()
        })

    def _when_update_finished(self):
        self._recive_update()
        self.lFinished.emit()

    def _update_tab_title(self, tab: BrowserTab, title: str):
        """Обновить название вкладки"""
        index = self.indexOf(tab)
        if index != -1:
            # Обрезать длинные названия
            short_title = title[:30] + "..." if len(title) > 30 else title
            self.setTabText(index, short_title)
    
    def _on_icon_changed(self, icon):
        index = self.currentIndex()
        self.setTabIcon(index, icon)

    def _on_current_changed(self, index: int):
        """Обработка смены текущей вкладки"""
        if index != -1:
            tab = self.widget(index)
            if tab:
                self.tab_url_changed.emit(tab.url().toString())
                self._recive_update()
    
    def close_tab(self, index: int):
        """Закрыть вкладку"""
        logger.info('closing a tab...')
        if self.count() == 1:
            #? Если это последняя вкладка, закрыть браузер полностью
            sys.exit()
        self.removeTab(index)
    
    def get_current_tab(self) -> BrowserTab:
        """Получить текущую вкладку"""
        return self.currentWidget()
    
    def close_all_tabs(self):
        """Закрыть все вкладки"""
        while self.count() > 0:
            self.removeTab(0)