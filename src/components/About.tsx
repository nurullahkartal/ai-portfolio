import React from 'react';
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
export default About;