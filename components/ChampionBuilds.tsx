"use client";

import { useEffect, useState } from 'react';
import { getItemImageUrl } from '@/lib/riot-data';

export default function ChampionBuilds({ champName }: { champName: string }) {
  const [build, setBuild] = useState<number[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/data/item_builds.json')
      .then(res => res.json())
      .then(data => {
        // Wir suchen nach dem Champion-Namen
        if (data[champName]) {
          setBuild(data[champName]);
        } else {
          setBuild(null);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load builds", err);
        setLoading(false);
      });
  }, [champName]);

  if (loading) return <div className="text-slate-500 text-sm animate-pulse">Lade Item-Daten...</div>;

  if (!build) {
    return (
       <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl text-center">
         <p className="text-slate-500 text-sm italic">
           Noch nicht genügend Daten für einen verlässlichen Build gesammelt.
         </p>
       </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-orange-400 font-bold text-sm tracking-widest uppercase">
            Most Frequent Winner Build
        </h3>
        <span className="text-xs text-green-500 bg-green-500/10 px-2 py-1 rounded border border-green-500/20">
            LIVE DATA
        </span>
      </div>

      <div className="flex flex-wrap gap-4">
        {build.map((itemId, index) => (
          <div key={index} className="group relative">
            {itemId !== 0 ? (
                <>
                  <img
                    src={getItemImageUrl(itemId)}
                    alt={`Item ${itemId}`}
                    className="w-16 h-16 rounded border border-slate-700 group-hover:border-orange-400 transition-colors"
                  />
                  {/* Tooltip für Item ID (Name wäre besser, aber ID reicht für V1) */}
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    ID: {itemId}
                  </span>
                </>
            ) : (
                <div className="w-16 h-16 bg-slate-950 rounded border border-slate-800 flex items-center justify-center">
                    <span className="text-slate-700 text-xs">Empty</span>
                </div>
            )}
          </div>
        ))}
      </div>

      <p className="mt-6 text-xs text-slate-500">
        Basierend auf aktuellen Gewinner-Matches. Das System lernt kontinuierlich dazu.
      </p>
    </div>
  );
}
