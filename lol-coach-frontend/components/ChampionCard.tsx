import React from 'react';
import Link from 'next/link';
import { ChampionDto, getChampionImageUrl } from '@/lib/riot-data';

interface ChampionCardProps {
  champion: ChampionDto;
  version?: string; // Optional, da riot-data jetzt einen Default hat
}

export const ChampionCard = ({ champion, version = "14.24.1" }: ChampionCardProps) => {
  // WICHTIG: Riot nutzt für Bilder IMMER die ID (z.B. "MonkeyKing"), nie den Namen ("Wukong").
  // Wir nutzen die ID auch für die URL, um Encoding-Probleme (Leerzeichen, Apostrophe) zu vermeiden.

  return (
    <Link
      href={`/champion/${champion.id}`}
      className="block group relative overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50 hover:border-[#1E90FF] transition-all duration-300 hover:shadow-[0_0_20px_rgba(30,144,255,0.3)] hover:-translate-y-1"
    >
      {/* Image Container */}
      <div className="aspect-square w-full overflow-hidden relative">
        <img
          src={getChampionImageUrl(champion.id, version)}
          alt={champion.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          loading="lazy"
          // Fallback falls Bild kaputt ist
          onError={(e) => {
            (e.target as HTMLImageElement).src = "https://ddragon.leagueoflegends.com/cdn/img/champion/tiles/Poro_0.jpg";
          }}
        />

        {/* Overlay Gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent opacity-80" />

        {/* Name Overlay */}
        <div className="absolute bottom-0 left-0 right-0 p-3">
          <h3 className="text-white font-bold text-lg tracking-wide group-hover:text-[#1E90FF] transition-colors truncate">
            {champion.name}
          </h3>
          <p className="text-xs text-slate-400 truncate">
            {champion.title}
          </p>
        </div>
      </div>
    </Link>
  );
};
