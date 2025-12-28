"use client";

import { useState, useEffect } from 'react';
import { getLatestChampionData, ChampionDto } from '@/lib/riot-data';
import { ChampionCard } from './ChampionCard';
import { Search } from 'lucide-react';

interface ChampionSearchProps {
  onSelect?: (championName: string) => void;
}

export default function ChampionSearch({ onSelect }: ChampionSearchProps = {}) {
  const [champions, setChampions] = useState<ChampionDto[]>([]);
  const [filtered, setFiltered] = useState<ChampionDto[]>([]);
  const [version, setVersion] = useState("14.24.1");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      // Direkt von Riot via unsere Lib laden
      const data = await getLatestChampionData();
      setVersion(data.version);

      // Sortieren
      const sorted = data.champions.sort((a, b) => a.name.localeCompare(b.name));
      setChampions(sorted);
      setFiltered(sorted);
      setLoading(false);
    }
    load();
  }, []);

  // Filter Logik
  useEffect(() => {
    const term = search.toLowerCase();
    const result = champions.filter(c =>
      c.name.toLowerCase().includes(term) ||
      c.id.toLowerCase().includes(term) ||
      c.tags.some(t => t.toLowerCase().includes(term))
    );
    setFiltered(result);
  }, [search, champions]);

  return (
    <div className="w-full max-w-7xl mx-auto p-4">
      {/* Search Input */}
      <div className="relative mb-8 max-w-xl mx-auto">
        <input
          type="text"
          placeholder="Suche Champion (z.B. Aatrox, Assassin...)"
          className="w-full bg-slate-900 border border-slate-700 rounded-full py-3 px-6 text-white focus:outline-none focus:border-[#1E90FF] focus:ring-1 focus:ring-[#1E90FF] transition-all"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Grid */}
      {loading ? (
        <div className="text-center text-slate-500 animate-pulse">Lade Riot Daten...</div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {filtered.map((champ) => (
            <div
              key={champ.key}
              className="h-full"
              onClick={() => onSelect && onSelect(champ.name)}
            >
              {/* Wir reichen die Version explizit weiter, damit Bilder laden */}
              <ChampionCard champion={champ} version={version} />
            </div>
          ))}
        </div>
      )}

      {!loading && filtered.length === 0 && (
        <div className="text-center text-slate-500 mt-10">Keine Champions gefunden.</div>
      )}
    </div>
  );
}
