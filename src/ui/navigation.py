"""Панель навигации браузера"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal


class NavigationBar(QWidget):
    """Панель навигации с адресной строкой и кнопками"""
    
    navigate_to_url = pyqtSignal(str)  # Пользователь ввел URL
    back_clicked = pyqtSignal()
    forward_clicked = pyqtSignal()
    reload_clicked = pyqtSignal()
    home_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    new_tab_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Инициализировать интерфейс"""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Кнопка назад
        self.back_btn = QPushButton("←")
        self.back_btn.setMaximumWidth(40)
        self.back_btn.clicked.connect(self.back_clicked.emit)
        self.back_btn.setToolTip("Назад")
        layout.addWidget(self.back_btn)
        
        # Кнопка вперед
        self.forward_btn = QPushButton("→")
        self.forward_btn.setMaximumWidth(40)
        self.forward_btn.clicked.connect(self.forward_clicked.emit)
        self.forward_btn.setToolTip("Вперед")
        self.forward_btn.setVisible(False)
        layout.addWidget(self.forward_btn)
        
        # Кнопка обновления
        self.reload_btn = QPushButton("⟳")
        self.reload_btn.setMaximumWidth(40)
        self.reload_btn.clicked.connect(self.reload_clicked.emit)
        self.reload_btn.setToolTip("Обновить (F5)")
        layout.addWidget(self.reload_btn)
        
        # Кнопка домой
        self.home_btn = QPushButton("⌂")
        self.home_btn.setMaximumWidth(40)
        self.home_btn.setProperty('class', 'ToolBtn')
        self.home_btn.clicked.connect(self.home_clicked.emit)
        self.home_btn.setToolTip("Главная (Alt+Home)")
        layout.addWidget(self.home_btn)
        
        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите URL или поисковый запрос...")
        self.url_bar.setObjectName("URLArea")
        self.url_bar.returnPressed.connect(self._on_url_entered)
        layout.addWidget(self.url_bar)

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setMaximumWidth(40)
        self.settings_btn.setStyleSheet("font-size: 12px")
        self.settings_btn.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(self.settings_btn)

        self.new_tab_btn = QPushButton('+')
        self.new_tab_btn.setMaximumSize(40, 40)
        self.new_tab_btn.setStyleSheet("font-size: 15px")
        self.new_tab_btn.clicked.connect(self.new_tab_clicked.emit)
        layout.addWidget(self.new_tab_btn)
        
        self.setLayout(layout)
    
    def _on_url_entered(self):
        """Обработка ввода URL"""
        url = self.url_bar.text().strip()
        if url:
            self.navigate_to_url.emit(url)
    
    def set_url(self, url: str):
        """Установить URL в адресной строке"""
        self.url_bar.setText(url)
    
    def set_back_enabled(self, enabled: bool):
        """Включить/отключить кнопку назад"""
        self.back_btn.setEnabled(enabled)
    
    def set_forward_enabled(self, enabled: bool):
        """Включить/отключить кнопку вперед"""
        self.forward_btn.setEnabled(enabled)
