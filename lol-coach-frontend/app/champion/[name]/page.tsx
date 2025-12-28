"use client";
import { useEffect, useState } from 'react';
import { getChampionDetailByName, getLatestVersion, getSpellImageUrl, getPassiveImageUrl } from '@/lib/riot-data';

export default function Page({ params }: { params: { name: string } }) {
  const [c, setC] = useState<any>(null);
  const [s, setS] = useState<any>(null);
  const [v, setV] = useState("14.1.1");
  const name = decodeURIComponent(params.name);

  useEffect(() => {
    getLatestVersion().then(setV);
    getChampionDetailByName(name).then(setC);
    fetch('/data/champion_stats.json').then(r => r.json()).then(d => {
       // Check both name and ID mapping
       if(d[name]) setS(d[name]);
    }).catch(() => {});
  }, [name]);

  if (!c) return <div className="p-10 text-white">Loading {name}...</div>;

  return (
    <div className="min-h-screen bg-[#00030C] text-slate-200 p-8">
      <div className="flex gap-8 mb-8">
        <img src={`https://ddragon.leagueoflegends.com/cdn/img/champion/loading/${c.id}_0.jpg`} className="rounded-xl border-2 border-slate-700"/>
        <div>
           <h1 className="text-6xl font-bold text-white">{c.name}</h1>
           <p className="text-xl text-blue-400 italic">{c.title}</p>
           <p className="mt-4 text-slate-400 max-w-2xl">{c.lore}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-slate-900 p-6 rounded border border-slate-800">
           <h3 className="text-blue-400 font-bold mb-4">DATA INSIGHTS</h3>
           {s ? s.best_teammates.map((m: any) => (
             <div key={m.name} className="flex justify-between border-b border-slate-800 py-2">
               <span>{m.name}</span> <span className="text-green-400">{m.count} Wins</span>
             </div>
           )) : "No data available."}
        </div>
        <div className="bg-slate-900 p-6 rounded border border-slate-800">
           <h3 className="text-blue-400 font-bold mb-4">ABILITIES</h3>
           <div className="flex gap-2">
             <img src={getPassiveImageUrl(c.passive.image.full, v)} className="w-12 h-12 rounded"/>
             {c.spells.map((sp: any) => <img key={sp.id} src={getSpellImageUrl(sp.image.full, v)} className="w-12 h-12 rounded"/>)}
           </div>
        </div>
      </div>
    </div>
  );
}
