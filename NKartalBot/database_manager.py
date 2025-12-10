import sqlite3
import logging
import json
from datetime import datetime

# Loglama ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_name="bot_data.db"):
        self.db_name = db_name
        self.kurulum_yap()

    def baglan(self):
        """Veritabanı bağlantısı oluşturur."""
        try:
            # check_same_thread=False, Flask web sunucusu için zorunludur
            conn = sqlite3.connect(self.db_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # Verileri sözlük gibi çekmek için
            return conn
        except Exception as e:
            logging.error(f"Veritabanı bağlantı hatası: {e}")
            return None

    def kurulum_yap(self):
        """Gerekli tabloları oluşturur."""
        conn = self.baglan()
        if conn:
            cursor = conn.cursor()
            
            # 1. Analiz Geçmişi Tablosu
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS analizler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                konu TEXT,
                icerik TEXT,
                gorsel_yolu TEXT,
                platform TEXT DEFAULT 'Instagram',
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 2. İstatistik Tablosu (Dashboard için)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS istatistikler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                islem_turu TEXT,
                detay TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            conn.commit()
            conn.close()
            logging.info("✅ Veritabanı tabloları kontrol edildi.")

    def islem_kaydet(self, tur, detay=""):
        """Web panelde yapılan işlemi kaydeder."""
        self.veri_ekle("INSERT INTO istatistikler (islem_turu, detay) VALUES (?, ?)", (tur, detay))

    def pano_verilerini_getir(self):
        """Dashboard (Bento Grid) için sayıları hesaplar."""
        conn = self.baglan()
        veriler = {
            "toplam_gonderi": 0,
            "bu_hafta": 0,
            "son_gonderiler": []
        }
        
        if conn:
            try:
                cur = conn.cursor()
                # Toplam sayı
                veriler["toplam_gonderi"] = cur.execute("SELECT COUNT(*) FROM analizler").fetchone()[0]
                
                # Son 4 gönderi (Vitrin için)
                cur.execute("SELECT konu, tarih, gorsel_yolu FROM analizler ORDER BY id DESC LIMIT 4")
                rows = cur.fetchall()
                veriler["son_gonderiler"] = [dict(row) for row in rows]
                
            except Exception as e:
                logging.error(f"Pano verisi hatası: {e}")
            finally:
                conn.close()
        
        return veriler

    def veri_ekle(self, sorgu, parametreler=()):
        conn = self.baglan()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sorgu, parametreler)
                conn.commit()
                return True
            except Exception as e:
                logging.error(f"SQL Ekleme Hatası: {e}")
                return False
            finally:
                conn.close()
        return False
