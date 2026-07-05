"""
EchoBrowser - Современный браузер на PyQt6

Главная точка входа в приложение
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Основная функция приложения"""
    
    # Создать приложение
    app = QApplication(sys.argv)

    # Создать главное окно
    window = MainWindow()
    window.show()
    
    # Запустить главный цикл
    sys.exit(app.exec())


if __name__ == "__main__":
    main()