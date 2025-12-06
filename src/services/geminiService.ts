import { GoogleGenerativeAI } from "@google/generative-ai";
import { Project } from "../types";

const API_KEY = import.meta.env.VITE_GEMINI_API_KEY || process.env.GEMINI_API_KEY;

const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

export const sendMessageToGemini = async (
  userMessage: string,
  history: { role: string; parts: { text: string }[] }[],
  projects: Project[]
): Promise<string> => {
  try {
    if (!API_KEY || API_KEY.includes('PLACEHOLDER')) {
      return "API anahtarı eksik. Lütfen .env.local dosyasını kontrol edin.";
    }

    const projectsContext = projects.map(p => 
      `- ${p.title}: ${p.description} [${p.tags.join(', ')}]`
    ).join('\n');

    const systemInstruction = `
      Sen Nurullah'ın AI asistanısın. Aşağıdaki projeleri referans alarak soruları cevapla:
      ${projectsContext}
      Cevapları Türkçe ver, samimi ve profesyonel ol.
    `;

    const chat = model.startChat({
      history: history,
      systemInstruction: { role: 'system', parts: [{ text: systemInstruction }]}
    });

    const result = await chat.sendMessage(userMessage);
    return result.response.text();
  } catch (error) {
    console.error("Gemini Hatası:", error);
    return "Şu anda bağlantı sorunu yaşıyorum.";
  }
};