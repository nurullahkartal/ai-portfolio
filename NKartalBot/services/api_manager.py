import os
import logging
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# Ayarları yükle
load_dotenv()
logger = logging.getLogger("NKartalAI")

class HybridBrain:
    def __init__(self):
        # 1. Motor: OpenAI (ChatGPT) - Öncelikli
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gpt_client = None
        if self.openai_key:
            self.gpt_client = OpenAI(api_key=self.openai_key)
            logger.info("🟢 OpenAI (ChatGPT) Motoru Hazır.")

        # 2. Motor: Google Gemini - Yedek (Failover)
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = None
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("🟢 Google Gemini Motoru Hazır (Yedek Güç).")

    def _chatgpt_ile_yaz(self, prompt):
        """ChatGPT kullanarak metin üretir."""
        if not self.gpt_client:
            raise Exception("OpenAI API Key eksik.")
        
        response = self.gpt_client.chat.completions.create(
            model="gpt-3.5-turbo", # Kredi dostu model
            messages=[
                {"role": "system", "content": "Sen dünyanın en iyi sosyal medya uzmanısın. Instagram için ilgi çekici, viral olacak captionlar yazarsın."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    def _gemini_ile_yaz(self, prompt):
        """Gemini kullanarak metin üretir."""
        if not self.gemini_model:
            raise Exception("Gemini API Key eksik.")
        
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()

    def icerik_uret(self, konu, mod="cyberpunk"):
        """
        HYBRID MOTOR: Önce ChatGPT'yi dener, hata alırsa Gemini'ye geçer.
        """
        # Prompt Tasarımı (Instagram Odaklı)
        ana_prompt = f"""
        Konu: '{konu}'
        
        GÖREV: Bu konu hakkında Instagram gönderisi için bir açıklama (caption) yaz.
        
        KURALLAR:
        1. Başlık: Dikkat çekici, büyük harfle başla.
        2. İçerik: Akıcı, emojili ve samimi bir dille 2-3 paragraf bilgi ver.
        3. Stil: {mod} temasına uygun olsun (Biraz fütüristik ve teknolojik).
        4. Hashtagler: En sona konuyla ilgili popüler 10 hashtag ekle.
        5. Türkçe yaz.
        """

        # 1. DENEME: ChatGPT
        try:
            logger.info(f"🧠 [1. Aşama] ChatGPT düşünmeye başladı: {konu}")
            sonuc = self._chatgpt_ile_yaz(ana_prompt)
            return {"kaynak": "ChatGPT", "metin": sonuc}
        except Exception as e:
            logger.warning(f"⚠️ ChatGPT Hata Verdi: {e}. Gemini devreye giriyor...")

        # 2. DENEME: Gemini (Failover)
        try:
            logger.info(f"🧠 [2. Aşama] Gemini düşünmeye başladı: {konu}")
            sonuc = self._gemini_ile_yaz(ana_prompt)
            return {"kaynak": "Gemini", "metin": sonuc}
        except Exception as e:
            logger.error(f"❌ Gemini de Hata Verdi: {e}")
            return {"kaynak": "HATA", "metin": "Üzgünüm, şu an beyinlerimde aşırı yüklenme var. Lütfen biraz sonra tekrar dene."}

# Test için (Dosya doğrudan çalıştırılırsa)
if __name__ == "__main__":
    beyin = HybridBrain()
    print(beyin.icerik_uret("Yapay Zeka Geleceği")["metin"])
