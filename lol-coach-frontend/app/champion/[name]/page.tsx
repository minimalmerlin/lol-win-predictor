'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import { ArrowLeft, TrendingUp, Users, ShoppingBag, Trophy } from 'lucide-react';
import {
  getChampionImageUrl,
  getChampionSplashUrl,
  getItemImageUrl,
  getItemNameSync
} from '@/lib/riot-data';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface ChampionStats {
  games: number;
  wins: number;
  losses: number;
  win_rate: number;
  picks: number;
  bans: number;
}

interface ItemBuild {
  items: number[];
  games: number;
  wins: number;
  losses: number;
  win_rate: number;
  pick_rate: number;
}

interface Teammate {
  teammate: string;
  games: number;
  winrate: number;
  synergy_lift: number;
  synergy_score: number;
}

interface ChampionData {
  champion: string;
  match_quality: number;
  exact_match: boolean;
  stats: ChampionStats;
  item_builds: {
    champion: string;
    found: boolean;
    total_games: number;
    top_builds: ItemBuild[];
    all_builds_count: number;
  };
  best_teammates: Teammate[];
  has_synergy_data: boolean;
}

export default function ChampionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const championName = params.name as string;

  const [data, setData] = useState<ChampionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChampionData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_URL}/api/champions/${championName}`);

        if (!response.ok) {
          throw new Error('Champion not found');
        }

        const result = await response.json();

        // Sort item builds by win rate (descending)
        if (result.item_builds?.top_builds) {
          result.item_builds.top_builds.sort((a: ItemBuild, b: ItemBuild) =>
            b.win_rate - a.win_rate
          );
        }

        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load champion data');
      } finally {
        setLoading(false);
      }
    };

    if (championName) {
      fetchChampionData();
    }
  }, [championName]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-2xl">Loading champion data...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <Card className="bg-slate-800/50 border-red-700/30 backdrop-blur max-w-md">
          <CardHeader>
            <CardTitle className="text-red-400">Error</CardTitle>
            <CardDescription className="text-slate-300">{error || 'Champion not found'}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/')} className="w-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const stats = data.stats;
  const hasStats = stats && stats.games > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-blue-800/30 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => router.push('/')}
              className="text-blue-200 hover:text-white"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
            <Separator orientation="vertical" className="h-8" />
            <div className="relative w-16 h-16 rounded-full overflow-hidden border-2 border-blue-500">
              <Image
                src={getChampionImageUrl(data.champion)}
                alt={data.champion}
                fill
                className="object-cover"
                unoptimized
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.src = `https://via.placeholder.com/64x64/1e293b/60a5fa?text=${data.champion.substring(0, 2)}`;
                }}
              />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                {data.champion}
                {!data.exact_match && (
                  <Badge variant="outline" className="text-yellow-400 border-yellow-400">
                    Fuzzy Match
                  </Badge>
                )}
              </h1>
              <p className="text-blue-200">
                Detailed Statistics & Analysis
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Stats Overview */}
          <div className="lg:col-span-3">
            <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                  <Trophy className="h-5 w-5 text-yellow-400" />
                  Champion Statistics
                </CardTitle>
                <CardDescription className="text-blue-200">
                  {hasStats ? `Based on ${stats.games.toLocaleString()} games from 51k+ matches` : 'No stats available'}
                </CardDescription>
              </CardHeader>
              {hasStats && (
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-white">{stats.games.toLocaleString()}</div>
                      <div className="text-sm text-slate-400">Games Played</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-400">
                        {(stats.win_rate * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-slate-400">Win Rate</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-400">{stats.picks.toLocaleString()}</div>
                      <div className="text-sm text-slate-400">Total Picks</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-red-400">{stats.bans.toLocaleString()}</div>
                      <div className="text-sm text-slate-400">Total Bans</div>
                    </div>
                  </div>
                  <Separator className="my-4" />
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Wins:</span>
                      <span className="text-green-400 font-semibold">{stats.wins.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Losses:</span>
                      <span className="text-red-400 font-semibold">{stats.losses.toLocaleString()}</span>
                    </div>
                  </div>
                </CardContent>
              )}
            </Card>
          </div>

          {/* Item Builds */}
          <div className="lg:col-span-2">
            <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                  <ShoppingBag className="h-5 w-5 text-purple-400" />
                  Item Builds
                </CardTitle>
                <CardDescription className="text-blue-200">
                  {data.item_builds.found
                    ? `Top builds from ${data.item_builds.total_games} games`
                    : 'No item build data available'}
                </CardDescription>
              </CardHeader>
              {data.item_builds.found && data.item_builds.top_builds.length > 0 && (
                <CardContent>
                  <div className="space-y-4">
                    {data.item_builds.top_builds.map((build, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-lg bg-slate-700/30 border border-slate-600/30 hover:border-blue-500/50 transition-colors"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <Badge className="bg-blue-600">Build {idx + 1}</Badge>
                            <span className="text-sm text-slate-300">
                              {build.games} games
                            </span>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold text-green-400">
                              {(build.win_rate * 100).toFixed(1)}%
                            </div>
                            <div className="text-xs text-slate-400">Win Rate</div>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {build.items.map((itemId, itemIdx) => (
                            <div
                              key={itemIdx}
                              className="relative group"
                              title={getItemNameSync(itemId)}
                            >
                              <div className="w-12 h-12 rounded border-2 border-slate-600 overflow-hidden hover:border-blue-500 transition-colors">
                                <Image
                                  src={getItemImageUrl(itemId)}
                                  alt={getItemNameSync(itemId)}
                                  width={48}
                                  height={48}
                                  className="object-cover"
                                  unoptimized
                                  onError={(e) => {
                                    const target = e.target as HTMLImageElement;
                                    target.src = `https://via.placeholder.com/48x48/334155/94a3b8?text=${itemId}`;
                                  }}
                                />
                              </div>
                              {/* Tooltip */}
                              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-slate-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                                {getItemNameSync(itemId)}
                              </div>
                            </div>
                          ))}
                        </div>
                        <div className="mt-2 text-xs text-slate-400 flex gap-4">
                          <span>{build.wins} wins</span>
                          <span>{build.losses} losses</span>
                          <span>{(build.pick_rate * 100).toFixed(1)}% pick rate</span>
                        </div>
                      </div>
                    ))}
                  </div>
                  {data.item_builds.all_builds_count > data.item_builds.top_builds.length && (
                    <div className="mt-4 text-center text-sm text-slate-400">
                      Showing top {data.item_builds.top_builds.length} of {data.item_builds.all_builds_count} builds
                    </div>
                  )}
                </CardContent>
              )}
            </Card>
          </div>

          {/* Best Teammates */}
          <div className="lg:col-span-1">
            <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                  <Users className="h-5 w-5 text-cyan-400" />
                  Best Teammates
                </CardTitle>
                <CardDescription className="text-blue-200">
                  {data.has_synergy_data
                    ? 'Champions with best synergy'
                    : 'No synergy data available'}
                </CardDescription>
              </CardHeader>
              {data.has_synergy_data && data.best_teammates.length > 0 && (
                <CardContent>
                  <div className="space-y-3">
                    {data.best_teammates.map((teammate, idx) => (
                      <div
                        key={idx}
                        className="p-3 rounded-lg bg-slate-700/30 border border-slate-600/30 hover:border-cyan-500/50 transition-colors cursor-pointer group"
                        onClick={() => router.push(`/champion/${teammate.teammate}`)}
                      >
                        <div className="flex items-center gap-3">
                          <div className="relative w-12 h-12 rounded-full overflow-hidden border-2 border-slate-600 group-hover:border-cyan-500 transition-colors flex-shrink-0">
                            <Image
                              src={getChampionImageUrl(teammate.teammate)}
                              alt={teammate.teammate}
                              fill
                              className="object-cover"
                              unoptimized
                              onError={(e) => {
                                const target = e.target as HTMLImageElement;
                                target.src = `https://via.placeholder.com/48x48/1e293b/60a5fa?text=${teammate.teammate.substring(0, 2)}`;
                              }}
                            />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="font-semibold text-white group-hover:text-cyan-400 transition-colors truncate">
                              {teammate.teammate}
                            </div>
                            <div className="text-xs text-slate-400">{teammate.games} games together</div>
                          </div>
                          <div className="text-right flex-shrink-0">
                            <div className="flex items-center gap-1 text-green-400 font-semibold">
                              <TrendingUp className="h-4 w-4" />
                              {(teammate.synergy_lift * 100).toFixed(1)}%
                            </div>
                            <div className="text-xs text-slate-400">
                              {(teammate.winrate * 100).toFixed(1)}% WR
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              )}
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
