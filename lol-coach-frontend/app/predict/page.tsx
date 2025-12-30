"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { AlertCircle, TrendingUp, Trophy, Sword } from 'lucide-react'

interface PredictionResult {
  blue_win_probability: number
  red_win_probability: number
  prediction: string
  confidence: string
  details: {
    gold_diff: number
    xp_diff: number
    kill_diff: number
    tower_diff: number
    dragon_diff: number
    snapshot_time: number
    model: string
    accuracy: string
  }
}

export default function PredictPage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  // Form state
  const [blueGold, setBlueGold] = useState('25000')
  const [redGold, setRedGold] = useState('23000')
  const [blueXP, setBlueXP] = useState('30000')
  const [redXP, setRedXP] = useState('28000')
  const [blueLevel, setBlueLevel] = useState('58')
  const [redLevel, setRedLevel] = useState('55')
  const [blueCS, setBlueCS] = useState('450')
  const [redCS, setRedCS] = useState('420')
  const [blueKills, setBlueKills] = useState('12')
  const [redKills, setRedKills] = useState('8')
  const [blueDragons, setBlueDragons] = useState('2')
  const [redDragons, setRedDragons] = useState('1')
  const [blueBarons, setBlueBarons] = useState('0')
  const [redBarons, setRedBarons] = useState('0')
  const [blueTowers, setBlueTowers] = useState('5')
  const [redTowers, setRedTowers] = useState('3')

  const handlePredict = async () => {
    try {
      setLoading(true)
      setError(null)

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
      const response = await fetch(`${API_URL}/api/predict-game-state`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          blue_gold: parseInt(blueGold),
          red_gold: parseInt(redGold),
          blue_xp: parseInt(blueXP),
          red_xp: parseInt(redXP),
          blue_level: parseInt(blueLevel),
          red_level: parseInt(redLevel),
          blue_cs: parseInt(blueCS),
          red_cs: parseInt(redCS),
          blue_kills: parseInt(blueKills),
          red_kills: parseInt(redKills),
          blue_dragons: parseInt(blueDragons),
          red_dragons: parseInt(redDragons),
          blue_barons: parseInt(blueBarons),
          red_barons: parseInt(redBarons),
          blue_towers: parseInt(blueTowers),
          red_towers: parseInt(redTowers),
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Prediction failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error('Prediction error:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const loadExampleData = (scenario: 'blue_ahead' | 'even' | 'red_ahead') => {
    if (scenario === 'blue_ahead') {
      setBlueGold('25000'); setRedGold('23000')
      setBlueXP('30000'); setRedXP('28000')
      setBlueLevel('58'); setRedLevel('55')
      setBlueCS('450'); setRedCS('420')
      setBlueKills('12'); setRedKills('8')
      setBlueDragons('2'); setRedDragons('1')
      setBlueBarons('0'); setRedBarons('0')
      setBlueTowers('5'); setRedTowers('3')
    } else if (scenario === 'even') {
      setBlueGold('24000'); setRedGold('24500')
      setBlueXP('29000'); setRedXP('29000')
      setBlueLevel('56'); setRedLevel('56')
      setBlueCS('430'); setRedCS('435')
      setBlueKills('10'); setRedKills('10')
      setBlueDragons('1'); setRedDragons('1')
      setBlueBarons('0'); setRedBarons('0')
      setBlueTowers('4'); setRedTowers('4')
    } else {
      setBlueGold('22000'); setRedGold('25000')
      setBlueXP('27000'); setRedXP('31000')
      setBlueLevel('54'); setRedLevel('59')
      setBlueCS('400'); setRedCS('460')
      setBlueKills('7'); setRedKills('13')
      setBlueDragons('0'); setRedDragons('2')
      setBlueBarons('0'); setRedBarons('1')
      setBlueTowers('2'); setRedTowers('5')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Game State Predictor</h1>
          <p className="text-gray-400">
            Predict match outcome based on real-time game statistics (79.28% accuracy)
          </p>
        </div>

        {/* Quick Load Examples */}
        <div className="flex gap-4">
          <Button
            onClick={() => loadExampleData('blue_ahead')}
            className="bg-blue-600 hover:bg-blue-700"
          >
            Blue Team Ahead
          </Button>
          <Button
            onClick={() => loadExampleData('even')}
            className="bg-gray-600 hover:bg-gray-700"
          >
            Even Game
          </Button>
          <Button
            onClick={() => loadExampleData('red_ahead')}
            className="bg-red-600 hover:bg-red-700"
          >
            Red Team Ahead
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Gold & XP */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white">Economy & Experience</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue Gold</Label>
                  <Input
                    type="number"
                    value={blueGold}
                    onChange={(e) => setBlueGold(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red Gold</Label>
                  <Input
                    type="number"
                    value={redGold}
                    onChange={(e) => setRedGold(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue XP</Label>
                  <Input
                    type="number"
                    value={blueXP}
                    onChange={(e) => setBlueXP(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red XP</Label>
                  <Input
                    type="number"
                    value={redXP}
                    onChange={(e) => setRedXP(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Levels & CS */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white">Levels & Farm</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue Level (Total)</Label>
                  <Input
                    type="number"
                    value={blueLevel}
                    onChange={(e) => setBlueLevel(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red Level (Total)</Label>
                  <Input
                    type="number"
                    value={redLevel}
                    onChange={(e) => setRedLevel(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue CS</Label>
                  <Input
                    type="number"
                    value={blueCS}
                    onChange={(e) => setBlueCS(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red CS</Label>
                  <Input
                    type="number"
                    value={redCS}
                    onChange={(e) => setRedCS(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Combat Stats */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white">Combat Statistics</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue Kills</Label>
                  <Input
                    type="number"
                    value={blueKills}
                    onChange={(e) => setBlueKills(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red Kills</Label>
                  <Input
                    type="number"
                    value={redKills}
                    onChange={(e) => setRedKills(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Objectives */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white">Objectives</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue Dragons</Label>
                  <Input
                    type="number"
                    value={blueDragons}
                    onChange={(e) => setBlueDragons(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red Dragons</Label>
                  <Input
                    type="number"
                    value={redDragons}
                    onChange={(e) => setRedDragons(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue Barons</Label>
                  <Input
                    type="number"
                    value={blueBarons}
                    onChange={(e) => setBlueBarons(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red Barons</Label>
                  <Input
                    type="number"
                    value={redBarons}
                    onChange={(e) => setRedBarons(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-blue-400">Blue Towers</Label>
                  <Input
                    type="number"
                    value={blueTowers}
                    onChange={(e) => setBlueTowers(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-red-400">Red Towers</Label>
                  <Input
                    type="number"
                    value={redTowers}
                    onChange={(e) => setRedTowers(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
              </CardContent>
            </Card>

            <Button
              onClick={handlePredict}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 h-12 text-lg"
            >
              {loading ? 'Predicting...' : 'Predict Outcome'}
            </Button>
          </div>

          {/* Results */}
          <div>
            {error && (
              <Card className="bg-gray-900 border-red-500/50">
                <CardHeader>
                  <CardTitle className="text-red-400 flex items-center gap-2">
                    <AlertCircle className="h-5 w-5" />
                    Error
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-400">{error}</p>
                </CardContent>
              </Card>
            )}

            {result && (
              <div className="space-y-4">
                {/* Win Probabilities */}
                <Card className="bg-gray-900 border-gray-800">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center gap-2">
                      <Trophy className="h-5 w-5" />
                      Prediction
                    </CardTitle>
                    <CardDescription>{result.prediction}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="flex justify-between mb-2">
                        <span className="text-blue-400 font-medium">Blue Team</span>
                        <span className="text-white font-bold">
                          {(result.blue_win_probability * 100).toFixed(2)}%
                        </span>
                      </div>
                      <Progress
                        value={result.blue_win_probability * 100}
                        className="h-3 bg-gray-800"
                      />
                    </div>

                    <div>
                      <div className="flex justify-between mb-2">
                        <span className="text-red-400 font-medium">Red Team</span>
                        <span className="text-white font-bold">
                          {(result.red_win_probability * 100).toFixed(2)}%
                        </span>
                      </div>
                      <Progress
                        value={result.red_win_probability * 100}
                        className="h-3 bg-gray-800"
                      />
                    </div>

                    <div className="pt-4 border-t border-gray-800">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Confidence</span>
                        <Badge
                          className={
                            result.confidence === 'high'
                              ? 'bg-green-500/20 text-green-400 border-green-500/50'
                              : result.confidence === 'medium'
                              ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50'
                              : 'bg-gray-500/20 text-gray-400 border-gray-500/50'
                          }
                        >
                          {result.confidence.toUpperCase()}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Statistics */}
                <Card className="bg-gray-900 border-gray-800">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Game State Details
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Gold Difference</span>
                      <span className={result.details.gold_diff > 0 ? 'text-blue-400' : 'text-red-400'}>
                        {result.details.gold_diff > 0 ? '+' : ''}{result.details.gold_diff}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">XP Difference</span>
                      <span className={result.details.xp_diff > 0 ? 'text-blue-400' : 'text-red-400'}>
                        {result.details.xp_diff > 0 ? '+' : ''}{result.details.xp_diff}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Kill Difference</span>
                      <span className={result.details.kill_diff > 0 ? 'text-blue-400' : 'text-red-400'}>
                        {result.details.kill_diff > 0 ? '+' : ''}{result.details.kill_diff}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Tower Difference</span>
                      <span className={result.details.tower_diff > 0 ? 'text-blue-400' : 'text-red-400'}>
                        {result.details.tower_diff > 0 ? '+' : ''}{result.details.tower_diff}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Dragon Difference</span>
                      <span className={result.details.dragon_diff > 0 ? 'text-blue-400' : 'text-red-400'}>
                        {result.details.dragon_diff > 0 ? '+' : ''}{result.details.dragon_diff}
                      </span>
                    </div>

                    <div className="pt-4 border-t border-gray-800 space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Model Accuracy</span>
                        <span className="text-white">{result.details.accuracy}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Snapshot Time</span>
                        <span className="text-white">{result.details.snapshot_time} min</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
