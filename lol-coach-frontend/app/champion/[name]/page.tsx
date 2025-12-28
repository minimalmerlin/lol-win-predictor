import { getChampionDetailByName, getLatestVersion, getSpellImageUrl, getPassiveImageUrl } from '@/lib/riot-data';
import Link from 'next/link';

// Helper um Daten zu fetchen (Server Component Pattern)
async function getData(name: string) {
  const version = await getLatestVersion();
  const champion = await getChampionDetailByName(name);
  return { version, champion };
}

// Next.js 16: params ist ein Promise!
export default async function ChampionPage({ params }: { params: Promise<{ name: string }> }) {
  // 1. Params auflösen
  const resolvedParams = await params;
  const champName = decodeURIComponent(resolvedParams.name);

  // 2. Daten laden
  const { version, champion } = await getData(champName);

  // 3. Stats client-side fetchen (optionaler Hydration Part wäre besser, aber wir machen es simpel via fetch im Render ist bei Server Components nicht möglich, daher hier Error Handling)
  // Hinweis: Für echte Stats müssten wir das hier zu einer Client Component machen oder fetch() serverseitig erlauben.
  // Wir nutzen hier eine Hybrid-Lösung: Server Component rendert Static Content, Client Wrapper könnte Stats holen.
  // Für jetzt: Wir zeigen erst mal den Static Content, damit die Seite nicht crasht.

  if (!champion) {
    return (
      <div className="min-h-screen bg-[#00030C] text-white flex flex-col items-center justify-center">
        <h1 className="text-4xl text-red-500">404</h1>
        <p>Champion "{champName}" nicht gefunden.</p>
        <Link href="/" className="text-blue-400 mt-4">Zurück</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#00030C] text-slate-200 pb-20 font-sans">
      {/* Hero */}
      <div className="relative h-[50vh] w-full">
        <div className="absolute inset-0 bg-gradient-to-t from-[#00030C] to-transparent z-10" />
        <img
          src={`https://ddragon.leagueoflegends.com/cdn/img/champion/splash/${champion.id}_0.jpg`}
          className="w-full h-full object-cover opacity-60"
          alt={champion.name}
        />
        <div className="absolute bottom-10 left-10 z-20">
          <h1 className="text-7xl font-black text-white uppercase">{champion.name}</h1>
          <p className="text-2xl text-[#1E90FF] italic">{champion.title}</p>
        </div>
        <Link href="/" className="absolute top-8 left-8 z-30 px-4 py-2 bg-black/50 border border-white/20 rounded text-white">
          ← BACK
        </Link>
      </div>

      <div className="max-w-7xl mx-auto px-8 grid grid-cols-1 lg:grid-cols-3 gap-12 -mt-10 relative z-20">
        {/* Lore & Spells */}
        <div className="lg:col-span-2 space-y-8">
           <div className="bg-slate-900/80 p-6 rounded-xl border border-slate-800 backdrop-blur">
             <h3 className="text-[#1E90FF] font-bold mb-4">LORE</h3>
             <p className="text-slate-300 leading-relaxed">{champion.lore}</p>
           </div>

           <div className="bg-slate-900/80 p-6 rounded-xl border border-slate-800 backdrop-blur">
             <h3 className="text-[#1E90FF] font-bold mb-4">ABILITIES</h3>
             <div className="flex gap-4 overflow-x-auto pb-2">
               <img src={getPassiveImageUrl(champion.passive.image.full, version)} className="w-16 h-16 rounded border border-slate-600" title="Passive" alt="Passive" />
               {champion.spells.map(spell => (
                 <img key={spell.id} src={getSpellImageUrl(spell.image.full, version)} className="w-16 h-16 rounded border border-slate-600" title={spell.name} alt={spell.name} />
               ))}
             </div>
           </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
           <div className="bg-slate-900/80 p-6 rounded-xl border border-slate-800 backdrop-blur">
              <h3 className="text-green-400 font-bold mb-4">TIPS</h3>
              <ul className="text-sm text-slate-400 list-disc pl-4 space-y-2">
                {champion.allytips.slice(0,3).map((t, i) => <li key={i}>{t}</li>)}
              </ul>
           </div>
        </div>
      </div>
    </div>
  );
}
