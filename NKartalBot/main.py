import os
import sys
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# --- MODÜLLERİ İÇERİ AL ---
try:
    from database_manager import DatabaseManager
    # Hata buradaydı, şimdi dosya yapısı doğruysa çalışacak
    from services.ai_manager import HybridBrain
    from services.visualizer import Visualizer
    from services.social_manager import SocialManager
except ImportError as e:
    print(f"KRİTİK HATA: Modüller bulunamadı! {e}")
    # Detaylı yol gösterelim
    print(f"Aranan yol: {os.getcwd()}/services")
    sys.exit(1)

# --- AYARLAR ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NKartalMain")

app = Flask(__name__)

# --- SİSTEMİ BAŞLAT ---
# Hata yönetimi ekleyelim ki hangisi bozuk anlayalım
try:
    db = DatabaseManager()
    ai = HybridBrain()
    viz = Visualizer()
    social = SocialManager()
except Exception as e:
    logger.error(f"Başlatma Hatası: {e}")
    sys.exit(1)

# Şifre Kontrolü İçin
SITE_SIFRESI = os.getenv("SITE_SIFRESI", "1")

# --- WEB ROTALARI ---

@app.route('/')
def ana_sayfa():
    """Dashboard Ana Sayfası"""
    try:
        stats = db.pano_verilerini_getir()
        profil_bilgisi = social.profil_verilerini_getir()
        embed_link = social.son_gonderi_embed()
        return render_template('index.html', stats=stats, profil=profil_bilgisi, son_embed_link=embed_link)
    except Exception as e:
        logger.error(f"Sayfa Yükleme Hatası: {e}")
        return "Sistem Yüklenirken Hata Oluştu. Logları kontrol edin."

@app.route('/api/analiz', methods=['POST'])
def analiz_api():
    """Botu Tetikleyen Fonksiyon"""
    veriler = request.json
    
    gelen_sifre = veriler.get('sifre')
    if str(gelen_sifre) != str(SITE_SIFRESI):
        return jsonify({"error": "🔐 Yetkisiz Erişim! Şifre yanlış."}), 403

    konu = veriler.get('konu')
    mod = veriler.get('mod', 'cyberpunk')

    if not konu:
        return jsonify({"error": "Konu boş olamaz."}), 400

    logger.info(f"🚀 Yeni Görev: '{konu}' (Mod: {mod})")

    try:
        # A. Yapay Zeka
        ai_sonuc = ai.icerik_uret(konu, mod=mod)
        metin = ai_sonuc["metin"]
        kaynak = ai_sonuc["kaynak"]
        
        # B. Görsel
        baslik = konu.upper()
        gorsel_yolu = viz.kart_olustur(baslik, metin, konu)
        
        # C. Instagram (Login varsa)
        social.gonderi_paylas(gorsel_yolu, metin)
        
        # D. Kayıt
        db.veri_ekle(
            "INSERT INTO analizler (konu, icerik, gorsel_yolu) VALUES (?, ?, ?)",
            (konu, metin, gorsel_yolu)
        )
        
        return jsonify({
            "status": "success",
            "ai_source": kaynak,
            "ai_text": metin
        }), 200

    except Exception as e:
        logger.error(f"İşlem Hatası: {e}")
        return jsonify({"error": f"Sistem Hatası: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print(f"🦅 NKartal Web AI Başlatılıyor... Port: {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)