import logging
import colorlog
from logging.handlers import RotatingFileHandler
import config
import os

def get_logger(name):
    """Возвращает настроенный логгер для модуля"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # чтобы не дублировать
        logger.setLevel(logging.INFO)
        
        console = colorlog.StreamHandler()
        console.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] %(levelname)s - %(name)s IN %(filename)s:%(lineno)d -> %(message)s',
            datefmt='%d-%m-%Y | %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        ))

        #? Формат лога (как оон будет выглядеть?)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(name)s IN %(filename)s:%(lineno)d -> %(message)s',
            datefmt='%d-%m-%Y | %H:%M:%S'
        )
        
        logger.addHandler(console)
        
        # Файл
        os.makedirs('logs', exist_ok=True)
        file_handler = RotatingFileHandler(
            config.LOG_FILE, maxBytes=3*1024*1024, backupCount=3, encoding='utf-8' #? параметры ротации: файл, куда записывать, макс. размер (3МБ), кол-во бэкапов и кодировка файла
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

default_logger = get_logger('EchoBrowser')