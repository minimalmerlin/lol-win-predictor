"use client";

import { useState, useEffect } from 'react';
import { getLatestChampionData, ChampionDto } from '@/lib/riot-data';
import { ChampionCard } from '../components/ChampionCard';

export default function Home() {
  const [version, setVersion] = useState<string>("14.1.1");
  const [champions, setChampions] = useState<ChampionDto[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  
  // State für die Teams (Draft Simulation)
  const [blueTeam, setBlueTeam] = useState<ChampionDto[]>([]);
  const [redTeam, setRedTeam] = useState<ChampionDto[]>([]);
  const [prediction, setPrediction] = useState<any>(null);

  // 1. Daten beim Start laden
  useEffect(() => {
    async function loadData() {
      const data = await getLatestChampionData();
      setVersion(data.version);
      // Sortiere Champions alphabetisch
      const sorted = data.champions.sort((a, b) => a.name.localeCompare(b.name));
      setChampions(sorted);
    }
    loadData();
  }, []);

  // Filterung für Suche
  const filteredChampions = champions.filter(c => 
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Champion auswählen
  const handleSelectChampion = (champ: ChampionDto) => {
    if (blueTeam.length < 5) {
      setBlueTeam([...blueTeam, champ]);
    } else if (redTeam.length < 5) {
      setRedTeam([...redTeam, champ]);
    }
  };

  // Reset Draft
  const handleReset = () => {
    setBlueTeam([]);
    setRedTeam([]);
    setPrediction(null);
  };

  // Vorhersage anfordern (API Call zum Python Backend)
  const handlePredict = async () => {
    if (blueTeam.length !== 5 || redTeam.length !== 5) {
      alert("Beide Teams müssen 5 Champions haben!");
      return;
    }

    try {
      const res = await fetch('http://127.0.0.1:5328/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          blue_team: blueTeam.map(c => parseInt(c.key)), // IDs als Int senden
          red_team: redTeam.map(c => parseInt(c.key))
        })
      });
      
      const result = await res.json();
      setPrediction(result);
    } catch (error) {
      console.error("API Fehler:", error);
      alert("Fehler bei der Verbindung zur AI.");
    }
  };

  return (
    <main className="flex min-h-screen flex-col bg-[#00030C] text-slate-200 p-8 font-sans">
      
      {/* HEADER */}
      <div className="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
        <h1 className="text-3xl font-bold tracking-widest text-[#1E90FF]">
          WAR ROOM <span className="text-sm text-slate-500 font-normal">SYSTEM V.2.0</span>
        </h1>
        <div className="text-xs text-slate-500">
          PATCH: <span className="text-slate-300">{version}</span>
        </div>
      </div>

      {/* DRAFT BEREICH */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
        
        {/* BLUE TEAM */}
        <div className="border border-blue-900/30 bg-blue-950/10 p-4 rounded-xl">
          <h2 className="text-blue-400 font-bold mb-4">BLUE TEAM</h2>
          <div className="flex flex-wrap gap-2 min-h-[100px]">
            {blueTeam.map((c) => (
              <div key={c.id} className="relative group cursor-pointer" onClick={() => setBlueTeam(blueTeam.filter(x => x.id !== c.id))}>
                 <ChampionCard championName={c.id} version={version} />
              </div>
            ))}
            {blueTeam.length < 5 && <div className="text-slate-600 text-sm italic p-2">Wähle Champions...</div>}
          </div>
        </div>

        {/* ERGEBNIS / MITTE */}
        <div className="flex flex-col items-center justify-center space-y-4">
          <button 
            onClick={handlePredict}
            className="px-8 py-3 bg-[#1E90FF] hover:bg-blue-600 text-white font-bold rounded-none border border-blue-400 shadow-[0_0_15px_rgba(30,144,255,0.5)] transition-all"
          >
            ANALYSE STARTEN
          </button>
          
          <button onClick={handleReset} className="text-xs text-slate-500 hover:text-slate-300 underline">
            RESET DRAFT
          </button>

          {prediction && (
            <div className="mt-4 p-4 bg-slate-900 border border-[#1E90FF] w-full text-center animate-pulse">
              <div className="text-xs text-slate-400 mb-1">PREDICTED WINNER</div>
              <div className={`text-2xl font-bold ${prediction.predicted_winner === 'Blue Team' ? 'text-blue-400' : 'text-red-500'}`}>
                {prediction.predicted_winner.toUpperCase()}
              </div>
              <div className="text-sm mt-2">
                Win Probability: <span className="text-white">{prediction.blue_win_probability}%</span>
              </div>
            </div>
          )}
        </div>

        {/* RED TEAM */}
        <div className="border border-red-900/30 bg-red-950/10 p-4 rounded-xl">
          <h2 className="text-red-400 font-bold mb-4">RED TEAM</h2>
          <div className="flex flex-wrap gap-2 min-h-[100px]">
            {redTeam.map((c) => (
               <div key={c.id} className="relative group cursor-pointer" onClick={() => setRedTeam(redTeam.filter(x => x.id !== c.id))}>
                 <ChampionCard championName={c.id} version={version} />
               </div>
            ))}
            {redTeam.length < 5 && <div className="text-slate-600 text-sm italic p-2">Wähle Champions...</div>}
          </div>
        </div>
      </div>

      {/* CHAMPION SELECTOR */}
      <div className="border-t border-slate-800 pt-6">
        <input 
          type="text" 
          placeholder="Suche Champion..." 
          className="w-full max-w-md bg-slate-900 border border-slate-700 p-2 text-white mb-6 focus:border-[#1E90FF] outline-none"
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 gap-2 h-64 overflow-y-auto pr-2 custom-scrollbar">
          {filteredChampions.map((champ) => (
            <div key={champ.key} onClick={() => handleSelectChampion(champ)} className="cursor-pointer opacity-70 hover:opacity-100 hover:scale-105 transition-all">
              <ChampionCard championName={champ.id} version={version} />
            </div>
          ))}
        </div>
      </div>

    </main>
  );
}