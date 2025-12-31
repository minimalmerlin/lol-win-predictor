"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Search, TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface MatchSummary {
  match_id: string
  game_duration: number
  blue_win: boolean
  final_score?: {
    blue_kills: number
    red_kills: number
    gold_diff: number
  }
}

export default function HistoryPage() {
  const [matches, setMatches] = useState<MatchSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchMatches()
  }, [])

  const fetchMatches = async () => {
    try {
      setLoading(true)
      // For now, we'll use mock data since we don't have a matches endpoint yet
      // TODO: Implement API endpoint for fetching match history

      const mockMatches: MatchSummary[] = Array.from({ length: 50 }, (_, i) => ({
        match_id: `EUW1_74${70000 + i}`,
        game_duration: 20 + Math.random() * 20,
        blue_win: Math.random() > 0.5,
        final_score: {
          blue_kills: Math.floor(Math.random() * 30),
          red_kills: Math.floor(Math.random() * 30),
          gold_diff: Math.floor((Math.random() - 0.5) * 10000)
        }
      }))

      setMatches(mockMatches)
      setError(null)
    } catch (err) {
      console.error('Error fetching matches:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const filteredMatches = matches.filter(m =>
    m.match_id.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const stats = {
    total: matches.length,
    blue_wins: matches.filter(m => m.blue_win).length,
    red_wins: matches.filter(m => !m.blue_win).length,
    avg_duration: matches.reduce((acc, m) => acc + m.game_duration, 0) / matches.length
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-12 bg-gray-800 rounded w-1/3"></div>
            <div className="h-64 bg-gray-800 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Match History</h1>
          <p className="text-gray-400">
            Browse and analyze historical match data from the database
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-gray-900 border-gray-800">
            <CardHeader className="pb-2">
              <CardDescription>Total Matches</CardDescription>
              <CardTitle className="text-3xl text-white">{stats.total.toLocaleString()}</CardTitle>
            </CardHeader>
          </Card>

          <Card className="bg-gray-900 border-blue-500/30">
            <CardHeader className="pb-2">
              <CardDescription>Blue Side Wins</CardDescription>
              <CardTitle className="text-3xl text-blue-400">{stats.blue_wins}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-gray-500">
                {((stats.blue_wins / stats.total) * 100).toFixed(1)}% win rate
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-900 border-red-500/30">
            <CardHeader className="pb-2">
              <CardDescription>Red Side Wins</CardDescription>
              <CardTitle className="text-3xl text-red-400">{stats.red_wins}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-gray-500">
                {((stats.red_wins / stats.total) * 100).toFixed(1)}% win rate
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-900 border-gray-800">
            <CardHeader className="pb-2">
              <CardDescription>Avg Game Length</CardDescription>
              <CardTitle className="text-3xl text-white">
                {stats.avg_duration.toFixed(1)}m
              </CardTitle>
            </CardHeader>
          </Card>
        </div>

        {/* Search */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Search Matches</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search by Match ID..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 bg-gray-800 border-gray-700 text-white"
                />
              </div>
              <Button
                onClick={fetchMatches}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Refresh
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Match Table */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Recent Matches</CardTitle>
            <CardDescription>
              Showing {filteredMatches.length} of {matches.length} matches
            </CardDescription>
          </CardHeader>
          <CardContent>
            {error ? (
              <div className="text-red-400 text-center py-8">{error}</div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow className="border-gray-800 hover:bg-gray-800/50">
                      <TableHead className="text-gray-400">Match ID</TableHead>
                      <TableHead className="text-gray-400">Duration</TableHead>
                      <TableHead className="text-gray-400">Winner</TableHead>
                      <TableHead className="text-gray-400">Score</TableHead>
                      <TableHead className="text-gray-400 text-right">Gold Diff</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredMatches.slice(0, 20).map((match) => (
                      <TableRow
                        key={match.match_id}
                        className="border-gray-800 hover:bg-gray-800/50 cursor-pointer"
                      >
                        <TableCell className="font-mono text-sm text-gray-300">
                          {match.match_id}
                        </TableCell>
                        <TableCell className="text-gray-400">
                          {match.game_duration.toFixed(1)} min
                        </TableCell>
                        <TableCell>
                          <Badge
                            className={
                              match.blue_win
                                ? 'bg-blue-500/20 text-blue-400 border-blue-500/50'
                                : 'bg-red-500/20 text-red-400 border-red-500/50'
                            }
                          >
                            {match.blue_win ? 'Blue' : 'Red'}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-gray-400">
                          {match.final_score && (
                            <span>
                              <span className="text-blue-400">{match.final_score.blue_kills}</span>
                              {' - '}
                              <span className="text-red-400">{match.final_score.red_kills}</span>
                            </span>
                          )}
                        </TableCell>
                        <TableCell className="text-right">
                          {match.final_score && (
                            <div className="flex items-center justify-end gap-2">
                              {match.final_score.gold_diff > 0 ? (
                                <TrendingUp className="h-4 w-4 text-green-400" />
                              ) : match.final_score.gold_diff < 0 ? (
                                <TrendingDown className="h-4 w-4 text-red-400" />
                              ) : (
                                <Minus className="h-4 w-4 text-gray-400" />
                              )}
                              <span
                                className={
                                  match.final_score.gold_diff > 0
                                    ? 'text-green-400'
                                    : match.final_score.gold_diff < 0
                                    ? 'text-red-400'
                                    : 'text-gray-400'
                                }
                              >
                                {match.final_score.gold_diff > 0 ? '+' : ''}
                                {match.final_score.gold_diff.toLocaleString()}
                              </span>
                            </div>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">About This Data</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-gray-400 space-y-2">
            <p>
              This data is sourced from our PostgreSQL database containing 10,000+ ranked matches
              from EUW1 server.
            </p>
            <p>
              All matches include complete timeline data with 10-minute, 15-minute, and 20-minute
              snapshots for game state analysis.
            </p>
            <p className="text-gray-500 text-xs">
              Note: Currently showing mock data. Live database integration coming soon.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
