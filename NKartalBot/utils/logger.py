# utils/logger.py

import logging
import colorama
from colorama import Fore, Style, init

# Colorama'yı başlat
init(autoreset=True)

def setup_logger(debug_mode=False):
    """
    Bot için merkezi loglama sistemini ayarlar. 
    Debug modu aktifse seviye DEBUG olur.
    """
    
    logger = logging.getLogger('NKartalBot')
    # Seviyeyi DEBUG/INFO olarak dinamikleştir
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO) 
    
    if not logger.handlers:

        LOG_FORMAT = '%(asctime)s [%(levelname)s] - %(message)s'
        formatter = logging.Formatter(LOG_FORMAT)

        # Dosya Handler'ı
        file_handler = logging.FileHandler("bot.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Konsol Handler'ı (Renkli çıktı)
        class ColoredStreamHandler(logging.StreamHandler):
            def format(self, record):
                log_message = super().format(record)
                if record.levelname == 'ERROR':
                    return Fore.RED + Style.BRIGHT + log_message
                elif record.levelname == 'WARNING':
                    return Fore.YELLOW + log_message
                elif record.levelname == 'INFO':
                    return Fore.CYAN + log_message
                elif record.levelname == 'DEBUG': # DEBUG logları için yeni renk
                    return Fore.MAGENTA + log_message
                if 'SUCCESS' in record.levelname: 
                    return Fore.GREEN + log_message
                return log_message

        stream_handler = ColoredStreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        # Success seviyesi tanımı
        logging.addLevelName(25, 'SUCCESS')
        def success(self, message, *args, **kws):
            if self.isEnabledFor(25):
                self._log(25, message, args, **kws) 
        
        logging.Logger.success = success

    return logger