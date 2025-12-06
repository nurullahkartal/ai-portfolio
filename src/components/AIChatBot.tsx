import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, Loader2 } from 'lucide-react';
import { ChatMessage, Project } from '../types';
import { sendMessageToGemini } from '../services/geminiService';

interface AIChatBotProps { projects: Project[]; }

const AIChatBot: React.FC<AIChatBotProps> = ({ projects }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', text: 'Merhaba! Ben Nurullah\'ın yapay zeka asistanıyım. Nasıl yardımcı olabilirim?', timestamp: new Date() }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMessage: ChatMessage = { role: 'user', text: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const history = messages.map(m => ({ role: m.role, parts: [{ text: m.text }] }));
      const responseText = await sendMessageToGemini(userMessage.text, history, projects);
      setMessages(prev => [...prev, { role: 'model', text: responseText, timestamp: new Date() }]);
    } catch {
      setMessages(prev => [...prev, { role: 'model', text: 'Hata oluştu.', timestamp: new Date() }]);
    } finally { setLoading(false); }
  };

  return (
    <>
      <button onClick={() => setIsOpen(true)} className={`fixed bottom-6 right-6 z-40 p-4 bg-brand-accent text-white rounded-full shadow-2xl transition-all ${isOpen ? 'opacity-0 scale-0 pointer-events-none' : ''}`}>
        <MessageSquare size={28} />
      </button>
      <div className={`fixed bottom-6 right-6 z-50 w-[90vw] md:w-[400px] h-[500px] bg-brand-card border border-white/10 rounded-2xl shadow-2xl flex flex-col transition-all origin-bottom-right ${isOpen ? 'scale-100 opacity-100' : 'scale-90 opacity-0 pointer-events-none'}`}>
        <div className="flex justify-between p-4 border-b border-white/5 bg-brand-dark/50 rounded-t-2xl">
          <div className="flex items-center gap-3"><Bot className="text-brand-accent" /> <span className="font-bold text-white">Nurullah AI</span></div>
          <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white"><X size={20} /></button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.role === 'user' ? 'bg-brand-accent text-white' : 'bg-white/10 text-gray-200'}`}>{msg.text}</div>
            </div>
          ))}
          {loading && <Loader2 className="animate-spin text-brand-accent" />}
          <div ref={messagesEndRef} />
        </div>
        <div className="p-4 border-t border-white/5">
          <div className="flex gap-2">
            <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} placeholder="Bir soru sorun..." className="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2 text-sm text-white focus:border-brand-accent outline-none" />
            <button onClick={handleSend} disabled={loading} className="p-2 bg-brand-accent rounded-full text-white"><Send size={18} /></button>
          </div>
        </div>
      </div>
    </>
  );
};
export default AIChatBot;