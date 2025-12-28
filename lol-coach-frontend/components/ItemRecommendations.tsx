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

      {/* Recommendations / Pending Status */}
      {recommendations && (
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
  );
}
