import React from 'react';
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
export default Footer;