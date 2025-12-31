'use client';

import { Home, Swords, BarChart3, Settings, Activity } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

interface AppShellProps {
  children: ReactNode;
}

const navigation = [
  { name: 'Übersicht', href: '/', icon: Home },
  { name: 'Draft Phase', href: '/draft', icon: Swords },
  { name: 'Live Game', href: '/live', icon: Activity },
  { name: 'Statistiken', href: '/stats', icon: BarChart3 },
  { name: 'Einstellungen', href: '/settings', icon: Settings },
];

export default function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar - Fixed Left with Glass Effect */}
      <aside className="w-64 bg-sidebar/50 backdrop-blur-md border-r border-white/10 flex flex-col">
        {/* Logo Area */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="accent-dot" />
            <h1 className="text-xl font-bold text-foreground gradient-text">
              Hextech Data
            </h1>
          </div>
          <p className="text-xs text-muted-foreground mt-1 ml-[18px]">
            Gaming Intelligence Engine
          </p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.name}
                href={item.href}
                className={`
                  flex items-center gap-3 px-4 py-3 rounded-lg
                  transition-all duration-200
                  ${
                    isActive
                      ? 'bg-white/10 text-foreground border border-primary/40 backdrop-blur-sm'
                      : 'text-muted-foreground hover:bg-white/5 hover:text-foreground'
                  }
                `}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer Info */}
        <div className="p-4 border-t border-white/10">
          <div className="text-xs text-muted-foreground">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse status-led" />
              <span className="text-success font-medium">System Online</span>
            </div>
            <p className="mt-2 opacity-60">v0.1.0 Beta</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header - Glass Effect */}
        <header className="glass-header sticky top-0 z-10 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-foreground">
                {navigation.find((item) => item.href === pathname)?.name || 'Dashboard'}
              </h2>
              <p className="text-sm text-muted-foreground">
                Echtzeit-Analysen powered by AI
              </p>
            </div>

            {/* Header Actions */}
            <div className="flex items-center gap-3">
              <div className="glass-card px-4 py-2">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Patch</span>
                  <span className="text-sm font-semibold text-primary neon-glow">14.23</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content - Scrollable */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
