"""Стили и UI компоненты"""
from PyQt6.QtCore import QFile
import config

# CSS стили для приложения

def get_stylesheet(theme: str = "light") -> str:
    """Получить стиль для темы"""
    file = QFile(f"{config.STYLES_DIR}/{theme}.qss")
    file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    style = file.readAll().data().decode()
    file.close()
    return style
