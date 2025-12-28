import { NextResponse } from 'next/server';

export async function POST() {
  // Aktuell deaktiviert, bis der Item-Crawler (fetch_matches_with_items.py) genug Daten gesammelt hat.
  return NextResponse.json({
    status: 'pending',
    message: 'Item-Datenbank wird aktuell neu aufgebaut (Crawler aktiv).',
    champion: '',
    recommended_items: [],
    popular_builds: []
  });
}
