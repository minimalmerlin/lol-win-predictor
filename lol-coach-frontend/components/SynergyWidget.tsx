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
    <div className="glass-card p-6">
      <h3 className="text-primary font-bold text-sm tracking-widest uppercase mb-4">Best Teammates</h3>
      {stats && stats.best_teammates && stats.best_teammates.length > 0 ? (
        <div className="space-y-2">
          {stats.best_teammates.map((mate: any, i: number) => (
             <div key={i} className="flex justify-between items-center bg-white/5 p-3 rounded-lg border border-white/10">
                <span className="font-bold text-foreground">{mate.name}</span>
                <span className="text-xs text-success font-mono bg-success/10 px-2 py-1 rounded">{mate.count} Wins</span>
             </div>
          ))}
          <div className="mt-4 text-center text-xs text-muted-foreground uppercase">
            Based on {stats.total_wins} Wins
          </div>
        </div>
      ) : stats === null ? (
        <div className="text-muted-foreground text-sm italic">Lade Match-Daten...</div>
      ) : (
        <div className="text-muted-foreground text-sm">Keine Daten verfügbar</div>
      )}
    </div>
  );
}
