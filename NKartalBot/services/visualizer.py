import os
import random
import textwrap
import logging
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

logger = logging.getLogger("NKartalArt")

class Visualizer:
    def __init__(self):
        self.font_path = os.getenv("FONT_NAME", "arial.ttf")
        # Font yoksa varsayılanı kullanmak için kontrol
        if not os.path.exists(self.font_path):
            self.font_path = "arial.ttf" # Sistemde varsa
        
    def _resim_indir(self, query):
        """Pexels API kullanarak HD fotoğraf indirir."""
        api_key = os.getenv("PEXELS_API_KEY")
        if not api_key:
            return None
            
        try:
            headers = {'Authorization': api_key}
            url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=square"
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            if data.get('photos'):
                img_url = data['photos'][0]['src']['large2x']
                resim_data = requests.get(img_url).content
                with open("temp_bg.jpg", "wb") as f:
                    f.write(resim_data)
                return "temp_bg.jpg"
        except Exception as e:
            logger.error(f"Pexels Hatası: {e}")
        return None

    def _mixed_media_efekti(self, img):
        """Görsele 'Gürültü' ve 'Cyberpunk' filtresi ekler."""
        # 1. Karartma (Overlay)
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 160)) # %60 Siyah
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # 2. Noise (Karıncalanma) Efekti - Premium hissi verir
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b = pixels[i, j]
                noise = random.randint(-20, 20)
                pixels[i, j] = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
        return img

    def kart_olustur(self, baslik, metin, konu):
        """Metni ve görseli birleştirir."""
        width, height = 1080, 1080
        
        # 1. Arka Planı Bul
        bg_file = self._resim_indir(konu)
        if bg_file:
            img = Image.open(bg_file).resize((width, height))
        else:
            # Resim bulunamazsa Cyberpunk Grisi
            img = Image.new('RGB', (width, height), color=(20, 25, 30))
            
        # 2. Efektleri Uygula
        img = self._mixed_media_efekti(img)
        draw = ImageDraw.Draw(img)

        # 3. Fontları Yükle
        try:
            baslik_font = ImageFont.truetype(self.font_path, 80)
            metin_font = ImageFont.truetype(self.font_path, 45)
            footer_font = ImageFont.truetype(self.font_path, 30)
        except:
            # Font dosyası yoksa varsayılan
            baslik_font = ImageFont.load_default()
            metin_font = ImageFont.load_default()
            footer_font = ImageFont.load_default()

        # 4. Çerçeve Çiz (Neon Cyan)
        draw.rectangle([40, 40, width-40, height-40], outline="#06b6d4", width=5)

        # 5. Başlığı Yaz (Ortala)
        # (Basit ortalama mantığı)
        draw.text((80, 150), baslik.upper(), font=baslik_font, fill="#06b6d4") # Neon Mavi

        # 6. Metni Yaz (Satır Satır)
        lines = textwrap.wrap(metin, width=40)
        y = 300
        for line in lines:
            draw.text((80, y), line, font=metin_font, fill="white")
            y += 60
            if y > 900: break # Taşarsa dur

        # 7. Alt Bilgi (Logo niyetine)
        draw.text((80, 980), "🦅 NKartal AI Analysis", font=footer_font, fill="#aaaaaa")

        # 8. Kaydet
        cikti_yolu = f"static/post_{random.randint(1000,9999)}.jpg"
        img.save(cikti_yolu)
        return cikti_yolu
