'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import ChampionSelectPredictor from '@/components/ChampionSelectPredictor';
import ChampionStatsExplorer from '@/components/ChampionStatsExplorer';
import ItemRecommendations from '@/components/ItemRecommendations';
import ChampionSearch from '@/components/ChampionSearch';
import { useRouter } from 'next/navigation';
import { Target, Activity, Sparkles } from 'lucide-react';
import Image from 'next/image';

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-white dark:bg-black">
      {/* Apple-style Header */}
      <header className="sticky top-0 z-50 border-b border-border/40 bg-white/80 dark:bg-black/80 backdrop-blur-xl supports-[backdrop-filter]:bg-white/60 dark:supports-[backdrop-filter]:bg-black/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="relative w-10 h-10 flex items-center justify-center">
                <Image 
                  src="/logo.svg" 
                  alt="LoL Coach" 
                  width={40} 
                  height={40}
                  className="dark:invert"
                />
              </div>
              <h1 className="text-xl font-semibold tracking-tight">
                LoL Coach
              </h1>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              <Button
                variant="ghost"
                onClick={() => router.push('/draft')}
                className="text-sm font-medium"
              >
                <Target className="mr-2 h-4 w-4" />
                Draft
              </Button>
              <Button
                variant="ghost"
                onClick={() => router.push('/live')}
                className="text-sm font-medium"
              >
                <Activity className="mr-2 h-4 w-4" />
                Live Game
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section - Apple Style */}
      <section className="relative overflow-hidden">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-32">
          <div className="mx-auto max-w-4xl text-center">
            <h2 className="text-5xl sm:text-7xl font-bold tracking-tight mb-6">
              AI-Powered Win
              <br />
              <span className="bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400 bg-clip-text text-transparent">
                Prediction
              </span>
            </h2>
            <p className="text-xl sm:text-2xl text-muted-foreground mb-12 max-w-2xl mx-auto font-normal">
              Real-time analytics, champion insights, and intelligent recommendations for League of Legends
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                onClick={() => router.push('/draft')}
                className="text-base h-12 px-8 rounded-full"
              >
                Get Started
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => router.push('/live')}
                className="text-base h-12 px-8 rounded-full"
              >
                Watch Live Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-border bg-secondary/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <Tabs defaultValue="predictor" className="mx-auto max-w-6xl">
            <TabsList className="grid w-full grid-cols-1 md:grid-cols-3 h-auto gap-2 bg-transparent p-0">
              <TabsTrigger
                value="predictor"
                className="data-[state=active]:bg-card data-[state=active]:shadow-sm rounded-xl py-4"
              >
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" />
                  <span>Win Prediction</span>
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="stats"
                className="data-[state=active]:bg-card data-[state=active]:shadow-sm rounded-xl py-4"
              >
                Champion Stats
              </TabsTrigger>
              <TabsTrigger
                value="items"
                className="data-[state=active]:bg-card data-[state=active]:shadow-sm rounded-xl py-4"
              >
                Item Builds
              </TabsTrigger>
            </TabsList>

            <div className="mt-8">
              <TabsContent value="predictor" className="m-0">
                <Card className="border-border/50 shadow-sm card-hover">
                  <CardHeader>
                    <CardTitle className="text-2xl">Win Prediction</CardTitle>
                    <CardDescription className="text-base">
                      Get real-time win probability based on team compositions
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ChampionSelectPredictor />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="stats" className="m-0">
                <Card className="border-border/50 shadow-sm card-hover">
                  <CardHeader>
                    <CardTitle className="text-2xl">Champion Analytics</CardTitle>
                    <CardDescription className="text-base">
                      Explore detailed statistics and performance metrics
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ChampionStatsExplorer />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="items" className="m-0">
                <Card className="border-border/50 shadow-sm card-hover">
                  <CardHeader>
                    <CardTitle className="text-2xl">AI Item Recommendations</CardTitle>
                    <CardDescription className="text-base">
                      Personalized builds based on matchup and game state
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ItemRecommendations />
                  </CardContent>
                </Card>
              </TabsContent>
            </div>
          </Tabs>
        </div>
      </section>

      {/* Quick Search Section */}
      <section className="border-t border-border">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="text-3xl font-bold tracking-tight mb-4">
              Quick Champion Lookup
            </h2>
            <p className="text-muted-foreground text-lg mb-8">
              Search for any champion to view detailed statistics and insights
            </p>
            <ChampionSearch />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-secondary/20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center text-sm text-muted-foreground">
            <p>Made for the League of Legends community</p>
            <p className="mt-2">Powered by AI and machine learning</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
