'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import ChampionSelectPredictor from '@/components/ChampionSelectPredictor';
import ChampionStatsExplorer from '@/components/ChampionStatsExplorer';
import ItemRecommendations from '@/components/ItemRecommendations';
import ChampionSearch from '@/components/ChampionSearch';
import { useRouter } from 'next/navigation';
import { Target, Activity } from 'lucide-react';

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Hero Section */}
      <header className="relative z-50 border-b border-blue-800/30 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
                <span className="text-2xl">🎮</span>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">
                  LoL Intelligent Coach
                </h1>
                <p className="text-blue-200">
                  AI-Powered Win Prediction & Champion Analysis
                </p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-4">
              <Button
                variant="outline"
                onClick={() => router.push('/draft')}
                className="border-purple-600/50 text-purple-400 hover:bg-purple-900/20"
              >
                <Target className="mr-2 h-4 w-4" />
                Draft Assistant
              </Button>
              <Button
                variant="outline"
                onClick={() => router.push('/live')}
                className="border-green-600/50 text-green-400 hover:bg-green-900/20"
              >
                <Activity className="mr-2 h-4 w-4" />
                Live Game
              </Button>
              <ChampionSearch />
            </div>
          </div>
          {/* Mobile Search */}
          <div className="md:hidden mt-4 space-y-2">
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => router.push('/draft')}
                className="flex-1 border-purple-600/50 text-purple-400 hover:bg-purple-900/20"
              >
                <Target className="mr-2 h-4 w-4" />
                Draft
              </Button>
              <Button
                variant="outline"
                onClick={() => router.push('/live')}
                className="flex-1 border-green-600/50 text-green-400 hover:bg-green-900/20"
              >
                <Activity className="mr-2 h-4 w-4" />
                Live
              </Button>
            </div>
            <ChampionSearch />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-blue-200">Model Accuracy</CardDescription>
              <CardTitle className="text-3xl text-white">90.9%</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-400">Win Prediction Model</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-blue-200">Champions Analyzed</CardDescription>
              <CardTitle className="text-3xl text-white">139</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-400">From 51k+ Games</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-blue-200">Matches Analyzed</CardDescription>
              <CardTitle className="text-3xl text-white">360k+</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-400">High-Elo Matches</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="champion-select" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-slate-800/50 border border-blue-700/30">
            <TabsTrigger
              value="champion-select"
              className="data-[state=active]:bg-blue-600 data-[state=active]:text-white"
            >
              🎯 Champion Select
            </TabsTrigger>
            <TabsTrigger
              value="stats"
              className="data-[state=active]:bg-blue-600 data-[state=active]:text-white"
            >
              📊 Champion Stats
            </TabsTrigger>
            <TabsTrigger
              value="items"
              className="data-[state=active]:bg-blue-600 data-[state=active]:text-white"
            >
              🛡️ Item Builds
            </TabsTrigger>
          </TabsList>

          <TabsContent value="champion-select" className="space-y-4">
            <ChampionSelectPredictor />
          </TabsContent>

          <TabsContent value="stats" className="space-y-4">
            <ChampionStatsExplorer />
          </TabsContent>

          <TabsContent value="items" className="space-y-4">
            <ItemRecommendations />
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t border-blue-800/30 bg-slate-900/50 backdrop-blur-sm mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-slate-400">
          <p>Built with ❤️ using Next.js, FastAPI, and Machine Learning</p>
          <p className="mt-2">
            <span className="text-blue-400">Model:</span> Random Forest (90.9% Accuracy, ROC-AUC: 0.982) |
            <span className="text-blue-400"> Training Data:</span> 360,188 Matches
          </p>
        </div>
      </footer>
    </div>
  );
}
