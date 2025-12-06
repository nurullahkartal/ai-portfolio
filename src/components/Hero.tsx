import React from 'react';
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
export default Hero;