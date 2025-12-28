import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';
import fs from 'fs';
import path from 'path';

function getChampionStats() {
  try {
    // Load from champion_stats.json
    const statsPath = path.join(process.cwd(), '..', 'data', 'champion_data', 'champion_stats.json');

    if (fs.existsSync(statsPath)) {
      const data = JSON.parse(fs.readFileSync(statsPath, 'utf-8'));

      // Convert to array format expected by frontend
      return Object.entries(data).map(([name, stats]: [string, any]) => ({
        name,
        games: stats.games || 0,
        wins: stats.wins || 0,
        losses: stats.losses || 0,
        win_rate: stats.win_rate || 0,
        roles: stats.roles || {}
      }));
    }
  } catch (error) {
    console.error('Error loading champion stats:', error);
  }

  return [];
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const minGames = parseInt(searchParams.get('min_games') || '0');
  const sortBy = searchParams.get('sort_by') || 'win_rate';
  const limit = parseInt(searchParams.get('limit') || '999');

  // Get real champion stats
  let championStats = getChampionStats();

  // Filter by minimum games
  if (minGames > 0) {
    championStats = championStats.filter(c => c.games >= minGames);
  }

  // Sort
  if (sortBy === 'win_rate') {
    championStats.sort((a, b) => b.win_rate - a.win_rate);
  } else if (sortBy === 'games') {
    championStats.sort((a, b) => b.games - a.games);
  }

  // Limit results
  championStats = championStats.slice(0, limit);

  return NextResponse.json({
    champions: championStats,
    total_champions: championStats.length
  });
}
