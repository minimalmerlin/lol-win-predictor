import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';
import fs from 'fs';
import path from 'path';

function getChampionsData() {
  try {
    // Load from champion_stats.json
    const statsPath = path.join(process.cwd(), '..', 'data', 'champion_data', 'champion_stats.json');

    if (fs.existsSync(statsPath)) {
      const data = JSON.parse(fs.readFileSync(statsPath, 'utf-8'));
      return data;
    }
  } catch (error) {
    console.error('Error loading champion stats:', error);
  }

  return null;
}

// Calculate similarity score between query and champion name
function calculateSimilarity(query: string, championName: string): number {
  const q = query.toLowerCase();
  const c = championName.toLowerCase();

  // Exact match
  if (c === q) return 1.0;

  // Starts with
  if (c.startsWith(q)) return 0.9;

  // Contains
  if (c.includes(q)) return 0.7;

  // Fuzzy match (character overlap)
  const overlap = q.split('').filter(char => c.includes(char)).length;
  return overlap / Math.max(q.length, c.length) * 0.5;
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('query') || searchParams.get('q') || '';
  const limit = parseInt(searchParams.get('limit') || '10');
  const includeStats = searchParams.get('include_stats') === 'true';

  if (query && query.length >= 2) {
    const championsData = getChampionsData();
    const championNames = championsData ? Object.keys(championsData) : [
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

    // Filter and calculate similarity
    const matches = championNames
      .map(name => ({
        name,
        similarity: calculateSimilarity(query, name),
        data: championsData ? championsData[name] : null
      }))
      .filter(m => m.similarity > 0.3)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit)
      .map(m => ({
        name: m.name,
        similarity: m.similarity,
        match_quality: m.similarity >= 0.9 ? 'exact' : m.similarity >= 0.7 ? 'good' : 'partial',
        has_builds: true,
        ...(includeStats && m.data ? {
          stats: {
            games: m.data.games,
            win_rate: m.data.win_rate
          }
        } : {})
      }));

    return NextResponse.json({ results: matches });
  }

  return NextResponse.json({ results: [] });
}
