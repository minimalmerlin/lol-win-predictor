"use client";

import { useState, useEffect, useRef } from 'react';
import { getLatestChampionData, ChampionDto, getChampionImageUrl } from '@/lib/riot-data';
import { useRouter } from 'next/navigation';
import { Search, X } from 'lucide-react';

// Optional Props definieren
interface ChampionSearchProps {
  onSelect?: (championId: string) => void; // Wenn vorhanden -> Selection Mode
}

/**
 * Fuzzy string matching using Levenshtein distance
 * Returns similarity score between 0 and 1 (1 = exact match)
 */
function fuzzyMatch(str: string, pattern: string): number {
  const strLower = str.toLowerCase();
  const patternLower = pattern.toLowerCase();

  // Exact match
  if (strLower === patternLower) return 1.0;

  // Contains match (high score)
  if (strLower.includes(patternLower)) {
    return 0.8 + (0.2 * (patternLower.length / strLower.length));
  }

  // Starts with match
  if (strLower.startsWith(patternLower)) {
    return 0.75;
  }

  // Levenshtein distance for typo tolerance
  const distance = levenshteinDistance(strLower, patternLower);
  const maxLength = Math.max(strLower.length, patternLower.length);

  if (distance > maxLength / 2) return 0; // Too different

  return 1 - (distance / maxLength);
}

/**
 * Calculate Levenshtein distance between two strings
 */
function levenshteinDistance(a: string, b: string): number {
  const matrix: number[][] = [];

  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }

  return matrix[b.length][a.length];
}

export default function ChampionSearch({ onSelect }: ChampionSearchProps) {
  const router = useRouter();
  const [champions, setChampions] = useState<ChampionDto[]>([]);
  const [filtered, setFiltered] = useState<ChampionDto[]>([]);
  const [version, setVersion] = useState("14.24.1");
  const [search, setSearch] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getLatestChampionData().then(data => {
      setVersion(data.version);
      setChampions(data.champions.sort((a, b) => a.name.localeCompare(b.name)));
    });
  }, []);

  useEffect(() => {
    if (!search) {
      setFiltered([]);
      return;
    }

    const term = search.toLowerCase();

    // Fuzzy search with scoring
    const scored = champions.map(c => ({
      champion: c,
      score: Math.max(
        fuzzyMatch(c.name, term),
        fuzzyMatch(c.id, term),
        fuzzyMatch(c.title, term) * 0.5 // Title match counts less
      )
    }));

    // Filter and sort by score
    const results = scored
      .filter(item => item.score > 0.3) // Minimum threshold
      .sort((a, b) => b.score - a.score) // Best matches first
      .slice(0, 10) // Limit results
      .map(item => item.champion);

    setFiltered(results);
  }, [search, champions]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // HYBRID LOGIC HANDLER
  const handleSelect = (id: string) => {
    if (onSelect) {
      // DRAFT MODE: Übergib ID an Parent, keine Navigation
      onSelect(id);
      setSearch(""); // Reset Input
      setIsOpen(false);
    } else {
      // NAVIGATION MODE: Gehe zur Detailseite
      setIsOpen(false);
      setSearch("");
      router.push(`/champion/${id}`);
    }
  };

  return (
    <div ref={wrapperRef} className="relative w-full z-50">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
        <input
          type="text"
          placeholder="Champion suchen... (z.B. 'yasou', 'lee sin')"
          className="w-full bg-slate-900 border border-slate-700 rounded-lg py-3 pl-12 pr-10 text-white focus:outline-none focus:border-[#1E90FF] focus:ring-1 focus:ring-[#1E90FF] transition-all"
          value={search}
          onFocus={() => setIsOpen(true)}
          onChange={(e) => { setSearch(e.target.value); setIsOpen(true); }}
        />
        {search && (
          <button onClick={() => setSearch('')} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {isOpen && search && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-slate-900 border border-slate-700 rounded-lg shadow-xl max-h-[300px] overflow-y-auto custom-scrollbar">
          {filtered.length > 0 ? (
            <div className="py-2">
              {filtered.map((champ) => (
                <div
                  key={champ.key}
                  onMouseDown={() => handleSelect(champ.id)}
                  className="flex items-center gap-4 px-4 py-3 hover:bg-[#1E90FF]/10 border-l-4 border-transparent hover:border-[#1E90FF] transition-all group cursor-pointer"
                >
                  <img
                    src={getChampionImageUrl(champ.id, version)}
                    alt={champ.name}
                    className="w-10 h-10 rounded-full border border-slate-700"
                  />
                  <div>
                    <div className="text-slate-200 font-bold group-hover:text-white">{champ.name}</div>
                    <div className="text-xs text-slate-500">{champ.title}</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 text-center text-slate-500 text-sm">
              Keine Treffer für "{search}". Versuche es mit einem anderen Namen.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
