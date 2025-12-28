import React from 'react';
import Link from 'next/link';
import { ChampionDto, getChampionImageUrl } from '@/lib/riot-data';

interface ChampionCardProps {
  champion: ChampionDto;
  version?: string; // Optional, da riot-data jetzt einen Default hat
  onClick?: () => void; // Optional click handler (for draft selection)
}

export const ChampionCard = ({ champion, version = "14.24.1", onClick }: ChampionCardProps) => {
  // WICHTIG: Riot nutzt für Bilder IMMER die ID (z.B. "MonkeyKing"), nie den Namen ("Wukong").
  // Wir nutzen die ID auch für die URL, um Encoding-Probleme (Leerzeichen, Apostrophe) zu vermeiden.

  const content = (
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
  );

  // If onClick provided, use div for draft selection; otherwise Link for navigation
  if (onClick) {
    return (
      <div
        onClick={onClick}
        className="block rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer group bg-slate-900 hover:bg-slate-800"
      >
        {content}
      </div>
    );
  }

  return (
    <Link
      href={`/champion/${champion.id}`}
      className="block rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer group bg-slate-900 hover:bg-slate-800"
    >
      {content}
    </Link>
  );
};
