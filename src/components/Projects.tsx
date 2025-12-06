import React from 'react';
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
export default Projects;