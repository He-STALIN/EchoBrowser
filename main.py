"""
EchoBrowser - Современный браузер на PyQt6

Главная точка входа в приложение
"""

import sys
import argparse
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import default_logger as logger


def main(url: str = None):
    """Основная функция приложения"""
    logger.info("Starting browser...")
    # Создать приложение
    app = QApplication(sys.argv)

    # Создать главное окно
    window = MainWindow()
    window.show()

    if url is not None:
        window.navigate_to_url(url)
    
    # Запустить главный цикл
    sys.exit(app.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser("EchoBrowser")
    parser.add_argument("-O", "--open", type=str, help="URL to open")

    args = parser.parse_args()

    if args.open:
        main(str(args.open))
    else:
        main()