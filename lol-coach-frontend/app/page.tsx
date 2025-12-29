'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import ChampionSelectPredictor from '@/components/ChampionSelectPredictor';
import ChampionStatsExplorer from '@/components/ChampionStatsExplorer';
import ItemRecommendations from '@/components/ItemRecommendations';
import ChampionSearch from '@/components/ChampionSearch';
import ChampionSearchModal from '@/components/ChampionSearchModal';
import { useRouter } from 'next/navigation';
import { Target, Activity, Search, Cpu, TrendingUp } from 'lucide-react';
import Image from 'next/image';
import { useModelStats } from '@/hooks/useModelStats';
import { formatAccuracy, formatMatchCount } from '@/lib/model-stats';

export default function Home() {
  const router = useRouter();
  const { stats, loading } = useModelStats();

  // Dynamic stats with fallback
  const accuracy = stats ? formatAccuracy(stats.accuracy) : '52.0%';
  const matchCount = stats ? formatMatchCount(stats.matches_count) : '12.8K';
  const matchCountFull = stats ? stats.matches_count.toLocaleString() : '12,834';

  return (
    <div className="min-h-screen bg-background">
      {/* HUD Header */}
      <header className="sticky top-0 z-50 glass-overlay">
        <div className="terminal-line mb-px" />
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="relative w-12 h-12 hex-glow">
                <Image
                  src="/logo.png"
                  alt="LoL Coach"
                  width={48}
                  height={48}
                  className="drop-shadow-[0_0_15px_rgba(76,201,240,0.8)]"
                />
              </div>
              <h1 className="text-xl font-bold cortana-glow" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                GAMING WAR ROOM
              </h1>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-2">
              <ChampionSearchModal />
              <Button
                variant="ghost"
                onClick={() => router.push('/draft')}
                className="btn-primary h-9 px-4"
              >
                <Target className="mr-2 h-4 w-4" />
                WAR DRAFT
              </Button>
              <Button
                variant="ghost"
                onClick={() => router.push('/live')}
                className="btn-primary h-9 px-4"
              >
                <Activity className="mr-2 h-4 w-4" />
                LIVE COMBAT
              </Button>
            </nav>
          </div>
        </div>
        <div className="terminal-line mt-px" />
      </header>

      {/* Hero HUD */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        {/* Grid overlay effect - Halo tactical grid */}
        <div className="absolute inset-0 opacity-10 scan-lines" style={{
          backgroundImage: 'linear-gradient(rgba(30,144,255,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(30,144,255,0.12) 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }} />

        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl">
            {/* Status Badge */}
            <div className="mb-8 flex justify-center">
              <div className="inline-flex items-center gap-2 rounded-md border border-primary/30 bg-card/50 px-4 py-2 backdrop-blur-sm">
                <div className="hex-point" />
                <span className="stat-label">Systems Online</span>
                <div className="h-2 w-2 rounded-full bg-[rgb(0,230,118)]" style={{
                  boxShadow: '0 0 10px rgba(0,230,118,0.8)'
                }} />
              </div>
            </div>

            {/* Main Heading */}
            <div className="text-center space-y-6">
              <h2 className="text-6xl sm:text-8xl font-bold leading-none" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                <span className="cortana-glow">VICTORY AI</span>
                <br />
                <span className="text-foreground">PREDICTION ENGINE</span>
              </h2>

              <p className="text-lg sm:text-xl text-card-foreground max-w-2xl mx-auto">
                Advanced AI analytics - Real-time match intelligence for competitive gaming supremacy
              </p>

              {/* STATS GRID */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto mt-20">

                {/* STAT 1: MODEL ACCURACY */}
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm">
                  <div className="text-4xl font-black text-[#1E90FF] mb-2 drop-shadow-[0_0_10px_rgba(30,144,255,0.5)]">
                    {loading ? '...' : accuracy}
                  </div>
                  <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">
                    BASELINE MODEL ACCURACY
                  </div>
                </div>

                {/* STAT 2: DATA VOLUME */}
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm">
                  <div className="text-4xl font-black text-[#1E90FF] mb-2 drop-shadow-[0_0_10px_rgba(30,144,255,0.5)]">
                    {loading ? '...' : `${matchCount}+`}
                  </div>
                  <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">
                    MATCHES ANALYZED
                  </div>
                </div>

                {/* STAT 3: ARCHITECTURE */}
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm">
                  <div className="text-4xl font-black text-[#1E90FF] mb-2 drop-shadow-[0_0_10px_rgba(30,144,255,0.5)]">
                    V.2.1
                  </div>
                  <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">
                    SYSTEM ARCHITECTURE
                  </div>
                </div>

              </div>

              {/* CTAs */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
                <Button
                  size="lg"
                  onClick={() => router.push('/draft')}
                  className="btn-primary h-14 px-10 text-base"
                >
                  <Cpu className="mr-2 h-5 w-5" />
                  START ANALYSIS
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  onClick={() => router.push('/live')}
                  className="h-14 px-10 text-base border-[rgba(0,100,180,0.4)] text-[rgb(0,100,180)] hover:bg-[rgba(0,100,180,0.2)]"
                  style={{textShadow: '0 0 10px rgba(0,100,180,0.7)'}}
                >
                  <Activity className="mr-2 h-5 w-5" />
                  LIVE GAME FEED
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Analysis Modules */}
      <section className="relative border-t border-primary/20 py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl sm:text-5xl font-bold mb-4" style={{fontFamily: "'Rajdhani', sans-serif"}}>
              <span className="text-foreground">ANALYSIS MODULES</span>
            </h2>
            <div className="terminal-line w-64 mx-auto" />
          </div>

          <Tabs defaultValue="predictor" className="mx-auto max-w-6xl">
            <TabsList className="grid w-full grid-cols-1 md:grid-cols-3 h-auto gap-4 bg-transparent p-0">
              <TabsTrigger
                value="predictor"
                className="hud-card data-[state=active]:border-primary/60 rounded-lg py-6 px-4"
              >
                <div className="flex flex-col items-center gap-2">
                  <Cpu className="h-8 w-8 text-primary" style={{filter: 'drop-shadow(0 0 8px rgba(30,144,255,0.9))'}} />
                  <div className="stat-label">Victory AI</div>
                  <div className="text-xs text-card-foreground/60">{accuracy} Accuracy</div>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="stats"
                className="hud-card data-[state=active]:border-primary/60 rounded-lg py-6 px-4"
              >
                <div className="flex flex-col items-center gap-2">
                  <TrendingUp className="h-8 w-8 text-primary" style={{filter: 'drop-shadow(0 0 8px rgba(30,144,255,0.9))'}} />
                  <div className="stat-label">Player Analytics</div>
                  <div className="text-xs text-card-foreground/60">Deep Stats</div>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="items"
                className="hud-card data-[state=active]:border-accent/60 rounded-lg py-6 px-4"
              >
                <div className="flex flex-col items-center gap-2">
                  <Activity className="h-8 w-8 text-accent" style={{filter: 'drop-shadow(0 0 8px rgba(0,100,180,0.9))'}} />
                  <div className="stat-label">Build Optimizer</div>
                  <div className="text-xs text-card-foreground/60">Adaptive Builds</div>
                </div>
              </TabsTrigger>
            </TabsList>

            <div className="mt-10">
              <TabsContent value="predictor" className="m-0">
                <div className="hud-card rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-primary/20">
                    <div className="hex-point" />
                    <div>
                      <h3 className="text-2xl font-bold" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                        AI VICTORY PREDICTOR
                      </h3>
                      <p className="text-sm text-card-foreground/70">
                        Machine learning win prediction - Analyze team composition for competitive advantage
                      </p>
                    </div>
                  </div>
                  <ChampionSelectPredictor />
                </div>
              </TabsContent>

              <TabsContent value="stats" className="m-0">
                <div className="hud-card rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-primary/20">
                    <div className="hex-point" />
                    <div>
                      <h3 className="text-2xl font-bold" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                        CHAMPION DATABASE
                      </h3>
                      <p className="text-sm text-card-foreground/70">
                        Complete player stats - Win rates, performance metrics, and competitive effectiveness
                      </p>
                    </div>
                  </div>
                  <ChampionStatsExplorer />
                </div>
              </TabsContent>

              <TabsContent value="items" className="m-0">
                <div className="hud-card rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-accent/30">
                    <div className="hex-point" style={{background: 'rgb(0,100,180)', boxShadow: '0 0 12px rgba(0,100,180,0.9)'}} />
                    <div>
                      <h3 className="text-2xl font-bold" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                        ADAPTIVE BUILD SYSTEM
                      </h3>
                      <p className="text-sm text-card-foreground/70">
                        Dynamic item recommendations - Optimized builds adapted to enemy matchups
                      </p>
                    </div>
                  </div>
                  <ItemRecommendations />
                </div>
              </TabsContent>
            </div>
          </Tabs>
        </div>
      </section>

      {/* Quick Search Terminal */}
      <section className="relative border-t border-primary/20 py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl">
            <div className="text-center mb-10">
              <div className="inline-flex items-center gap-2 mb-4">
                <Search className="h-5 w-5 text-primary" />
                <span className="stat-label">Fast Deploy</span>
              </div>
              <h2 className="text-3xl font-bold" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                CHAMPION ROSTER
              </h2>
            </div>
            <div className="hud-card rounded-lg p-8">
              <ChampionSearch />
            </div>
          </div>
        </div>
      </section>

      {/* System Footer */}
      <footer className="relative border-t border-primary/20 glass-overlay">
        <div className="terminal-line mb-px" />
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center space-y-6">
            <div className="flex items-center justify-center gap-3">
              <Image
                src="/logo.png"
                alt="War Room"
                width={32}
                height={32}
                className="drop-shadow-[0_0_15px_rgba(30,144,255,0.9)]"
              />
              <span className="text-xl font-bold cortana-glow" style={{fontFamily: "'Rajdhani', sans-serif"}}>
                GAMING WAR ROOM
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <div className="stat-label">
                <div className="text-primary text-sm mb-1">◆</div>
                Neural AI Engine
              </div>
              <div className="stat-label">
                <div className="text-accent text-sm mb-1">◆</div>
                Live Match Analytics
              </div>
              <div className="stat-label">
                <div className="text-[rgb(0,200,140)] text-sm mb-1">◆</div>
                {accuracy} Baseline Accuracy
              </div>
            </div>

            <div className="text-xs text-card-foreground/50 pt-4 border-t border-primary/10">
              ADVANCED GAMING INTELLIGENCE • {matchCountFull}+ Match Analysis • AI-Powered Victory Network V.2.1
            </div>
          </div>
        </div>
        <div className="terminal-line mt-px" />
      </footer>
    </div>
  );
}
