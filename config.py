import os
from pathlib import Path

#* === PATHS ===
BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "logs" / "log.log"
DATA_DIR = BASE_DIR / "data"
COOKIES_DIR = DATA_DIR / "cookies"
STYLES_DIR = DATA_DIR / "styles"
RESOURCES_DIR = DATA_DIR / "resources"
CONFIG_FILE = BASE_DIR / "data" / "cfg" / "settings.json"
os.makedirs(COOKIES_DIR, exist_ok=True)

#* === UI ===
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
WINDOW_TITLE = "EchoBrowser"

#* === BROWSER ===
DEFAULT_HOME_PAGE = "home"  #? "home" или URL
DEFAULT_SEARCH_ENGINE = "https://www.google.com/search?q="
CUSTOM_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/140.0.0.0 EchoBrowser/1.0"

USE_GPU_RENDER = False
FULLSCREEN_SUPPORT_EN = True
LOCAL_STORAGE_EN = True

#* === EXTEND ===
DEBUG = True
