import React from 'react';
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
export default Contact;