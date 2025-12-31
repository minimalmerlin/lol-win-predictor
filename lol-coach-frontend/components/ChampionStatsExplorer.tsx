'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { api, type Champion } from '@/lib/api';
import { ExternalLink } from 'lucide-react';
import { getChampionImageUrl } from '@/lib/riot-data';

export default function ChampionStatsExplorer() {
  const router = useRouter();
  const [champions, setChampions] = useState<Champion[]>([]);
  const [filteredChampions, setFilteredChampions] = useState<Champion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [minGames, setMinGames] = useState(20);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getChampionStats({
          min_games: minGames,
          sort_by: 'win_rate',
          limit: 100,
        });

        if (data && data.champions && Array.isArray(data.champions)) {
          setChampions(data.champions);
          setFilteredChampions(data.champions);
        } else {
          throw new Error('Invalid data format received');
        }
      } catch (err) {
        console.error('Champion stats error:', err);
        setError('Keine Champion-Daten verfügbar');
        setChampions([]);
        setFilteredChampions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [minGames]);

  useEffect(() => {
    if (searchTerm) {
      const filtered = champions.filter((champ) =>
        champ.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredChampions(filtered);
    } else {
      setFilteredChampions(champions);
    }
  }, [searchTerm, champions]);

  const getWinRateColor = (winRate: number) => {
    if (winRate >= 0.6) return 'text-green-400';
    if (winRate >= 0.5) return 'text-blue-400';
    return 'text-red-400';
  };

  const getWinRateBadgeColor = (winRate: number) => {
    if (winRate >= 0.6) return 'bg-green-600';
    if (winRate >= 0.5) return 'bg-blue-600';
    return 'bg-red-600';
  };

  if (loading) {
    return (
      <div className="glass-card p-6">
        <div className="text-center text-muted-foreground">Lade Champion-Statistiken...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card p-6 border-destructive/50">
        <div className="text-center text-destructive">{error}</div>
        <div className="text-center text-muted-foreground text-sm mt-2">
          Bitte stelle sicher, dass die API erreichbar ist.
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
        <CardHeader>
          <CardTitle className="text-white">🔍 Filter Champions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-slate-400 mb-2 block">Search Champion</label>
              <Input
                placeholder="Search by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400"
              />
            </div>
            <div>
              <label className="text-sm text-slate-400 mb-2 block">Minimum Games</label>
              <Input
                type="number"
                min="1"
                value={minGames}
                onChange={(e) => setMinGames(Number(e.target.value))}
                className="bg-slate-700/50 border-slate-600 text-white"
              />
            </div>
          </div>

          <div className="text-sm text-slate-400">
            Showing {filteredChampions.length} of {champions.length} champions
          </div>
        </CardContent>
      </Card>

      {/* Stats Table */}
      <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
        <CardHeader>
          <CardTitle className="text-white">📊 Champion Statistics</CardTitle>
          <CardDescription className="text-slate-400">
            Sorted by win rate (minimum {minGames} games)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {/* Header */}
            <div className="grid grid-cols-5 gap-4 pb-3 border-b border-slate-700 text-sm font-medium text-slate-400">
              <div>Champion</div>
              <div className="text-center">Games</div>
              <div className="text-center">Wins</div>
              <div className="text-center">Losses</div>
              <div className="text-center">Win Rate</div>
            </div>

            {/* Rows */}
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {filteredChampions.map((champ, index) => (
                <div
                  key={champ.name}
                  className="grid grid-cols-5 gap-4 p-3 rounded-lg hover:bg-slate-700/30 transition-colors cursor-pointer group"
                  onClick={() => router.push(`/champions/${champ.name}`)}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-slate-500 text-sm">#{index + 1}</span>
                    <div className="relative w-8 h-8 rounded-full overflow-hidden border border-slate-600 group-hover:border-blue-500 transition-colors flex-shrink-0">
                      <Image
                        src={getChampionImageUrl(champ.name)}
                        alt={champ.name}
                        fill
                        className="object-cover"
                        unoptimized
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.src = `https://via.placeholder.com/32x32/1e293b/60a5fa?text=${champ.name.substring(0, 2)}`;
                        }}
                      />
                    </div>
                    <span className="text-white font-medium group-hover:text-blue-400 transition-colors flex items-center gap-1">
                      {champ.name}
                      <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </span>
                  </div>
                  <div className="text-center text-slate-300">{champ.games}</div>
                  <div className="text-center text-green-400">{champ.wins}</div>
                  <div className="text-center text-red-400">{champ.losses}</div>
                  <div className="flex justify-center">
                    <Badge className={`${getWinRateBadgeColor(champ.win_rate)} text-white`}>
                      {(champ.win_rate * 100).toFixed(1)}%
                    </Badge>
                  </div>
                </div>
              ))}
            </div>

            {filteredChampions.length === 0 && (
              <div className="text-center py-8 text-slate-400">
                No champions found matching your criteria
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Top Performers */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card className="bg-gradient-to-br from-green-900/20 to-green-800/10 border-green-700/30">
          <CardHeader className="pb-3">
            <CardTitle className="text-green-400 text-lg">🥇 Highest Win Rate</CardTitle>
          </CardHeader>
          <CardContent>
            {filteredChampions[0] && (
              <div>
                <div className="text-2xl font-bold text-white">{filteredChampions[0].name}</div>
                <div className="text-3xl font-bold text-green-400 mt-1">
                  {(filteredChampions[0].win_rate * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-slate-400 mt-2">
                  {filteredChampions[0].games} games
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-900/20 to-blue-800/10 border-blue-700/30">
          <CardHeader className="pb-3">
            <CardTitle className="text-blue-400 text-lg">📈 Most Played</CardTitle>
          </CardHeader>
          <CardContent>
            {champions.sort((a, b) => b.games - a.games)[0] && (
              <div>
                <div className="text-2xl font-bold text-white">
                  {champions.sort((a, b) => b.games - a.games)[0].name}
                </div>
                <div className="text-3xl font-bold text-blue-400 mt-1">
                  {champions.sort((a, b) => b.games - a.games)[0].games}
                </div>
                <div className="text-sm text-slate-400 mt-2">games played</div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-900/20 to-purple-800/10 border-purple-700/30">
          <CardHeader className="pb-3">
            <CardTitle className="text-purple-400 text-lg">🏆 Most Wins</CardTitle>
          </CardHeader>
          <CardContent>
            {champions.sort((a, b) => b.wins - a.wins)[0] && (
              <div>
                <div className="text-2xl font-bold text-white">
                  {champions.sort((a, b) => b.wins - a.wins)[0].name}
                </div>
                <div className="text-3xl font-bold text-purple-400 mt-1">
                  {champions.sort((a, b) => b.wins - a.wins)[0].wins}
                </div>
                <div className="text-sm text-slate-400 mt-2">total wins</div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
