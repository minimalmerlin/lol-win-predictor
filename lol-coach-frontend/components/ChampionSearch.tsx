"use client";

import { useState, useEffect, useRef } from 'react';
import { getLatestChampionData, ChampionDto, getChampionImageUrl } from '@/lib/riot-data';
import { useRouter } from 'next/navigation';
import { Search, X } from 'lucide-react';

// Optional Props definieren
interface ChampionSearchProps {
  onSelect?: (championId: string) => void; // Wenn vorhanden -> Selection Mode
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
    setFiltered(champions.filter(c =>
      c.name.toLowerCase().includes(term) || c.id.toLowerCase().includes(term)
    ));
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
          placeholder="Champion suchen..."
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
            <div className="p-4 text-center text-slate-500 text-sm">Keine Treffer.</div>
          )}
        </div>
      )}
    </div>
  );
}
