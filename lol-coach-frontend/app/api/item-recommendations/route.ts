import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

// Mock item IDs (LoL item IDs)
const ITEMS = {
  // Boots
  boots: [3006, 3047, 3020, 3111, 3009],
  // AD Items
  ad: [3031, 3094, 3036, 3072, 3153],
  // AP Items
  ap: [3089, 3157, 3165, 3135, 3116],
  // Tank Items
  tank: [3068, 3075, 3742, 3065, 3143],
  // Support Items
  support: [3107, 3222, 3504, 3109, 3190],
};

function generateItemRecommendations(champion: string, enemyTeam: string[], topN: number) {
  // Determine item category based on champion name (very simplistic)
  const isADC = ['Jinx', 'Ashe', 'Caitlyn', 'Vayne', 'Ezreal'].includes(champion);
  const isAP = ['Ahri', 'Lux', 'Syndra', 'Orianna', 'Annie'].includes(champion);
  const isTank = ['Malphite', 'Ornn', 'Maokai', 'Shen'].includes(champion);
  const isSupport = ['Janna', 'Lulu', 'Soraka', 'Nami'].includes(champion);

  let itemPool: number[] = [];
  if (isADC) itemPool = [...ITEMS.ad, ...ITEMS.boots];
  else if (isAP) itemPool = [...ITEMS.ap, ...ITEMS.boots];
  else if (isTank) itemPool = [...ITEMS.tank, ...ITEMS.boots];
  else if (isSupport) itemPool = [...ITEMS.support, ...ITEMS.boots];
  else itemPool = [...ITEMS.ad, ...ITEMS.ap, ...ITEMS.tank].slice(0, 15);

  // Generate recommendations
  const recommendations = itemPool.slice(0, topN).map((itemId, index) => {
    const games = Math.floor(Math.random() * 3000 + 500);
    const winRate = Math.random() * 0.15 + 0.50; // 50-65% win rate
    const wins = Math.floor(games * winRate);

    return {
      item_id: itemId,
      games,
      wins,
      win_rate: winRate,
    };
  });

  // Sort by win rate
  recommendations.sort((a, b) => b.win_rate - a.win_rate);

  // Generate popular builds
  const popularBuilds = [
    {
      items: itemPool.slice(0, 6),
      games: Math.floor(Math.random() * 2000 + 1000),
      wins: 0,
      win_rate: 0,
    },
    {
      items: itemPool.slice(1, 7),
      games: Math.floor(Math.random() * 1500 + 500),
      wins: 0,
      win_rate: 0,
    },
    {
      items: itemPool.slice(2, 8),
      games: Math.floor(Math.random() * 1000 + 300),
      wins: 0,
      win_rate: 0,
    },
  ];

  // Calculate wins for builds
  popularBuilds.forEach(build => {
    const winRate = Math.random() * 0.12 + 0.48;
    build.win_rate = winRate;
    build.wins = Math.floor(build.games * winRate);
  });

  // Sort builds by games (popularity)
  popularBuilds.sort((a, b) => b.games - a.games);

  return {
    champion,
    recommended_items: recommendations,
    popular_builds: popularBuilds,
  };
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { champion, enemy_team, top_n = 5 } = body;

    if (!champion) {
      return NextResponse.json(
        { error: 'Missing champion parameter' },
        { status: 400 }
      );
    }

    const enemyTeam = enemy_team || [];
    const recommendations = generateItemRecommendations(champion, enemyTeam, top_n);

    return NextResponse.json(recommendations);
  } catch (error) {
    return NextResponse.json(
      { error: 'Invalid request body' },
      { status: 400 }
    );
  }
}
