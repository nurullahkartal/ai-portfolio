# services/scraper.py (ULTIMATE EDITION - GEMINI 2.0 FLASH)

import wikipedia
import re
from utils.logger import setup_logger
from services.database_manager import DatabaseManager
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Env yükle
load_dotenv('gizli.env')

logger = setup_logger()

class DataScraper:
    def __init__(self):
        self.db = DatabaseManager()
        wikipedia.set_lang("tr")
        
        # AI Ayarları
        self.ai_aktif = False
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            try:
                genai.configure(api_key=api_key)
                # GÜNCEL MODEL: Gemini 2.0 Flash (En Hızlısı)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.ai_aktif = True
                logger.info("🧠 Yapay Zeka (Gemini 2.0 Flash) Modülü Aktif!")
            except Exception as e:
                 logger.error(f"⚠️ AI Modeli Başlatma Hatası: {e}")
        else:
            logger.warning("⚠️ Gemini API anahtarı bulunamadı. AI devre dışı.")

    def yapay_zeka_ozetle(self, konu, ham_metin):
        """Metni AI ile Instagram formatına çevirir."""
        if not self.ai_aktif:
            return ham_metin[:400] 

        try:
            logger.info(f"🤖 AI, '{konu}' için metni yeniden yazıyor...")
            # GÜNCEL PROMPT: Kısa, öz ve Instagram formatına uygun
            prompt = (
                f"Aşağıdaki metni bir Instagram görseli (infografik) için hazırla.\n"
                f"Konu: {konu}\n"
                f"Kurallar:\n"
                f"1. MAKSİMUM 3 CÜMLE kullan. Çok kısa ve vurucu olsun.\n"
                f"2. Metin asla 350 karakteri geçmesin. (Görsele sığması şart).\n"
                f"3. Emoji kullanma (Görselin ciddiyetini bozmasın, onları caption'a koyarız).\n"
                f"4. Madde işareti kullanma, düz paragraf olsun.\n\n"
                f"Metin: {ham_metin[:2000]}"
            )
            
            # Hata almamak için güvenlik filtrelerini kapatıyoruz
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            response = self.model.generate_content(prompt, safety_settings=safety_settings)
            return response.text
        except Exception as e:
            logger.error(f"AI Hatası: {e}")
            return ham_metin[:400]

    def veri_analiz_et(self, konu):
        """Veriyi çeker, veritabanına bakar, AI ile işler."""
        logger.info(f"'{konu}' için veri hazırlığı başlatıldı.")
        
        # 1. Veritabanı Kontrolü
        kayit = self.db.veri_getir(konu)
        if kayit:
            logger.info(f"Veri veritabanında bulundu. (ID: {kayit[0]})")
            return {
                "konu": kayit[1],
                "veri": kayit[2],
                "ham_veri": kayit[3],
                "tarih": kayit[4],
                "baslik": kayit[1]
            }

        # 2. Wikipedia ve AI
        logger.warning("Veri veritabanında bulunamadı. Wikipedia ve AI devreye giriyor...")
        try:
            search_results = wikipedia.search(konu)
            if not search_results:
                return None
            
            page = wikipedia.page(search_results[0])
            ham_icerik = page.content
            
            # AI ile İçerik Üret
            ai_metin = self.yapay_zeka_ozetle(konu, ham_icerik)
            kisa_ozet = wikipedia.summary(konu, sentences=2)
            
            veri_paketi = {
                "konu": konu,
                "veri": ai_metin,
                "ham_veri": kisa_ozet,
                "tarih": "2025-12-10",
                "baslik": page.title
            }
            
            # Veritabanına Kaydet
            self.db.veri_ekle(konu, ai_metin, kisa_ozet)
            logger.success(f"'{konu}' AI ile işlendi ve kaydedildi.")
            
            return veri_paketi

        except Exception as e:
            logger.error(f"Scraper hatası: {e}")
            return None