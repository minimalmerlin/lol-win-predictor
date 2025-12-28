'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ArrowLeft, Activity, TrendingUp, Clock, Trophy, Zap, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { getChampionImageUrl } from '@/lib/riot-data';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface LivePrediction {
  game_time: number;
  game_time_formatted: string;
  blue_team: {
    champions: string[];
    kills: number;
    deaths: number;
    gold: number;
    towers: number;
  };
  red_team: {
    champions: string[];
    kills: number;
    deaths: number;
    gold: number;
    towers: number;
  };
  predictions: {
    champion_matchup: {
      blue_win_probability: number;
      red_win_probability: number;
      confidence: string;
    };
    game_state: {
      message?: string;
      blue_win_probability?: number;
      red_win_probability?: number;
    };
  };
  recommendation: string;
}

export default function LiveGamePage() {
  const router = useRouter();
  const [gameRunning, setGameRunning] = useState(false);
  const [prediction, setPrediction] = useState<LivePrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const checkGameStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/live/status`);
      if (response.ok) {
        const data = await response.json();
        setGameRunning(data.is_running);
        return data.is_running;
      }
      return false;
    } catch (err) {
      console.error('Failed to check game status:', err);
      return false;
    }
  };

  const fetchLivePrediction = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/api/live/predict`);

      if (response.status === 404) {
        setGameRunning(false);
        setPrediction(null);
        setError('No game is currently running');
        return;
      }

      if (response.ok) {
        const data = await response.json();
        setPrediction(data);
        setGameRunning(true);
      } else {
        throw new Error('Failed to fetch prediction');
      }
    } catch (err) {
      console.error('Error fetching live prediction:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Initial check
  useEffect(() => {
    checkGameStatus().then(isRunning => {
      if (isRunning) {
        fetchLivePrediction();
      } else {
        setLoading(false);
      }
    });
  }, []);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh || !gameRunning) return;

    const interval = setInterval(() => {
      fetchLivePrediction();
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [autoRefresh, gameRunning]);

  const getWinRateColor = (probability: number) => {
    if (probability >= 0.65) return 'text-green-400';
    if (probability >= 0.50) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getWinRateBg = (probability: number) => {
    if (probability >= 0.65) return 'bg-green-500/20 border-green-500/50';
    if (probability >= 0.50) return 'bg-yellow-500/20 border-yellow-500/50';
    return 'bg-red-500/20 border-red-500/50';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-green-950">
      {/* Header */}
      <header className="border-b border-green-800/30 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Button
              variant="ghost"
              onClick={() => router.push('/')}
              className="text-slate-300 hover:text-white"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>

            <div className="flex items-center gap-2">
              <Activity className="h-6 w-6 text-green-400" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
                Live Game Tracker
              </h1>
              {gameRunning && (
                <Badge className="bg-green-600 animate-pulse">
                  <span className="w-2 h-2 bg-white rounded-full mr-2 inline-block"></span>
                  LIVE
                </Badge>
              )}
            </div>

            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={autoRefresh ? 'border-green-600/50 text-green-400' : 'border-slate-600'}
              >
                Auto-Refresh: {autoRefresh ? 'ON' : 'OFF'}
              </Button>
              <Button
                variant="outline"
                onClick={fetchLivePrediction}
                disabled={loading || !gameRunning}
                className="border-blue-600/50 text-blue-400 hover:bg-blue-900/20"
              >
                Refresh Now
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* No Game Running */}
        {!gameRunning && !loading && (
          <Card className="bg-slate-800/50 border-yellow-600/30 max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-yellow-400">
                <AlertCircle className="h-6 w-6" />
                No Game Detected
              </CardTitle>
              <CardDescription>Start a League of Legends game to enable live tracking</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-slate-700/50 rounded-lg">
                <h3 className="font-medium text-white mb-2">How it works:</h3>
                <ol className="list-decimal list-inside space-y-2 text-slate-300 text-sm">
                  <li>Start any League of Legends game (Practice, Custom, or Normal)</li>
                  <li>This page will automatically detect when the game starts</li>
                  <li>Real-time win predictions will update every 30 seconds</li>
                  <li>Get strategic recommendations based on current game state</li>
                </ol>
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={fetchLivePrediction}
                  className="flex-1 bg-green-600 hover:bg-green-700"
                >
                  Check for Game
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Loading */}
        {loading && (
          <div className="text-center py-12">
            <Activity className="h-16 w-16 mx-auto mb-4 text-green-400 animate-spin" />
            <p className="text-slate-400">Connecting to game...</p>
          </div>
        )}

        {/* Live Prediction */}
        {gameRunning && prediction && !loading && (
          <div className="space-y-6">
            {/* Game Time & Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="bg-slate-800/50 border-cyan-600/30">
                <CardHeader className="pb-3">
                  <CardDescription className="text-cyan-200 flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    Game Time
                  </CardDescription>
                  <CardTitle className="text-3xl text-white">{prediction.game_time_formatted}</CardTitle>
                </CardHeader>
              </Card>

              <Card className="bg-slate-800/50 border-blue-600/30">
                <CardHeader className="pb-3">
                  <CardDescription className="text-blue-200">Blue Gold</CardDescription>
                  <CardTitle className="text-2xl text-white">{(prediction.blue_team.gold / 1000).toFixed(1)}k</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-slate-400">
                  {prediction.blue_team.kills}K / {prediction.blue_team.deaths}D
                </CardContent>
              </Card>

              <Card className="bg-slate-800/50 border-red-600/30">
                <CardHeader className="pb-3">
                  <CardDescription className="text-red-200">Red Gold</CardDescription>
                  <CardTitle className="text-2xl text-white">{(prediction.red_team.gold / 1000).toFixed(1)}k</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-slate-400">
                  {prediction.red_team.kills}K / {prediction.red_team.deaths}D
                </CardContent>
              </Card>

              <Card className="bg-slate-800/50 border-purple-600/30">
                <CardHeader className="pb-3">
                  <CardDescription className="text-purple-200 flex items-center gap-2">
                    <Trophy className="h-4 w-4" />
                    Gold Diff
                  </CardDescription>
                  <CardTitle className={`text-2xl ${prediction.blue_team.gold > prediction.red_team.gold ? 'text-blue-400' : 'text-red-400'}`}>
                    {prediction.blue_team.gold > prediction.red_team.gold ? '+' : ''}{((prediction.blue_team.gold - prediction.red_team.gold) / 1000).toFixed(1)}k
                  </CardTitle>
                </CardHeader>
              </Card>
            </div>

            {/* Teams */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Blue Team */}
              <Card className="bg-slate-800/50 border-blue-600/30">
                <CardHeader>
                  <CardTitle className="text-blue-400">Blue Team (Your Team)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {prediction.blue_team.champions.map((champ, idx) => (
                      <div key={idx} className="flex items-center gap-3 p-2 bg-blue-900/20 rounded-lg border border-blue-500/30">
                        <div className="relative w-10 h-10 rounded-full overflow-hidden border-2 border-blue-500">
                          <Image
                            src={getChampionImageUrl(champ)}
                            alt={champ}
                            fill
                            className="object-cover"
                            unoptimized
                          />
                        </div>
                        <span className="font-medium text-white">{champ}</span>
                      </div>
                    ))}
                  </div>

                  <Separator className="my-4 bg-slate-700" />

                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">Kills</div>
                      <div className="text-white font-bold">{prediction.blue_team.kills}</div>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">Deaths</div>
                      <div className="text-white font-bold">{prediction.blue_team.deaths}</div>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">Towers</div>
                      <div className="text-white font-bold">{prediction.blue_team.towers}</div>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">KDA</div>
                      <div className="text-white font-bold">
                        {prediction.blue_team.deaths > 0
                          ? (prediction.blue_team.kills / prediction.blue_team.deaths).toFixed(2)
                          : prediction.blue_team.kills.toFixed(2)}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Red Team */}
              <Card className="bg-slate-800/50 border-red-600/30">
                <CardHeader>
                  <CardTitle className="text-red-400">Red Team (Enemy)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {prediction.red_team.champions.map((champ, idx) => (
                      <div key={idx} className="flex items-center gap-3 p-2 bg-red-900/20 rounded-lg border border-red-500/30">
                        <div className="relative w-10 h-10 rounded-full overflow-hidden border-2 border-red-500">
                          <Image
                            src={getChampionImageUrl(champ)}
                            alt={champ}
                            fill
                            className="object-cover"
                            unoptimized
                          />
                        </div>
                        <span className="font-medium text-white">{champ}</span>
                      </div>
                    ))}
                  </div>

                  <Separator className="my-4 bg-slate-700" />

                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">Kills</div>
                      <div className="text-white font-bold">{prediction.red_team.kills}</div>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">Deaths</div>
                      <div className="text-white font-bold">{prediction.red_team.deaths}</div>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">Towers</div>
                      <div className="text-white font-bold">{prediction.red_team.towers}</div>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <div className="text-slate-400">KDA</div>
                      <div className="text-white font-bold">
                        {prediction.red_team.deaths > 0
                          ? (prediction.red_team.kills / prediction.red_team.deaths).toFixed(2)
                          : prediction.red_team.kills.toFixed(2)}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Predictions */}
            <Card className="bg-slate-800/50 border-purple-600/30">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-purple-400">
                  <TrendingUp className="h-5 w-5" />
                  AI Win Prediction
                </CardTitle>
                <CardDescription>Real-time analysis based on game state</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Champion Matchup Prediction */}
                <div>
                  <h3 className="text-sm font-medium text-slate-400 mb-3">Champion Matchup (Pre-Game)</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className={`p-4 rounded-lg border-2 ${getWinRateBg(prediction.predictions.champion_matchup.blue_win_probability)}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-blue-400 font-medium">Blue Team</span>
                        <span className={`text-3xl font-bold ${getWinRateColor(prediction.predictions.champion_matchup.blue_win_probability)}`}>
                          {(prediction.predictions.champion_matchup.blue_win_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-3">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-cyan-500 h-3 rounded-full transition-all"
                          style={{ width: `${prediction.predictions.champion_matchup.blue_win_probability * 100}%` }}
                        />
                      </div>
                    </div>

                    <div className={`p-4 rounded-lg border-2 ${getWinRateBg(prediction.predictions.champion_matchup.red_win_probability)}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-red-400 font-medium">Red Team</span>
                        <span className={`text-3xl font-bold ${getWinRateColor(prediction.predictions.champion_matchup.red_win_probability)}`}>
                          {(prediction.predictions.champion_matchup.red_win_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-3">
                        <div
                          className="bg-gradient-to-r from-red-500 to-orange-500 h-3 rounded-full transition-all"
                          style={{ width: `${prediction.predictions.champion_matchup.red_win_probability * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Game State Prediction */}
                {prediction.predictions.game_state.blue_win_probability !== undefined && (
                  <div>
                    <Separator className="bg-slate-700 mb-4" />
                    <h3 className="text-sm font-medium text-slate-400 mb-3 flex items-center gap-2">
                      <Zap className="h-4 w-4 text-yellow-400" />
                      Current Game State Prediction
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className={`p-4 rounded-lg border-2 ${getWinRateBg(prediction.predictions.game_state.blue_win_probability!)}`}>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-blue-400 font-medium">Blue Win %</span>
                          <span className={`text-4xl font-bold ${getWinRateColor(prediction.predictions.game_state.blue_win_probability!)}`}>
                            {(prediction.predictions.game_state.blue_win_probability! * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-4">
                          <div
                            className="bg-gradient-to-r from-blue-500 to-cyan-500 h-4 rounded-full transition-all"
                            style={{ width: `${prediction.predictions.game_state.blue_win_probability! * 100}%` }}
                          />
                        </div>
                      </div>

                      <div className={`p-4 rounded-lg border-2 ${getWinRateBg(prediction.predictions.game_state.red_win_probability!)}`}>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-red-400 font-medium">Red Win %</span>
                          <span className={`text-4xl font-bold ${getWinRateColor(prediction.predictions.game_state.red_win_probability!)}`}>
                            {(prediction.predictions.game_state.red_win_probability! * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-4">
                          <div
                            className="bg-gradient-to-r from-red-500 to-orange-500 h-4 rounded-full transition-all"
                            style={{ width: `${prediction.predictions.game_state.red_win_probability! * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {prediction.predictions.game_state.message && (
                  <div className="p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg text-sm text-yellow-200">
                    {prediction.predictions.game_state.message}
                  </div>
                )}

                {/* Recommendation */}
                <div className="p-4 bg-gradient-to-r from-purple-900/30 to-blue-900/30 border-2 border-purple-500/30 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Zap className="h-5 w-5 text-purple-400 mt-0.5 flex-shrink-0" />
                    <div>
                      <h3 className="font-medium text-purple-300 mb-1">Strategic Recommendation</h3>
                      <p className="text-slate-200">{prediction.recommendation}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
