import pyodbc

_connection = None  # Bağlantıyı saklamak için global değişken

def create_connection():
    """Veritabanı bağlantısını oluşturur, zaten bağlıysa tekrar bağlanmaz."""
    global _connection
    if _connection is None or _connection.closed:  # Bağlantı yoksa veya kapanmışsa tekrar bağlan
        try:
            _connection = pyodbc.connect(
                "DRIVER={SQL Server};"
                "SERVER=DESKTOP-G2QDAFP;"
                "DATABASE=Lib;"
                "Trusted_Connection=yes;"
            )
        except Exception as e:
            print(f"Veri Tabanı Bağlantı hatası: {e}")
            return None
    return _connection
