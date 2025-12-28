import React from 'react';

// Props definieren
interface ChampionCardProps {
  championName: string; // Der "Key" name für die URL (z.B. "Aatrox")
  version: string;      // Die aktuelle Patch-Version (z.B. "14.1.1")
}

export const ChampionCard = ({ championName, version }: ChampionCardProps) => {
  // URL generieren
  const imageUrl = `https://ddragon.leagueoflegends.com/cdn/${version}/img/champion/${championName}.png`;

  return (
    <div className="flex flex-col items-center p-2 border border-slate-700 bg-slate-900 rounded-lg hover:border-blue-500 transition-all">
      <div className="relative w-16 h-16 mb-2">
        <img 
          src={imageUrl} 
          alt={championName}
          className="rounded-full border-2 border-slate-600"
          // Fallback, falls Bild nicht lädt (z.B. neuer Champ)
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/fallback-icon.png';
          }}
        />
      </div>
      <span className="text-xs font-bold text-slate-200">{championName}</span>
    </div>
  );
};