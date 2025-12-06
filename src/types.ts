import { LucideIcon } from 'lucide-react';

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
}