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

  if (query && query.length >= 2) {
    // Filter and calculate similarity
    const matches = CHAMPIONS
      .map(name => ({
        name,
        similarity: calculateSimilarity(query, name)
      }))
      .filter(m => m.similarity > 0.3)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit)
      .map(m => ({
        name: m.name,
        similarity: m.similarity,
        match_quality: m.similarity >= 0.9 ? 'exact' : m.similarity >= 0.7 ? 'good' : 'partial',
        has_builds: true,
        stats: {
          games: Math.floor(Math.random() * 10000 + 1000),
          win_rate: Math.random() * 0.2 + 0.45 // 45-65% win rate
        }
      }));

    return NextResponse.json({ results: matches });
  }

  return NextResponse.json({ results: [] });
}
