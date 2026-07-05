from pathlib import Path
import config

def get_home_page_url() -> str:
    """Получить URL главной страницы"""
    home_file = Path(config.BASE_DIR) / "data" / "resources" / "home.html"
        
        
    home_file = str(home_file).replace('\\', '/')

    return f"file:///{home_file}"