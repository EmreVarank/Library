import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(error_message):
    """Hata mesajını log dosyasına kaydeder"""
    logging.error(error_message)
