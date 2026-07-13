from pathlib import Path
import config

def get_home_page_url() -> str:
    """Получить URL главной страницы"""
    home_file = Path(config.RESOURCES_DIR) / "home.html"
        
    home_file = str(home_file).replace('\\', '/')

    return f"file:///{home_file}"


def get_about_page_url() -> str:
    """Получить URL страницы 'О нас'"""
    about_file = Path(config.RESOURCES_DIR) / "about.html"

    about_file = str(about_file).replace('\\', '/')

    return f"file:///{about_file}"