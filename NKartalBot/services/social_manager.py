import os
import logging
from instagrapi import Client

logger = logging.getLogger("NKartalSocial")

class SocialManager:
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.session_file = os.getenv("INSTAGRAM_SESSION_FILE", "instagrapi_session.json")
        self.cl = Client()
        self.giris_yap()

    def giris_yap(self):
        """Instagram'a güvenli giriş yapar ve oturumu kaydeder."""
        if not self.username or not self.password:
            logger.warning("⚠️ Instagram bilgileri eksik. Modül 'Salt Okunur' modunda.")
            return

        try:
            if os.path.exists(self.session_file):
                self.cl.load_settings(self.session_file)
                logger.info("✅ Kayıtlı oturum yüklendi.")
            
            # Oturum geçerli mi diye basit bir kontrol (login gerekebilir)
            # self.cl.login(self.username, self.password) # İlk seferde açmak gerekebilir
            # logger.info("✅ Instagram Girişi Başarılı.")
        except Exception as e:
            logger.error(f"❌ Instagram Giriş Hatası: {e}")
            # Hata durumunda session dosyasını silip tekrar denemek gerekebilir
            
    def gonderi_paylas(self, resim_yolu, aciklama):
        """Fotoğrafı Instagram'a yükler."""
        try:
            if not os.path.exists(resim_yolu):
                return None
            
            media = self.cl.photo_upload(
                path=resim_yolu,
                caption=aciklama
            )
            # Yüklenen gönderinin kodunu döndür (örn: C4xyz...)
            return media.code 
        except Exception as e:
            logger.error(f"❌ Paylaşım Hatası: {e}")
            return None

    def profil_verilerini_getir(self):
        """Dashboard'daki sol kart için verileri çeker."""
        try:
            # Kendi profil bilgilerimizi çekelim (veya belirli bir kullanıcı)
            # Eğer login yapılmadıysa bu kısım hata verebilir, try-except önemli.
            user_id = self.cl.user_id_from_username(self.username)
            info = self.cl.user_info(user_id)
            
            return {
                "kullanici_adi": info.username,
                "takipci": info.follower_count,
                "gonderi_sayisi": info.media_count,
                "pp_url": str(info.profile_pic_url)
            }
        except Exception as e:
            logger.warning(f"Profil verisi çekilemedi (Login gerekebilir): {e}")
            return {
                "kullanici_adi": "nk_bot",
                "takipci": "---",
                "gonderi_sayisi": "---",
                "pp_url": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png" # Varsayılan robot resmi
            }

    def son_gonderi_embed(self):
        """Siteye gömmek için son gönderinin linkini verir."""
        try:
            user_id = self.cl.user_id_from_username(self.username)
            medias = self.cl.user_medias(user_id, amount=1)
            
            if medias:
                son_medya = medias[0]
                # Embed linki oluştur
                # Instagram embed formatı: instagram.com/p/{CODE}/embed
                return f"https://www.instagram.com/p/{son_medya.code}/embed"
            
        except Exception as e:
            logger.warning(f"Son gönderi çekilemedi: {e}")
        
        return None # Veri yoksa None döner
