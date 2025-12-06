import React, { useState, useEffect } from 'react';
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
export default Navbar;