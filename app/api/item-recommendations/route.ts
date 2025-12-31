import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { champion } = body; // championId oder champion Name

    if (!champion) {
      return NextResponse.json({
        status: 'error',
        message: 'Champion parameter missing',
        champion: '',
        recommended_items: [],
        popular_builds: []
      }, { status: 400 });
    }

    // Lade die generierte JSON-Datei
    const jsonPath = path.join(process.cwd(), 'public', 'data', 'item_builds.json');

    if (!fs.existsSync(jsonPath)) {
      return NextResponse.json({
        status: 'pending',
        message: 'Item-Datenbank wird aktuell neu aufgebaut (Crawler aktiv).',
        champion: champion,
        recommended_items: [],
        popular_builds: []
      });
    }

    const fileContents = fs.readFileSync(jsonPath, 'utf8');
    const allBuilds = JSON.parse(fileContents);

    // Suche nach Champion (die Keys sind Namen wie "Aatrox")
    let championBuild = allBuilds[champion];

    // Falls nicht gefunden, versuche case-insensitive Suche
    if (!championBuild) {
      const championLower = champion.toLowerCase();
      const matchingKey = Object.keys(allBuilds).find(
        key => key.toLowerCase() === championLower
      );
      if (matchingKey) {
        championBuild = allBuilds[matchingKey];
      }
    }

    if (!championBuild || championBuild.length === 0) {
      return NextResponse.json({
        status: 'pending',
        message: `Noch nicht genug Daten für ${champion}.`,
        champion: champion,
        recommended_items: [],
        popular_builds: []
      });
    }

    // Erstelle ein Build-Objekt im erwarteten Format
    // Da wir aktuell nur "Most Common Items" haben, erstellen wir einen Single Build
    const build = {
      items: championBuild.filter((id: number) => id !== 0), // Filtere leere Slots
      games: 100, // Placeholder - wir tracken noch keine genauen Zahlen
      wins: 55,   // Placeholder
      win_rate: 0.55 // Placeholder
    };

    return NextResponse.json({
      status: 'success',
      champion: champion,
      recommended_items: [], // Vorerst leer, da wir nur Builds haben
      popular_builds: [build]
    });

  } catch (error) {
    console.error('Item recommendations error:', error);
    return NextResponse.json({
      status: 'error',
      message: 'Internal server error',
      champion: '',
      recommended_items: [],
      popular_builds: []
    }, { status: 500 });
  }
}
