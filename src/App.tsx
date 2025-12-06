import React, { useState, useEffect } from 'react';
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
export default App;