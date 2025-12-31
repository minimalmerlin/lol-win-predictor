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
          {/* Show builds if available */}
          {recommendations.popular_builds && recommendations.popular_builds.length > 0 ? (
            <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
              <CardHeader>
                <CardTitle className="text-white text-2xl">
                  🛡️ Most Common Winner Build for {recommendations.champion}
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Based on 1,590+ analyzed matches • Hover over items for details
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {recommendations.popular_builds.map((build, index) => (
                    <div
                      key={index}
                      className="p-6 bg-gradient-to-r from-yellow-900/20 to-yellow-800/10 border-2 border-yellow-500/50 rounded-xl"
                    >
                      {/* Header */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="text-3xl">🏆</div>
                          <div>
                            <h3 className="text-xl font-bold text-white">
                              Core Build (Most Common Items)
                            </h3>
                            <p className="text-sm text-slate-400">
                              Based on winning games across all roles
                            </p>
                          </div>
                        </div>
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
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ) : (
            // Pending status when no builds available
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 text-center">
              <div className="text-orange-500 font-bold tracking-widest uppercase mb-2">
                SYSTEM UPDATE IN PROGRESS
              </div>
              <p className="text-slate-400 mb-6">
                Die KI lernt gerade aus neuen Live-Matches die aktuellen Meta-Builds.
                Bitte warte auf den Abschluss des Crawling-Prozesses.
              </p>

              {/* Visueller Platzhalter */}
              <div className="flex justify-center gap-4 opacity-30">
                {[1,2,3,4,5,6].map(i => (
                  <div key={i} className="w-12 h-12 bg-slate-800 rounded border border-slate-700"></div>
                ))}
              </div>

              {/* Status Info */}
              <div className="mt-6 pt-6 border-t border-slate-800">
                <p className="text-sm text-slate-500">
                  Der Item-Crawler sammelt aktuell Daten aus 5.000+ Ranked-Matches.
                  Diese Funktion wird automatisch aktiviert, sobald genug Daten verfügbar sind.
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
