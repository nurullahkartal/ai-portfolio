import os

# Proje Dosya İçerikleri
files = {
    "package.json": """{
  "name": "nurullah.ai-portfolio",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.2.1",
    "react-dom": "^19.2.1",
    "lucide-react": "^0.556.0",
    "@google/genai": "^1.31.0"
  },
  "devDependencies": {
    "@types/node": "^22.14.0",
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "~5.8.2",
    "vite": "^6.2.0"
  }
}""",

    "vite.config.ts": """import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
    return {
      server: {
        port: 3000,
        host: '0.0.0.0',
      },
      plugins: [react()],
      define: {
        'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY)
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, './src'),
        }
      }
    };
});""",

    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2022",
    "experimentalDecorators": true,
    "useDefineForClassFields": false,
    "module": "ESNext",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "types": ["node"],
    "moduleResolution": "bundler",
    "isolatedModules": true,
    "moduleDetection": "force",
    "allowJs": true,
    "jsx": "react-jsx",
    "paths": {
      "@/*": ["./src/*"]
    },
    "allowImportingTsExtensions": true,
    "noEmit": true
  },
  "include": ["src"]
}""",

    ".env.local": """GEMINI_API_KEY=PLACEHOLDER_API_KEY""",

    ".gitignore": """node_modules
dist
dist-ssr
*.local
.DS_Store
*.log
""",

    "index.html": """<!DOCTYPE html>
<html lang="tr" class="scroll-smooth">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Nurullah.AI - Portfolio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
      tailwind.config = {
        theme: {
          extend: {
            fontFamily: {
              sans: ['Inter', 'sans-serif'],
            },
            colors: {
              brand: {
                dark: '#0B0C15',
                card: '#13141F',
                accent: '#8B5CF6',
                accentHover: '#7C3AED',
                text: '#E2E8F0',
                muted: '#94A3B8'
              }
            }
          }
        }
      }
    </script>
    <style>
      body { background-color: #0B0C15; color: #E2E8F0; }
      ::-webkit-scrollbar { width: 8px; }
      ::-webkit-scrollbar-track { background: #0B0C15; }
      ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: #475569; }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/index.tsx"></script>
  </body>
</html>""",

    "src/index.tsx": """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const rootElement = document.getElementById('root');
if (!rootElement) throw new Error("Could not find root element");

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""",

    "src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;""",

    "src/types.ts": """import { LucideIcon } from 'lucide-react';

export interface Project {
  id: number;
  title: string;
  description: string;
  icon: LucideIcon;
  tags: string[];
}

export interface NavItem {
  label: string;
  href: string;
}

export interface ChatMessage {
  role: 'user' | 'model';
  text: string;
  timestamp: Date;
}

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
  status: 'Satışta' | 'Tükendi' | 'Kritik';
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'Yönetici' | 'Editör' | 'İzleyici';
  status: 'Aktif' | 'Pasif';
  lastLogin: string;
}

export interface BlogPost {
  id: number;
  title: string;
  category: string;
  status: 'Yayında' | 'Taslak';
  date: string;
}

export interface SystemLog {
  id: number;
  action: string;
  user: string;
  time: string;
}

export interface SiteSettings {
  title: string;
  description: string;
  maintenanceMode: boolean;
  twoFactorAuth: boolean;
}

export interface ProfileSettings {
  email: string;
  github: string;
  linkedin: string;
  twitter: string;
  instagram: string;
}""",

    "src/services/geminiService.ts": """import { GoogleGenerativeAI } from "@google/genai";
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
    ).join('\\n');

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
};""",

    "src/App.tsx": """import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import Projects from './components/Projects';
import Contact from './components/Contact';
import AIChatBot from './components/AIChatBot';
import Footer from './components/Footer';
import AdminPanel from './components/AdminPanel';
import { Project, ProfileSettings } from './types';
import { PieChart } from 'lucide-react';

const initialProjects: Project[] = [
  {
    id: 1,
    title: "Veri Analiz Botu",
    description: "İstatistiksel verileri otomatik çeken ve görselleştiren bot.",
    icon: PieChart,
    tags: ["Python", "Data Analysis"]
  }
];

const initialProfile: ProfileSettings = {
  email: "nurullahkartalai@gmail.com",
  github: "https://github.com",
  linkedin: "https://linkedin.com",
  twitter: "",
  instagram: ""
};

const App: React.FC = () => {
  const loadState = <T,>(key: string, defaultValue: T): T => {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : defaultValue;
    } catch { return defaultValue; }
  };

  const [projects, setProjects] = useState<Project[]>(() => loadState('projects', initialProjects));
  const [profile, setProfile] = useState<ProfileSettings>(() => loadState('profile', initialProfile));
  const [siteSettings, setSiteSettings] = useState(() => loadState('siteSettings', {
    title: 'Nurullah.AI - Portfolio',
    description: 'Yapay zeka portfolyosu.',
    maintenanceMode: false,
    twoFactorAuth: true,
  }));
  const [isAdminOpen, setIsAdminOpen] = useState(false);

  useEffect(() => { localStorage.setItem('projects', JSON.stringify(projects)); }, [projects]);
  useEffect(() => { localStorage.setItem('profile', JSON.stringify(profile)); }, [profile]);
  useEffect(() => { 
    localStorage.setItem('siteSettings', JSON.stringify(siteSettings));
    document.title = siteSettings.title;
  }, [siteSettings]);

  return (
    <div className="min-h-screen bg-brand-dark text-brand-text font-sans selection:bg-brand-accent selection:text-white relative">
      {siteSettings.maintenanceMode && (
        <div className="bg-red-600 text-white text-center py-2 font-bold sticky top-0 z-[60]">
          ⚠ BAKIM MODU
        </div>
      )}
      <Navbar />
      <main>
        <Hero />
        <About />
        <Projects projects={projects} />
        <Contact profile={profile} />
      </main>
      <Footer onAdminClick={() => setIsAdminOpen(true)} profile={profile} />
      <AIChatBot projects={projects} />
      {isAdminOpen && (
        <AdminPanel 
          isOpen={isAdminOpen} 
          onClose={() => setIsAdminOpen(false)} 
          projects={projects} setProjects={setProjects}
          siteSettings={siteSettings} setSiteSettings={setSiteSettings}
          profile={profile} setProfile={setProfile}
        />
      )}
    </div>
  );
};
export default App;""",

    # COMPONENTS
    "src/components/Navbar.tsx": """import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { NavItem } from '../types';

const navItems: NavItem[] = [
  { label: 'Ana Sayfa', href: '#hero' },
  { label: 'Hakkımda', href: '#about' },
  { label: 'Projeler', href: '#projects' },
  { label: 'İletişim', href: '#contact' },
];

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${scrolled ? 'bg-brand-dark/90 backdrop-blur-md py-4 border-b border-white/10' : 'bg-transparent py-6'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-brand-accent">Nurullah.AI</span>
          
          <div className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <a key={item.label} href={item.href} className="text-sm font-medium text-brand-text hover:text-brand-accent transition-colors">{item.label}</a>
            ))}
          </div>

          <div className="md:hidden">
            <button onClick={() => setIsOpen(!isOpen)} className="text-brand-text hover:text-white">
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>
      {isOpen && (
        <div className="md:hidden bg-brand-card border-t border-white/10 absolute w-full">
          <div className="px-4 pt-2 pb-6 space-y-1">
            {navItems.map((item) => (
              <a key={item.label} href={item.href} onClick={() => setIsOpen(false)} className="block px-3 py-3 rounded-md text-base font-medium text-brand-text hover:bg-white/5">{item.label}</a>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};
export default Navbar;""",

    "src/components/Hero.tsx": """import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';

const Hero: React.FC = () => {
  return (
    <section id="hero" className="relative min-h-screen flex items-center pt-20 overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-accent/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[120px]"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
        <div className="flex flex-col md:flex-row items-center justify-between gap-12">
          <div className="flex-1 space-y-8 text-center md:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-accent/10 border border-brand-accent/20 text-brand-accent text-sm font-medium">
              <Sparkles size={14} /> <span>Yapay Zeka Destekli Çözümler</span>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold leading-tight text-white">
              Geleceği Kodluyorum, <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-accent to-blue-400">Bugünden.</span>
            </h1>
            <p className="text-lg md:text-xl text-brand-muted max-w-2xl mx-auto md:mx-0">
              Yapay zeka ve modern web teknolojileri ile işletmeniz için ölçeklenebilir çözümler.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
              <a href="#projects" className="px-8 py-4 bg-brand-accent hover:bg-brand-accentHover text-white rounded-lg font-semibold flex items-center justify-center gap-2">
                Projeleri İncele <ArrowRight size={18} />
              </a>
              <a href="#contact" className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 text-white rounded-lg font-semibold">İletişime Geç</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
export default Hero;""",

    "src/components/About.tsx": """import React from 'react';
import { Code, Cpu, Globe, Sparkles, User, Zap, Layers } from 'lucide-react';

const About: React.FC = () => {
  return (
    <section id="about" className="py-24 bg-[#0B0C15] relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Hakkımda</h2>
          <p className="text-brand-muted">Dijital dünyada iz bırakan çözümler.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <div className="space-y-8">
            <div className="bg-[#13141F] rounded-2xl p-8 border border-white/5">
              <div className="flex items-center gap-4 mb-6">
                <User className="text-brand-accent" size={24} />
                <h3 className="text-xl font-bold text-white">Ben Kimim?</h3>
              </div>
              <p className="text-gray-400 mb-4">
                Merhaba, ben Nurullah. Teknolojiye tutkulu bir **Full Stack Geliştirici** ve **AI Mühendisiyim**.
              </p>
            </div>
            
            <div className="bg-[#13141F] rounded-2xl p-8 border border-white/5">
                <div className="flex items-center gap-4 mb-6">
                    <Layers className="text-blue-400" size={24} />
                    <h3 className="text-xl font-bold text-white">Teknoloji Yığını</h3>
                </div>
                <div className="space-y-3 text-sm text-gray-300">
                    <div className="flex gap-2"><Globe size={16}/> React 19 & TypeScript</div>
                    <div className="flex gap-2"><Sparkles size={16}/> Google Gemini AI</div>
                    <div className="flex gap-2"><Zap size={16}/> Tailwind CSS</div>
                </div>
            </div>
          </div>

          <div className="bg-[#13141F] rounded-2xl p-8 border border-white/5">
            <h3 className="text-xl font-bold text-white mb-8 flex items-center gap-3">
              <Cpu className="text-brand-accent" /> Yetenekler
            </h3>
            <div className="space-y-8">
              <div>
                <h4 className="text-sm font-semibold text-gray-400 uppercase mb-4">AI & Data</h4>
                <div className="flex flex-wrap gap-2">
                  {['Python', 'TensorFlow', 'LLM', 'NLP', 'Computer Vision'].map(s => (
                    <span key={s} className="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">{s}</span>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-gray-400 uppercase mb-4">Web</h4>
                <div className="flex flex-wrap gap-2">
                  {['React', 'Next.js', 'Node.js', 'PostgreSQL', 'Docker'].map(s => (
                    <span key={s} className="px-3 py-1 bg-blue-500/10 text-blue-300 rounded-full text-xs">{s}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
export default About;""",

    "src/components/Projects.tsx": """import React from 'react';
import { Project } from '../types';
import { ArrowRight } from 'lucide-react';

interface ProjectsProps { projects: Project[]; }

const Projects: React.FC<ProjectsProps> = ({ projects }) => {
  return (
    <section id="projects" className="py-24 bg-brand-dark">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Seçili Projeler</h2>
        </div>
        
        {projects.length === 0 ? (
          <div className="text-center text-gray-500">Henüz proje eklenmemiş.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {projects.map((project) => (
              <div key={project.id} className="group bg-[#151621] rounded-2xl p-8 border border-white/5 hover:border-brand-accent/50 transition-all">
                <div className="w-14 h-14 rounded-lg bg-brand-accent/10 flex items-center justify-center mb-6">
                  <project.icon className="text-brand-accent w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{project.title}</h3>
                <p className="text-brand-muted mb-6 h-24 overflow-hidden">{project.description}</p>
                <div className="flex flex-wrap gap-2 mb-8">
                  {project.tags.map(tag => (
                    <span key={tag} className="text-xs px-2 py-1 rounded bg-white/5 text-gray-400">{tag}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
export default Projects;""",

    "src/components/Contact.tsx": """import React from 'react';
import { Mail, Github, Linkedin, Twitter, Instagram } from 'lucide-react';
import { ProfileSettings } from '../types';

interface ContactProps { profile: ProfileSettings; }

const Contact: React.FC<ContactProps> = ({ profile }) => {
  return (
    <section id="contact" className="py-24 bg-brand-dark">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <h2 className="text-3xl font-bold text-white mb-12">Bana Ulaşın</h2>
        <div className="bg-[#13141F] rounded-3xl p-8 border border-white/5">
            <p className="text-xl text-gray-300 mb-8">Projeler ve iş birlikleri için iletişime geçin.</p>
            <a href={`mailto:${profile.email}`} className="inline-flex items-center gap-3 px-6 py-4 bg-brand-accent hover:bg-brand-accentHover text-white rounded-lg mb-10">
                <Mail size={20} /> <span>{profile.email}</span>
            </a>
            <div className="flex justify-center gap-6">
              {profile.github && <a href={profile.github} target="_blank" className="text-gray-400 hover:text-white"><Github /></a>}
              {profile.linkedin && <a href={profile.linkedin} target="_blank" className="text-gray-400 hover:text-white"><Linkedin /></a>}
              {profile.twitter && <a href={profile.twitter} target="_blank" className="text-gray-400 hover:text-white"><Twitter /></a>}
            </div>
        </div>
      </div>
    </section>
  );
};
export default Contact;""",

    "src/components/Footer.tsx": """import React from 'react';
import { Lock } from 'lucide-react';
import { ProfileSettings } from '../types';

interface FooterProps { onAdminClick: () => void; profile: ProfileSettings; }

const Footer: React.FC<FooterProps> = ({ onAdminClick }) => {
  return (
    <footer className="py-8 bg-[#08090F] border-t border-white/5">
      <div className="max-w-7xl mx-auto px-4 text-center flex flex-col items-center gap-4">
        <p className="text-sm text-gray-500">© {new Date().getFullYear()} Nurullah.AI - Tüm hakları saklıdır.</p>
        <button onClick={onAdminClick} className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-full text-xs text-gray-400 hover:text-white transition-all">
            <Lock size={12} /> <span>Yönetici Paneli</span>
        </button>
      </div>
    </footer>
  );
};
export default Footer;""",

    "src/components/AIChatBot.tsx": """import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, Loader2 } from 'lucide-react';
import { ChatMessage, Project } from '../types';
import { sendMessageToGemini } from '../services/geminiService';

interface AIChatBotProps { projects: Project[]; }

const AIChatBot: React.FC<AIChatBotProps> = ({ projects }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', text: 'Merhaba! Ben Nurullah\\'ın yapay zeka asistanıyım. Nasıl yardımcı olabilirim?', timestamp: new Date() }
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
export default AIChatBot;""",

    "src/components/AdminPanel.tsx": """import React, { useState, useEffect } from 'react';
import { X, Plus, Trash2, PieChart, Globe, Terminal, Cpu, Shield, Database, Lock, LayoutDashboard, FileText, ShoppingBag, Users, Settings, Save, RefreshCw } from 'lucide-react';
import { Project, Product, User, BlogPost, SiteSettings, ProfileSettings } from '../types';

interface AdminPanelProps {
  isOpen: boolean; onClose: () => void;
  projects: Project[]; setProjects: React.Dispatch<React.SetStateAction<Project[]>>;
  siteSettings: SiteSettings; setSiteSettings: React.Dispatch<React.SetStateAction<SiteSettings>>;
  profile: ProfileSettings; setProfile: React.Dispatch<React.SetStateAction<ProfileSettings>>;
}

const iconOptions = [{ name: 'PieChart', icon: PieChart }, { name: 'Terminal', icon: Terminal }, { name: 'Globe', icon: Globe }, { name: 'Cpu', icon: Cpu }, { name: 'Shield', icon: Shield }, { name: 'Database', icon: Database }];

const AdminPanel: React.FC<AdminPanelProps> = ({ isOpen, onClose, projects, setProjects, siteSettings, setSiteSettings, profile, setProfile }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  
  // Local Forms
  const [newProjectTitle, setNewProjectTitle] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  const [selectedIconIdx, setSelectedIconIdx] = useState(0);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === 'admin123') setIsAuthenticated(true);
  };

  const handleSaveProject = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectTitle) return;
    const newProject: Project = {
      id: Date.now(),
      title: newProjectTitle,
      description: newProjectDesc,
      tags: ['New'],
      icon: iconOptions[selectedIconIdx].icon
    };
    setProjects([...projects, newProject]);
    setNewProjectTitle(''); setNewProjectDesc('');
  };

  const handleDeleteProject = (id: number) => {
    if (confirm('Silmek istediğine emin misin?')) setProjects(projects.filter(p => p.id !== id));
  };

  if (!isOpen) return null;

  if (!isAuthenticated) {
    return (
      <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/90 backdrop-blur">
        <div className="bg-[#13141F] p-8 rounded-2xl border border-white/10 w-96 text-center">
            <button onClick={onClose} className="absolute top-4 right-4 text-gray-400"><X /></button>
            <Lock className="mx-auto text-brand-accent mb-4" size={32} />
            <h2 className="text-white text-xl font-bold mb-4">Yönetici Paneli</h2>
            <form onSubmit={handleLogin}>
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Şifre: admin123" className="w-full bg-white/5 border border-white/10 rounded p-2 text-white mb-4 text-center" />
                <button type="submit" className="w-full bg-brand-accent py-2 rounded text-white font-bold">Giriş</button>
            </form>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-[60] flex bg-[#0B0C15] text-white">
      <aside className="w-64 bg-[#13141F] border-r border-white/5 p-4 flex flex-col gap-2">
        <div className="text-xl font-bold text-center mb-8">Nurullah.AI</div>
        <button onClick={() => setActiveTab('dashboard')} className={`p-3 rounded text-left ${activeTab === 'dashboard' ? 'bg-brand-accent' : 'hover:bg-white/5'}`}>Dashboard</button>
        <button onClick={() => setActiveTab('content')} className={`p-3 rounded text-left ${activeTab === 'content' ? 'bg-brand-accent' : 'hover:bg-white/5'}`}>İçerik</button>
        <button onClick={() => setActiveTab('settings')} className={`p-3 rounded text-left ${activeTab === 'settings' ? 'bg-brand-accent' : 'hover:bg-white/5'}`}>Ayarlar</button>
        <button onClick={onClose} className="mt-auto p-3 text-red-400 hover:bg-red-500/10 rounded">Çıkış</button>
      </aside>
      
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-8">
            <h1 className="text-2xl font-bold capitalize">{activeTab}</h1>
            <button onClick={onClose}><X /></button>
        </header>

        {activeTab === 'dashboard' && (
            <div className="grid grid-cols-3 gap-6">
                <div className="bg-[#13141F] p-6 rounded-xl border border-white/5">
                    <h3 className="text-gray-400">Toplam Proje</h3>
                    <p className="text-3xl font-bold">{projects.length}</p>
                </div>
            </div>
        )}

        {activeTab === 'content' && (
            <div className="space-y-8">
                <div className="bg-[#13141F] p-6 rounded-xl border border-white/5">
                    <h3 className="font-bold mb-4">Yeni Proje Ekle</h3>
                    <form onSubmit={handleSaveProject} className="space-y-4">
                        <input value={newProjectTitle} onChange={e => setNewProjectTitle(e.target.value)} placeholder="Proje Başlığı" className="w-full bg-black/20 border border-white/10 rounded p-2 text-white" />
                        <textarea value={newProjectDesc} onChange={e => setNewProjectDesc(e.target.value)} placeholder="Açıklama" className="w-full bg-black/20 border border-white/10 rounded p-2 text-white" />
                        <div className="flex gap-2">
                            {iconOptions.map((opt, i) => (
                                <button type="button" key={i} onClick={() => setSelectedIconIdx(i)} className={`p-2 rounded border ${selectedIconIdx === i ? 'bg-brand-accent border-brand-accent' : 'border-white/10'}`}>
                                    <opt.icon size={16} />
                                </button>
                            ))}
                        </div>
                        <button type="submit" className="bg-brand-accent px-4 py-2 rounded text-white flex items-center gap-2"><Plus size={16}/> Ekle</button>
                    </form>
                </div>
                
                <div className="space-y-2">
                    {projects.map(p => (
                        <div key={p.id} className="flex justify-between items-center bg-[#13141F] p-4 rounded border border-white/5">
                            <span>{p.title}</span>
                            <button onClick={() => handleDeleteProject(p.id)} className="text-red-400"><Trash2 size={16} /></button>
                        </div>
                    ))}
                </div>
            </div>
        )}

        {activeTab === 'settings' && (
             <div className="bg-[#13141F] p-6 rounded-xl border border-white/5 space-y-4">
                <h3 className="font-bold">Profil Ayarları</h3>
                <input value={profile.email} onChange={e => setProfile({...profile, email: e.target.value})} placeholder="Email" className="w-full bg-black/20 border border-white/10 rounded p-2 text-white" />
                <input value={profile.github} onChange={e => setProfile({...profile, github: e.target.value})} placeholder="Github URL" className="w-full bg-black/20 border border-white/10 rounded p-2 text-white" />
                <input value={profile.linkedin} onChange={e => setProfile({...profile, linkedin: e.target.value})} placeholder="Linkedin URL" className="w-full bg-black/20 border border-white/10 rounded p-2 text-white" />
             </div>
        )}
      </main>
    </div>
  );
};
export default AdminPanel;"""
}

# Dosyaları Oluşturma
def create_project():
    print("🚀 Nurullah.AI Proje Kurulumu Başlatılıyor...")
    
    for filepath, content in files.items():
        # Klasörleri oluştur
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        # Dosyayı yaz
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
            print(f"✅ Oluşturuldu: {filepath}")

    print("\n🎉 Kurulum Tamamlandı!")
    print("\nŞimdi şu komutları çalıştır:")
    print("1. npm install")
    print("2. npm run dev")
    print("\nNOT: .env.local dosyasına Gemini API anahtarını eklemeyi unutma!")

if __name__ == "__main__":
    create_project()