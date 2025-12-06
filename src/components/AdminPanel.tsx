import React, { useState, useEffect } from 'react';
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
export default AdminPanel;