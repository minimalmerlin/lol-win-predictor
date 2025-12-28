'use client';

import { useEffect, useState } from 'react';

interface SynergyWidgetProps {
  champName: string;
}

export function SynergyWidget({ champName }: SynergyWidgetProps) {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch('/data/champion_stats.json')
      .then(res => res.json())
      .then(data => {
        if (data[champName]) setStats(data[champName]);
      })
      .catch(e => console.error(e));
  }, [champName]);

  return (
    <div className="bg-gradient-to-b from-slate-800 to-slate-900 border border-slate-700 p-6 rounded-xl shadow-lg">
      <h3 className="text-[#1E90FF] font-bold text-sm tracking-widest uppercase mb-4">Best Teammates</h3>
      {stats ? (
        <div className="space-y-2">
          {stats.best_teammates.map((mate: any, i: number) => (
             <div key={i} className="flex justify-between items-center bg-slate-950/50 p-3 rounded border border-white/5">
                <span className="font-bold text-slate-200">{mate.name}</span>
                <span className="text-xs text-green-400 font-mono bg-green-500/10 px-2 py-1 rounded">{mate.count} Wins</span>
             </div>
          ))}
          <div className="mt-4 text-center text-xs text-slate-500 uppercase">
            Based on {stats.total_wins} Wins
          </div>
        </div>
      ) : (
        <div className="text-slate-500 text-sm italic">Lade Match-Daten...</div>
      )}
    </div>
  );
}
