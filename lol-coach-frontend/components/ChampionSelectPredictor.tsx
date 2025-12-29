'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { api, type ChampionMatchupPrediction } from '@/lib/api';
import ChampionCombobox from './ChampionCombobox';

export default function ChampionSelectPredictor() {
  const [blueChampions, setBlueChampions] = useState<string[]>([]);
  const [redChampions, setRedChampions] = useState<string[]>([]);
  const [prediction, setPrediction] = useState<ChampionMatchupPrediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    if (blueChampions.length === 0 || redChampions.length === 0) {
      setError('Please select at least one champion for each team');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await api.predictChampionMatchup(blueChampions, redChampions);
      setPrediction(result);
    } catch (err: any) {
      // Show detailed error message
      const errorMessage = err?.message || err?.details || 'Failed to predict matchup. Please try again.';
      setError(errorMessage);
      console.error('Prediction error:', err);
      
      // Log full error for debugging
      if (err?.response) {
        console.error('Response error:', await err.response.text());
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setBlueChampions([]);
    setRedChampions([]);
    setPrediction(null);
    setError(null);
  };

  const addBlueChampion = (champion: string) => {
    if (!blueChampions.includes(champion) && blueChampions.length < 5) {
      setBlueChampions([...blueChampions, champion]);
    }
  };

  const addRedChampion = (champion: string) => {
    if (!redChampions.includes(champion) && redChampions.length < 5) {
      setRedChampions([...redChampions, champion]);
    }
  };

  const removeBlueChampion = (champion: string) => {
    setBlueChampions(blueChampions.filter((c) => c !== champion));
  };

  const removeRedChampion = (champion: string) => {
    setRedChampions(redChampions.filter((c) => c !== champion));
  };

  return (
    <div className="space-y-6">
      {/* Team Selection */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Blue Team */}
        <Card className="bg-slate-800/50 border-blue-500/30 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-blue-400">🔵 Blue Team</CardTitle>
            <CardDescription className="text-slate-400">
              Select up to 5 champions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ChampionCombobox onSelect={addBlueChampion} disabled={blueChampions.length >= 5} />

            <div className="flex flex-wrap gap-2">
              {blueChampions.map((champ) => (
                <Badge
                  key={champ}
                  variant="secondary"
                  className="bg-blue-600 text-white px-3 py-1 cursor-pointer hover:bg-blue-700"
                  onClick={() => removeBlueChampion(champ)}
                >
                  {champ} ×
                </Badge>
              ))}
            </div>

            <div className="text-sm text-slate-400">
              {blueChampions.length}/5 champions selected
            </div>
          </CardContent>
        </Card>

        {/* Red Team */}
        <Card className="bg-slate-800/50 border-red-500/30 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-red-400">🔴 Red Team</CardTitle>
            <CardDescription className="text-slate-400">
              Select up to 5 champions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ChampionCombobox onSelect={addRedChampion} disabled={redChampions.length >= 5} />

            <div className="flex flex-wrap gap-2">
              {redChampions.map((champ) => (
                <Badge
                  key={champ}
                  variant="secondary"
                  className="bg-red-600 text-white px-3 py-1 cursor-pointer hover:bg-red-700"
                  onClick={() => removeRedChampion(champ)}
                >
                  {champ} ×
                </Badge>
              ))}
            </div>

            <div className="text-sm text-slate-400">
              {redChampions.length}/5 champions selected
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Actions */}
      <div className="flex gap-4 items-center">
        <Button
          onClick={handlePredict}
          disabled={loading || blueChampions.length === 0 || redChampions.length === 0}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
          size="lg"
        >
          {loading ? 'Predicting...' : '🔮 Predict Win Probability'}
        </Button>
        <Button onClick={handleReset} variant="outline" className="border-slate-600 text-slate-300" size="lg">
          Reset
        </Button>
        {(blueChampions.length === 0 || redChampions.length === 0) && !loading && (
          <span className="text-sm text-yellow-400">
            ⚠️ Select at least 1 champion per team
          </span>
        )}
      </div>

      {/* Error */}
      {error && (
        <Card className="bg-red-900/20 border-red-500/50">
          <CardContent className="pt-6">
            <p className="text-red-300">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Prediction Result */}
      {prediction && (
        <Card className="bg-slate-800/50 border-blue-700/30 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-2xl text-white">📊 Prediction Results</CardTitle>
            <CardDescription className="text-slate-400">{prediction.prediction}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Win Probabilities */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-blue-400 font-medium">Blue Team</span>
                  <span className="text-2xl font-bold text-white">
                    {(prediction.blue_win_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress
                  value={prediction.blue_win_probability * 100}
                  className="h-3 bg-slate-700"
                />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-red-400 font-medium">Red Team</span>
                  <span className="text-2xl font-bold text-white">
                    {(prediction.red_win_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress
                  value={prediction.red_win_probability * 100}
                  className="h-3 bg-slate-700"
                />
              </div>
            </div>

            {/* Details */}
            {prediction.details && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-slate-900/50 rounded-lg">
                <div className="text-center">
                  <div className="text-sm text-slate-400">Blue Avg WR</div>
                  <div className="text-lg font-bold text-blue-400">
                    {(prediction.details.blue_avg_winrate * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-slate-400">Red Avg WR</div>
                  <div className="text-lg font-bold text-red-400">
                    {(prediction.details.red_avg_winrate * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-slate-400">Confidence</div>
                  <div className="text-lg font-bold text-yellow-400 capitalize">
                    {prediction.confidence}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-sm text-slate-400">Model Accuracy</div>
                  <div className="text-lg font-bold text-green-400">
                    {prediction.details.accuracy}
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
