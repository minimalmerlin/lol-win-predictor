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
import { Target, Activity, Sparkles, Trophy, Zap } from 'lucide-react';
import Image from 'next/image';

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen gaming-gradient">
      {/* Luxury Header */}
      <header className="sticky top-0 z-50 glass border-b border-primary/10">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="relative w-10 h-10 flex items-center justify-center shimmer">
                <Image 
                  src="/logo.svg" 
                  alt="LoL Coach" 
                  width={40} 
                  height={40}
                  className="drop-shadow-[0_0_8px_rgba(167,139,250,0.6)]"
                />
              </div>
              <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                LoL Coach
              </h1>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-4">
              <ChampionSearchModal />
              <Button
                variant="ghost"
                onClick={() => router.push('/draft')}
                className="text-sm font-medium hover:bg-primary/10 hover:text-primary"
              >
                <Target className="mr-2 h-4 w-4" />
                Draft
              </Button>
              <Button
                variant="ghost"
                onClick={() => router.push('/live')}
                className="text-sm font-medium hover:bg-accent/10 hover:text-accent"
              >
                <Activity className="mr-2 h-4 w-4" />
                Live Game
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section - Premium Gaming */}
      <section className="relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-accent/5 pointer-events-none" />
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
        
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-primary/20 mb-8">
              <Trophy className="h-4 w-4 text-accent" />
              <span className="text-sm font-medium">90.9% Win Prediction Accuracy</span>
            </div>
            
            <h2 className="text-6xl sm:text-8xl font-extrabold tracking-tight mb-6">
              <span className="block glow-text bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
                AI-Powered
              </span>
              <span className="block text-foreground mt-2">Win Prediction</span>
            </h2>
            
            <p className="text-xl sm:text-2xl text-muted-foreground mb-12 max-w-2xl mx-auto font-normal">
              Dominate the Rift with real-time analytics, champion insights, and intelligent AI recommendations
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                onClick={() => router.push('/draft')}
                className="text-base h-14 px-10 rounded-full bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 shadow-lg shadow-primary/25 relative overflow-hidden group"
              >
                <Zap className="mr-2 h-5 w-5" />
                <span className="relative z-10">Get Started</span>
                <div className="absolute inset-0 shimmer" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => router.push('/live')}
                className="text-base h-14 px-10 rounded-full border-primary/30 hover:border-primary/50 hover:bg-primary/5"
              >
                <Activity className="mr-2 h-5 w-5" />
                Watch Live Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative border-t border-primary/10 bg-card/30 backdrop-blur-sm">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tight mb-4 bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
              Professional Gaming Tools
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Built for champions, powered by AI
            </p>
          </div>

          <Tabs defaultValue="predictor" className="mx-auto max-w-6xl">
            <TabsList className="grid w-full grid-cols-1 md:grid-cols-3 h-auto gap-4 bg-transparent p-0">
              <TabsTrigger
                value="predictor"
                className="data-[state=active]:bg-gradient-to-br data-[state=active]:from-primary/20 data-[state=active]:to-primary/10 data-[state=active]:border-primary/30 data-[state=active]:shadow-lg data-[state=active]:shadow-primary/20 rounded-2xl py-5 border border-transparent hover:border-primary/20 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/20">
                    <Sparkles className="h-5 w-5 text-primary" />
                  </div>
                  <div className="text-left">
                    <div className="font-bold">Win Prediction</div>
                    <div className="text-xs text-muted-foreground">90.9% Accurate</div>
                  </div>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="stats"
                className="data-[state=active]:bg-gradient-to-br data-[state=active]:from-cyan-500/20 data-[state=active]:to-cyan-500/10 data-[state=active]:border-cyan-500/30 data-[state=active]:shadow-lg data-[state=active]:shadow-cyan-500/20 rounded-2xl py-5 border border-transparent hover:border-cyan-500/20 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-cyan-500/20">
                    <Trophy className="h-5 w-5 text-cyan-500" />
                  </div>
                  <div className="text-left">
                    <div className="font-bold">Champion Stats</div>
                    <div className="text-xs text-muted-foreground">Deep Analytics</div>
                  </div>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="items"
                className="data-[state=active]:bg-gradient-to-br data-[state=active]:from-accent/20 data-[state=active]:to-accent/10 data-[state=active]:border-accent/30 data-[state=active]:shadow-lg data-[state=active]:shadow-accent/20 rounded-2xl py-5 border border-transparent hover:border-accent/20 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-accent/20">
                    <Zap className="h-5 w-5 text-accent" />
                  </div>
                  <div className="text-left">
                    <div className="font-bold">AI Item Builds</div>
                    <div className="text-xs text-muted-foreground">Personalized</div>
                  </div>
                </div>
              </TabsTrigger>
            </TabsList>

            <div className="mt-10">
              <TabsContent value="predictor" className="m-0">
                <Card className="luxury-card border-primary/20 shadow-2xl shadow-primary/10 bg-card/80 backdrop-blur-sm">
                  <CardHeader className="border-b border-primary/10">
                    <CardTitle className="text-3xl flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-gradient-to-br from-primary/30 to-primary/10">
                        <Sparkles className="h-6 w-6 text-primary" />
                      </div>
                      Win Prediction Engine
                    </CardTitle>
                    <CardDescription className="text-base text-foreground/70">
                      Get real-time win probability with 90.9% accuracy based on team compositions and matchups
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-8">
                    <ChampionSelectPredictor />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="stats" className="m-0">
                <Card className="luxury-card border-cyan-500/20 shadow-2xl shadow-cyan-500/10 bg-card/80 backdrop-blur-sm">
                  <CardHeader className="border-b border-cyan-500/10">
                    <CardTitle className="text-3xl flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-gradient-to-br from-cyan-500/30 to-cyan-500/10">
                        <Trophy className="h-6 w-6 text-cyan-500" />
                      </div>
                      Champion Analytics
                    </CardTitle>
                    <CardDescription className="text-base text-foreground/70">
                      Explore detailed statistics, win rates, and performance metrics for every champion
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-8">
                    <ChampionStatsExplorer />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="items" className="m-0">
                <Card className="luxury-card border-accent/20 shadow-2xl shadow-accent/10 bg-card/80 backdrop-blur-sm">
                  <CardHeader className="border-b border-accent/10">
                    <CardTitle className="text-3xl flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-gradient-to-br from-accent/30 to-accent/10">
                        <Zap className="h-6 w-6 text-accent" />
                      </div>
                      AI Item Recommendations
                    </CardTitle>
                    <CardDescription className="text-base text-foreground/70">
                      Personalized builds optimized for your matchup, team composition, and game state
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-8">
                    <ItemRecommendations />
                  </CardContent>
                </Card>
              </TabsContent>
            </div>
          </Tabs>
        </div>
      </section>

      {/* Quick Search Section */}
      <section className="relative border-t border-primary/10">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="mx-auto max-w-3xl">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-accent/20 mb-6">
                <Sparkles className="h-4 w-4 text-accent" />
                <span className="text-sm font-medium">Instant Champion Lookup</span>
              </div>
              <h2 className="text-4xl font-bold tracking-tight mb-4 bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
                Quick Champion Search
              </h2>
              <p className="text-muted-foreground text-lg mb-8">
                Access detailed statistics and insights for any champion instantly
              </p>
            </div>
            <div className="stat-card p-8 rounded-2xl">
              <ChampionSearch />
            </div>
          </div>
        </div>
      </section>

      {/* Premium Footer */}
      <footer className="relative border-t border-primary/10 glass">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center space-y-6">
            <div className="flex items-center justify-center gap-3 mb-6">
              <Image 
                src="/logo.svg" 
                alt="LoL Coach" 
                width={32} 
                height={32}
                className="drop-shadow-[0_0_8px_rgba(167,139,250,0.6)]"
              />
              <span className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                LoL Coach
              </span>
            </div>
            
            <div className="max-w-2xl mx-auto space-y-4">
              <p className="text-lg font-medium text-foreground/90">
                Made with passion for the League of Legends community
              </p>
              <div className="flex items-center justify-center gap-8 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-primary" />
                  <span>AI-Powered Analytics</span>
                </div>
                <div className="flex items-center gap-2">
                  <Trophy className="h-4 w-4 text-accent" />
                  <span>90.9% Accuracy</span>
                </div>
                <div className="flex items-center gap-2">
                  <Zap className="h-4 w-4 text-cyan-500" />
                  <span>Real-Time Updates</span>
                </div>
              </div>
              <p className="text-sm text-muted-foreground/70 pt-4 border-t border-primary/10">
                Advanced machine learning models trained on 360,000+ ranked matches
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
