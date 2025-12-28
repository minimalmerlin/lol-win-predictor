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

export default function Home() {
  const router = useRouter();

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
                  className="drop-shadow-[0_0_15px_rgba(0,255,255,0.8)]"
                />
              </div>
              <h1 className="text-xl font-bold neon-cyan" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                NeuroPlay Analytics
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
                DRAFT
              </Button>
              <Button
                variant="ghost"
                onClick={() => router.push('/live')}
                className="btn-primary h-9 px-4"
              >
                <Activity className="mr-2 h-4 w-4" />
                LIVE
              </Button>
            </nav>
          </div>
        </div>
        <div className="terminal-line mt-px" />
      </header>

      {/* Hero HUD */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        {/* Grid overlay effect */}
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: 'linear-gradient(rgba(0,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,255,0.1) 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }} />
        
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl">
            {/* Status Badge */}
            <div className="mb-8 flex justify-center">
              <div className="inline-flex items-center gap-2 rounded-md border border-primary/30 bg-card/50 px-4 py-2 backdrop-blur-sm">
                <div className="hex-point" />
                <span className="stat-label">System Active</span>
                <div className="h-2 w-2 rounded-full bg-[rgb(0,230,118)]" style={{
                  boxShadow: '0 0 10px rgba(0,230,118,0.8)'
                }} />
              </div>
            </div>
            
            {/* Main Heading */}
            <div className="text-center space-y-6">
              <h2 className="text-6xl sm:text-8xl font-bold leading-none" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                <span className="neon-cyan">AI-POWERED</span>
                <br />
                <span className="text-foreground">WIN PREDICTION</span>
              </h2>
              
              <p className="text-lg sm:text-xl text-card-foreground max-w-2xl mx-auto">
                Advanced neural networks analyzing real-time game data for tactical superiority
              </p>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto pt-8">
                <div className="text-center">
                  <div className="stat-value">90.9%</div>
                  <div className="stat-label">Accuracy</div>
                </div>
                <div className="text-center">
                  <div className="stat-value neon-magenta">360K+</div>
                  <div className="stat-label">Matches</div>
                </div>
                <div className="text-center">
                  <div className="stat-value">Real-Time</div>
                  <div className="stat-label">Analysis</div>
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
                  INITIATE ANALYSIS
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  onClick={() => router.push('/live')}
                  className="h-14 px-10 text-base border-[rgba(225,0,255,0.3)] text-[rgb(225,0,255)] hover:bg-[rgba(225,0,255,0.1)]"
                  style={{textShadow: '0 0 5px rgba(225,0,255,0.5)'}}
                >
                  <Activity className="mr-2 h-5 w-5" />
                  LIVE TRACKING
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
            <h2 className="text-4xl sm:text-5xl font-bold mb-4" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
              <span className="text-foreground">TACTICAL SYSTEMS</span>
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
                  <Cpu className="h-8 w-8 text-primary" style={{filter: 'drop-shadow(0 0 5px rgba(0,255,255,0.6))'}} />
                  <div className="stat-label">Win Predictor</div>
                  <div className="text-xs text-card-foreground/60">90.9% Accuracy</div>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="stats"
                className="hud-card data-[state=active]:border-primary/60 rounded-lg py-6 px-4"
              >
                <div className="flex flex-col items-center gap-2">
                  <TrendingUp className="h-8 w-8 text-primary" style={{filter: 'drop-shadow(0 0 5px rgba(0,255,255,0.6))'}} />
                  <div className="stat-label">Champion Analytics</div>
                  <div className="text-xs text-card-foreground/60">Deep Stats</div>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="items"
                className="hud-card data-[state=active]:border-[rgba(225,0,255,0.3)] rounded-lg py-6 px-4"
              >
                <div className="flex flex-col items-center gap-2">
                  <Activity className="h-8 w-8 text-[rgb(225,0,255)]" style={{filter: 'drop-shadow(0 0 5px rgba(225,0,255,0.6))'}} />
                  <div className="stat-label">AI Builds</div>
                  <div className="text-xs text-card-foreground/60">Adaptive</div>
                </div>
              </TabsTrigger>
            </TabsList>

            <div className="mt-10">
              <TabsContent value="predictor" className="m-0">
                <div className="hud-card rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-primary/20">
                    <div className="hex-point" />
                    <div>
                      <h3 className="text-2xl font-bold" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                        WIN PREDICTION ENGINE
                      </h3>
                      <p className="text-sm text-card-foreground/70">
                        Real-time probability analysis based on team composition
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
                      <h3 className="text-2xl font-bold" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                        CHAMPION ANALYTICS
                      </h3>
                      <p className="text-sm text-card-foreground/70">
                        Performance metrics and statistical analysis
                      </p>
                    </div>
                  </div>
                  <ChampionStatsExplorer />
                </div>
              </TabsContent>

              <TabsContent value="items" className="m-0">
                <div className="hud-card rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-[rgba(225,0,255,0.2)]">
                    <div className="hex-point" style={{background: 'rgb(225,0,255)', boxShadow: '0 0 8px rgba(225,0,255,0.8)'}} />
                    <div>
                      <h3 className="text-2xl font-bold" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                        AI ITEM BUILDS
                      </h3>
                      <p className="text-sm text-card-foreground/70">
                        Dynamic recommendations based on game state
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
                <span className="stat-label">Quick Access</span>
              </div>
              <h2 className="text-3xl font-bold" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                CHAMPION DATABASE
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
                alt="LoL Coach"
                width={32}
                height={32}
                className="drop-shadow-[0_0_12px_rgba(0,255,255,0.8)]"
              />
              <span className="text-xl font-bold neon-cyan" style={{fontFamily: "'Chakra Petch', sans-serif"}}>
                NeuroPlay Analytics
              </span>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <div className="stat-label">
                <div className="text-primary text-sm mb-1">◆</div>
                Neural Network Analysis
              </div>
              <div className="stat-label">
                <div className="text-[rgb(225,0,255)] text-sm mb-1">◆</div>
                Real-Time Processing
              </div>
              <div className="stat-label">
                <div className="text-[rgb(0,230,118)] text-sm mb-1">◆</div>
                90.9% Accuracy
              </div>
            </div>
            
            <div className="text-xs text-card-foreground/50 pt-4 border-t border-primary/10">
              Trained on 360,000+ ranked matches • Powered by advanced ML models
            </div>
          </div>
        </div>
        <div className="terminal-line mt-px" />
      </footer>
    </div>
  );
}
