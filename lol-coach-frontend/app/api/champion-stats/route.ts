import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

const CHAMPIONS = [
  "Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Ashe",
  "Aurelion Sol", "Azir", "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn",
  "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo",
  "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora",
  "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Hecarim",
  "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan IV", "Jax",
  "Jayce", "Jhin", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina",
  "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc",
  "Lee Sin", "Leona", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar",
  "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus",
  "Nautilus", "Nidalee", "Nocturne", "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon",
  "Poppy", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Renekton", "Rengar", "Riven",
  "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir",
  "Skarner", "Sona", "Soraka", "Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon",
  "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate",
  "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi", "Viktor",
  "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo",
  "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zyra"
];

// Generate mock stats for a champion
function generateChampionStats(name: string) {
  const games = Math.floor(Math.random() * 5000 + 1000);
  const winRate = Math.random() * 0.15 + 0.45; // 45-60% win rate
  const wins = Math.floor(games * winRate);
  const losses = games - wins;

  return {
    name,
    games,
    wins,
    losses,
    win_rate: winRate,
    roles: {
      'TOP': Math.random() * 0.5,
      'JUNGLE': Math.random() * 0.5,
      'MIDDLE': Math.random() * 0.5,
      'BOTTOM': Math.random() * 0.5,
      'SUPPORT': Math.random() * 0.5,
    }
  };
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const minGames = parseInt(searchParams.get('min_games') || '0');
  const sortBy = searchParams.get('sort_by') || 'win_rate';
  const limit = parseInt(searchParams.get('limit') || '999');

  // Generate stats for all champions
  let championStats = CHAMPIONS.map(generateChampionStats);

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
