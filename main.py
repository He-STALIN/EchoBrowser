"""
EchoBrowser - Современный браузер на PyQt6

Главная точка входа в приложение
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import default_logger as logger


def main():
    """Основная функция приложения"""
    logger.info("Starting browser...")
    # Создать приложение
    app = QApplication(sys.argv)

    # Создать главное окно
    window = MainWindow()
    window.show()
    
    # Запустить главный цикл
    sys.exit(app.exec())


if __name__ == "__main__":
    main()