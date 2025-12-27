'use client';

import { useState } from 'react';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { api, type ItemRecommendationResponse } from '@/lib/api';
import { getItemData } from '@/lib/items';
import ChampionCombobox from './ChampionCombobox';

export default function ItemRecommendations() {
  const [selectedChampion, setSelectedChampion] = useState<string | null>(null);
  const [enemyTeam, setEnemyTeam] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<ItemRecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSelectChampion = (champion: string) => {
    setSelectedChampion(champion);
  };

  const handleAddEnemy = (champion: string) => {
    if (!enemyTeam.includes(champion) && enemyTeam.length < 5) {
      setEnemyTeam([...enemyTeam, champion]);
    }
  };

  const handleRemoveEnemy = (champion: string) => {
    setEnemyTeam(enemyTeam.filter((c) => c !== champion));
  };

  const handleGetRecommendations = async () => {
    if (!selectedChampion) {
      setError('Please select your champion first');
      return;
    }

    if (enemyTeam.length === 0) {
      setError('Please select at least one enemy champion');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await api.getItemRecommendations(selectedChampion, enemyTeam, 5);
      setRecommendations(result);
    } catch (err) {
      setError('Failed to get item recommendations. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedChampion(null);
    setEnemyTeam([]);
    setRecommendations(null);
    setError(null);
  };

  return (
    <div className="space-y-6">
      {/* Selection */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Your Champion */}
        <Card className="bg-slate-800/50 border-blue-500/30 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-blue-400">⚔️ Your Champion</CardTitle>
            <CardDescription className="text-slate-400">Select your champion</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ChampionCombobox
              onSelect={handleSelectChampion}
              disabled={selectedChampion !== null}
            />

            {selectedChampion && (
              <div className="flex items-center justify-between p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
                <span className="text-xl font-bold text-white">{selectedChampion}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedChampion(null)}
                  className="text-slate-400 hover:text-white"
                >
                  Change
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Enemy Team */}
        <Card className="bg-slate-800/50 border-red-500/30 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-red-400">🛡️ Enemy Team</CardTitle>
            <CardDescription className="text-slate-400">
              Select enemy champions (optional)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ChampionCombobox onSelect={handleAddEnemy} disabled={enemyTeam.length >= 5} />

            <div className="flex flex-wrap gap-2">
              {enemyTeam.map((champ) => (
                <Badge
                  key={champ}
                  variant="secondary"
                  className="bg-red-600 text-white px-3 py-1 cursor-pointer hover:bg-red-700"
                  onClick={() => handleRemoveEnemy(champ)}
                >
                  {champ} ×
                </Badge>
              ))}
            </div>

            <div className="text-sm text-slate-400">{enemyTeam.length}/5 enemies selected</div>
          </CardContent>
        </Card>
      </div>

      {/* Actions */}
      <div className="flex gap-4">
        <Button
          onClick={handleGetRecommendations}
          disabled={loading || !selectedChampion || enemyTeam.length === 0}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
        >
          {loading ? 'Loading...' : '🛡️ Get Item Recommendations'}
        </Button>
        <Button onClick={handleReset} variant="outline" className="border-slate-600 text-slate-300">
          Reset
        </Button>
      </div>

      {/* Error */}
      {error && (
        <Card className="bg-red-900/20 border-red-500/50">
          <CardContent className="pt-6">
            <p className="text-red-300">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      {recommendations && (
        <div className="space-y-6">
          {/* Recommended Builds */}
          {recommendations.popular_builds.length > 0 ? (
            <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
              <CardHeader>
                <CardTitle className="text-white text-2xl">
                  🛡️ Recommended Item Builds for {recommendations.champion}
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Complete builds sorted by win rate • Hover over items for names
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {recommendations.popular_builds.map((build, index) => (
                    <div
                      key={index}
                      className={`p-6 bg-gradient-to-r rounded-xl border-2 transition-all hover:scale-[1.02] ${
                        index === 0
                          ? 'from-yellow-900/20 to-yellow-800/10 border-yellow-500/50'
                          : 'from-slate-900/50 to-slate-800/30 border-slate-700'
                      }`}
                    >
                      {/* Header */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          {index === 0 && (
                            <div className="text-3xl">🏆</div>
                          )}
                          <div>
                            <h3 className="text-xl font-bold text-white">
                              {index === 0 ? 'Best Build' : `Build #${index + 1}`}
                            </h3>
                            <p className="text-sm text-slate-400">
                              {build.games} games played
                            </p>
                          </div>
                        </div>
                        <Badge
                          className={`text-lg px-4 py-2 ${
                            build.win_rate >= 0.6
                              ? 'bg-green-600'
                              : build.win_rate >= 0.5
                                ? 'bg-blue-600'
                                : 'bg-orange-600'
                          }`}
                        >
                          {(build.win_rate * 100).toFixed(1)}% Win Rate
                        </Badge>
                      </div>

                      {/* Items Grid */}
                      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
                        {build.items.map((itemId, itemIndex) => {
                          const itemData = getItemData(itemId);
                          return (
                            <div
                              key={itemId}
                              className="group relative flex flex-col items-center"
                            >
                              {/* Item Icon */}
                              <div className="relative w-16 h-16 rounded-xl overflow-hidden border-2 border-slate-600 group-hover:border-blue-500 transition-all group-hover:scale-110 shadow-lg">
                                <Image
                                  src={itemData.image}
                                  alt={itemData.name}
                                  fill
                                  className="object-cover"
                                  unoptimized
                                />
                              </div>

                              {/* Item Number Badge */}
                              <div className="mt-2 px-2 py-0.5 bg-slate-700 rounded text-xs text-slate-300">
                                Item {itemIndex + 1}
                              </div>

                              {/* Item Name (always visible) */}
                              <div className="mt-1 text-xs text-center text-white font-medium max-w-[80px] line-clamp-2">
                                {itemData.name}
                              </div>

                              {/* Enhanced Tooltip on hover */}
                              <div className="absolute -top-20 left-1/2 -translate-x-1/2 px-3 py-2 bg-slate-900 border border-blue-500 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-20 shadow-xl">
                                <div className="font-bold">{itemData.name}</div>
                                <div className="text-xs text-slate-400">Item #{itemId}</div>
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      {/* Build Stats */}
                      <div className="mt-4 pt-4 border-t border-slate-700 flex gap-6 text-sm">
                        <div className="flex items-center gap-2">
                          <span className="text-slate-400">Games:</span>
                          <span className="text-white font-semibold">{build.games}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-slate-400">Wins:</span>
                          <span className="text-green-400 font-semibold">{build.wins}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-slate-400">Losses:</span>
                          <span className="text-red-400 font-semibold">{build.games - build.wins}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="bg-slate-800/50 border-yellow-700/30 backdrop-blur">
              <CardContent className="pt-6">
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📦</div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    No Item Builds Found
                  </h3>
                  <p className="text-slate-400 mb-4">
                    Not enough data for {recommendations.champion} with this enemy team composition.
                  </p>
                  <p className="text-sm text-slate-500">
                    Try selecting different enemy champions or check the Champion Stats tab for individual item recommendations.
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
