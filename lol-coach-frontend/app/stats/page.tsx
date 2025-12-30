"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Database, TrendingUp, Target, Zap } from 'lucide-react'

interface StatsData {
  database: {
    matches: number
    champions: number
    snapshots: number
    size: string
    connection: string
  }
  models: {
    game_state: {
      accuracy: number
      roc_auc: number
      snapshot_time: number
      trained_on: number
      timestamp: string
    }
    champion_matchup: {
      accuracy: number
      trained_on: number
      timestamp: string
    }
  }
  api_version: string
  data_source: string
}

export default function StatsPage() {
  const [stats, setStats] = useState<StatsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000'
      const response = await fetch(`${API_URL}/api/stats`)

      if (!response.ok) {
        throw new Error('Failed to fetch stats')
      }

      const data = await response.json()
      setStats(data)
      setError(null)
    } catch (err) {
      console.error('Error fetching stats:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-12 bg-gray-800 rounded w-1/3"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[1, 2, 3, 4].map(i => (
                <div key={i} className="h-32 bg-gray-800 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error || !stats) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 p-8">
        <div className="max-w-7xl mx-auto">
          <Card className="border-red-500/50 bg-gray-900">
            <CardHeader>
              <CardTitle className="text-red-400">Error Loading Stats</CardTitle>
              <CardDescription>{error || 'Unknown error'}</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">System Statistics</h1>
          <p className="text-gray-400">
            Real-time performance metrics and database statistics
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="bg-gray-900 border-blue-500/30">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">
                Total Matches
              </CardTitle>
              <Database className="h-4 w-4 text-blue-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">
                {stats.database.matches.toLocaleString()}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                In PostgreSQL database
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-900 border-green-500/30">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">
                Model Accuracy
              </CardTitle>
              <Target className="h-4 w-4 text-green-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">
                {(stats.models.game_state.accuracy * 100).toFixed(2)}%
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Game State Predictor
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-900 border-purple-500/30">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">
                ROC-AUC Score
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-purple-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">
                {(stats.models.game_state.roc_auc * 100).toFixed(2)}%
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Classification Quality
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-900 border-orange-500/30">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">
                Database Size
              </CardTitle>
              <Zap className="h-4 w-4 text-orange-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">
                {stats.database.size}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                PostgreSQL Storage
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Model Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Game State Predictor */}
          <Card className="bg-gray-900 border-gray-800">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-white">Game State Predictor</CardTitle>
                  <CardDescription>
                    Real-time win prediction from game state
                  </CardDescription>
                </div>
                <Badge className="bg-green-500/20 text-green-400 border-green-500/50">
                  Production
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">Accuracy</span>
                  <span className="text-lg font-bold text-white">
                    {(stats.models.game_state.accuracy * 100).toFixed(2)}%
                  </span>
                </div>
                <Progress
                  value={stats.models.game_state.accuracy * 100}
                  className="h-2 bg-gray-800"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">ROC-AUC</span>
                  <span className="text-lg font-bold text-white">
                    {(stats.models.game_state.roc_auc * 100).toFixed(2)}%
                  </span>
                </div>
                <Progress
                  value={stats.models.game_state.roc_auc * 100}
                  className="h-2 bg-gray-800"
                />
              </div>

              <div className="pt-4 border-t border-gray-800 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Snapshot Time</span>
                  <span className="text-white">{stats.models.game_state.snapshot_time} minutes</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Training Data</span>
                  <span className="text-white">{stats.models.game_state.trained_on.toLocaleString()} matches</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Last Updated</span>
                  <span className="text-white">
                    {new Date(stats.models.game_state.timestamp).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Champion Matchup Predictor */}
          <Card className="bg-gray-900 border-gray-800">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-white">Champion Matchup Predictor</CardTitle>
                  <CardDescription>
                    Draft phase win prediction
                  </CardDescription>
                </div>
                <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/50">
                  Active
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">Accuracy</span>
                  <span className="text-lg font-bold text-white">
                    {(stats.models.champion_matchup.accuracy * 100).toFixed(2)}%
                  </span>
                </div>
                <Progress
                  value={stats.models.champion_matchup.accuracy * 100}
                  className="h-2 bg-gray-800"
                />
              </div>

              <div className="pt-4 border-t border-gray-800 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Training Data</span>
                  <span className="text-white">{stats.models.champion_matchup.trained_on.toLocaleString()} matches</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Last Updated</span>
                  <span className="text-white">
                    {new Date(stats.models.champion_matchup.timestamp).toLocaleDateString()}
                  </span>
                </div>
              </div>

              <div className="pt-4">
                <p className="text-xs text-gray-500">
                  Note: 52% accuracy is expected for draft-only predictions,
                  as it's marginally better than random (50%).
                  Real improvements come from game state data.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Database Info */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Database Information</CardTitle>
            <CardDescription>PostgreSQL storage and performance</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div>
                <div className="text-2xl font-bold text-white">
                  {stats.database.matches.toLocaleString()}
                </div>
                <div className="text-sm text-gray-400">Matches</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">
                  {stats.database.champions.toLocaleString()}
                </div>
                <div className="text-sm text-gray-400">Champion Picks</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">
                  {stats.database.snapshots.toLocaleString()}
                </div>
                <div className="text-sm text-gray-400">Timeline Snapshots</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">
                  {stats.database.size}
                </div>
                <div className="text-sm text-gray-400">Total Size</div>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-400">Database Status:</span>
                <span className="text-sm font-medium text-green-400">
                  {stats.database.connection}
                </span>
              </div>
              <div className="text-sm text-gray-500">
                API Version: {stats.api_version}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
