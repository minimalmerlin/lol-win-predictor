import { getChampionDetailByName, getLatestVersion, getSpellImageUrl, getPassiveImageUrl } from '@/lib/riot-data';
import { SynergyWidget } from '@/components/SynergyWidget';
import Link from 'next/link';

// Helper für Data Fetching
async function getData(name: string) {
  const version = await getLatestVersion();
  const champion = await getChampionDetailByName(name);
  return { version, champion };
}

export default async function ChampionPage({ params }: { params: Promise<{ name: string }> }) {
  // Next.js 16: Params awaiten
  const resolvedParams = await params;
  const champName = decodeURIComponent(resolvedParams.name);
  const { version, champion } = await getData(champName);

  if (!champion) return <div className="p-20 text-center text-white">Champion nicht gefunden</div>;

  return (
    <div className="min-h-screen bg-[#00030C] text-slate-200 font-sans pb-20">

      {/* 1. HERO & IDENTITY */}
      <div className="relative w-full h-[500px]">
        <div className="absolute inset-0 bg-gradient-to-t from-[#00030C] via-[#00030C]/50 to-transparent z-10" />
        <img
          src={`https://ddragon.leagueoflegends.com/cdn/img/champion/splash/${champion.id}_0.jpg`}
          className="w-full h-full object-cover object-top opacity-60"
          alt={champion.name}
        />
        <div className="absolute bottom-0 left-0 w-full p-8 z-20 bg-gradient-to-t from-[#00030C] to-transparent">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-7xl font-black text-white uppercase tracking-tighter mb-2">{champion.name}</h1>
            <p className="text-2xl text-[#1E90FF] italic font-serif mb-6">{champion.title}</p>
            <p className="max-w-3xl text-lg text-slate-300 leading-relaxed border-l-4 border-[#1E90FF] pl-6 mb-12">
              {champion.lore}
            </p>
          </div>
        </div>
        <Link href="/" className="absolute top-6 left-6 z-30 px-4 py-2 bg-slate-900/80 border border-slate-700 rounded text-sm hover:border-[#1E90FF] transition">
          ← BACK TO WAR ROOM
        </Link>
      </div>

      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-8 -mt-10 relative z-30">

        {/* LEFT COLUMN (8 cols) */}
        <div className="lg:col-span-8 space-y-8">

          {/* ABILITIES */}
          <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
            <h3 className="text-[#1E90FF] font-bold text-sm tracking-widest uppercase mb-6">Combat Abilities</h3>
            <div className="flex flex-wrap gap-6">
              <div className="text-center group">
                <img src={getPassiveImageUrl(champion.passive.image.full, version)} className="w-16 h-16 rounded-lg border-2 border-slate-600 mb-2" />
                <span className="text-xs font-bold text-slate-500">PASSIVE</span>
              </div>
              {champion.spells.map((spell, i) => (
                <div key={spell.id} className="text-center group relative">
                   <img src={getSpellImageUrl(spell.image.full, version)} className="w-16 h-16 rounded-lg border-2 border-slate-600 group-hover:border-[#1E90FF] transition mb-2" />
                   <span className="text-xs font-bold text-slate-500">{["Q","W","E","R"][i]}</span>
                   {/* Simple Tooltip */}
                   <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block w-64 bg-black p-3 text-xs rounded border border-slate-700 z-50">
                     <strong className="text-[#1E90FF] block mb-1">{spell.name}</strong>
                     {spell.description.replace(/<[^>]*>?/gm, '').substring(0, 100)}...
                   </div>
                </div>
              ))}
            </div>
          </section>

          {/* 2. STRATEGIC GUIDE (TIPS) */}
          <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
            <h3 className="text-green-400 font-bold text-sm tracking-widest uppercase mb-4">Tactical Guide</h3>
            <ul className="space-y-3">
              {champion.allytips.length > 0 ? (
                champion.allytips.map((tip, i) => (
                  <li key={i} className="flex gap-3 text-slate-300">
                    <span className="text-green-500 font-bold">✓</span>
                    <span>{tip}</span>
                  </li>
                ))
              ) : (
                <li className="text-slate-500 italic">Keine spezifischen Tipps verfügbar.</li>
              )}
            </ul>
          </section>

          {/* 4. BUILD PLACEHOLDER */}
          <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl opacity-70">
             <div className="flex justify-between items-center mb-6">
                <h3 className="text-orange-400 font-bold text-sm tracking-widest uppercase">Recommended Build</h3>
                <span className="px-2 py-1 bg-orange-500/10 text-orange-500 text-xs border border-orange-500/20 rounded">CRAWLER UPDATE NEEDED</span>
             </div>
             <div className="flex gap-4">
                {[1,2,3,4,5,6].map(i => (
                  <div key={i} className="w-16 h-16 bg-slate-950 border border-slate-800 rounded flex items-center justify-center">
                    <span className="text-slate-700 text-xs">Item {i}</span>
                  </div>
                ))}
             </div>
             <p className="mt-4 text-sm text-slate-500">
               Die Item-Daten werden im nächsten System-Update aus den 50k Matches extrahiert.
             </p>
          </section>
        </div>

        {/* RIGHT COLUMN (4 cols) */}
        <div className="lg:col-span-4 space-y-6">

          {/* 3. SYNERGIES (Client Side Load) */}
          <SynergyWidget champName={champion.name} />

          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
             <h3 className="text-red-400 font-bold text-sm tracking-widest uppercase mb-4">Counter Tips</h3>
             <ul className="space-y-3 text-sm text-slate-400">
                {champion.enemytips.slice(0,3).map((t, i) => (
                  <li key={i}>• {t}</li>
                ))}
             </ul>
          </div>
        </div>

      </div>
    </div>
  );
}
