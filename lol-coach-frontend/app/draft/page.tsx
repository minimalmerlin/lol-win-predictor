'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ArrowLeft, TrendingUp, Users, AlertTriangle, Target, ShoppingBag, Sparkles } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { getChampionImageUrl, getItemImageUrl, getItemNameSync } from '@/lib/riot-data';
import ChampionSearch from '@/components/ChampionSearch';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

const ROLES = ['Top', 'Jungle', 'Mid', 'ADC', 'Support'];

interface ChampionSlot {
  champion: string | null;
  role: string;
}

interface PredictionResult {
  blue_win_probability: number;
  red_win_probability: number;
  confidence: string;
  prediction: string;
  details: {
    blue_avg_winrate: number;
    red_avg_winrate: number;
  };
}

interface ItemBuild {
  core_items: number[];
  situational_items: {
    vs_ap_heavy?: number[];
    vs_ad_heavy?: number[];
    vs_healers?: number[];
    when_ahead?: number[];
    when_behind?: number[];
  };
  early_game: number[];
  mid_game: number[];
  late_game: number[];
  explanation: string;
}

export default function DraftAssistantPage() {
  const router = useRouter();

  const [blueTeam, setBlueTeam] = useState<ChampionSlot[]>(
    ROLES.map(role => ({ champion: null, role }))
  );
  const [redTeam, setRedTeam] = useState<ChampionSlot[]>(
    ROLES.map(role => ({ champion: null, role }))
  );

  const [userSlot, setUserSlot] = useState<number>(0); // Which blue team slot is the user
  const [selectedTeam, setSelectedTeam] = useState<'blue' | 'red' | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [itemBuild, setItemBuild] = useState<ItemBuild | null>(null);
  const [loading, setLoading] = useState(false);
  const [buildLoading, setBuildLoading] = useState(false);

  // Auto-predict when both teams have at least 1 champion
  useEffect(() => {
    const blueChamps = blueTeam.filter(s => s.champion).map(s => s.champion!);
    const redChamps = redTeam.filter(s => s.champion).map(s => s.champion!);

    if (blueChamps.length > 0 && redChamps.length > 0) {
      predictMatchup(blueChamps, redChamps);
    } else {
      setPrediction(null);
    }
  }, [blueTeam, redTeam]);

  const predictMatchup = async (blueChamps: string[], redChamps: string[]) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/predict-champion-matchup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          blue_champions: blueChamps,
          red_champions: redChamps
        })
      });

      if (response.ok) {
        const data = await response.json();
        setPrediction(data);
      }
    } catch (error) {
      console.error('Failed to predict:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateDynamicBuild = async () => {
    const userChampion = blueTeam[userSlot];
    if (!userChampion.champion) {
      alert('Please select your champion first!');
      return;
    }

    // Check if we have enough champions
    const blueChamps = blueTeam.filter(s => s.champion);
    const redChamps = redTeam.filter(s => s.champion);

    if (blueChamps.length < 5 || redChamps.length < 5) {
      alert('Please select all champions for both teams!');
      return;
    }

    setBuildLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/draft/dynamic-build`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_champion: userChampion.champion,
          user_role: userChampion.role,
          ally_champions: blueTeam.filter((_, i) => i !== userSlot).map(s => s.champion),
          ally_roles: blueTeam.filter((_, i) => i !== userSlot).map(s => s.role),
          enemy_champions: redTeam.map(s => s.champion),
          enemy_roles: redTeam.map(s => s.role),
          game_state: 'even'
        })
      });

      if (response.ok) {
        const data = await response.json();
        setItemBuild(data);
      } else {
        alert('Failed to generate build recommendation');
      }
    } catch (error) {
      console.error('Failed to generate build:', error);
      alert('Error generating build');
    } finally {
      setBuildLoading(false);
    }
  };

  const handleSlotClick = (team: 'blue' | 'red', slot: number) => {
    setSelectedTeam(team);
    setSelectedSlot(slot);
  };

  const handleChampionSelect = (championName: string) => {
    if (selectedTeam && selectedSlot !== null) {
      if (selectedTeam === 'blue') {
        const newTeam = [...blueTeam];
        newTeam[selectedSlot] = { ...newTeam[selectedSlot], champion: championName };
        setBlueTeam(newTeam);
      } else {
        const newTeam = [...redTeam];
        newTeam[selectedSlot] = { ...newTeam[selectedSlot], champion: championName };
        setRedTeam(newTeam);
      }
      setSelectedTeam(null);
      setSelectedSlot(null);
    }
  };

  const handleRoleChange = (team: 'blue' | 'red', slot: number, role: string) => {
    if (team === 'blue') {
      const newTeam = [...blueTeam];
      newTeam[slot] = { ...newTeam[slot], role };
      setBlueTeam(newTeam);
    } else {
      const newTeam = [...redTeam];
      newTeam[slot] = { ...newTeam[slot], role };
      setRedTeam(newTeam);
    }
  };

  const handleClearSlot = (team: 'blue' | 'red', slot: number) => {
    if (team === 'blue') {
      const newTeam = [...blueTeam];
      newTeam[slot] = { champion: null, role: newTeam[slot].role };
      setBlueTeam(newTeam);
    } else {
      const newTeam = [...redTeam];
      newTeam[slot] = { champion: null, role: newTeam[slot].role };
      setRedTeam(newTeam);
    }
  };

  const handleReset = () => {
    setBlueTeam(ROLES.map(role => ({ champion: null, role })));
    setRedTeam(ROLES.map(role => ({ champion: null, role })));
    setPrediction(null);
    setItemBuild(null);
  };

  const getWinRateColor = (probability: number) => {
    if (probability >= 0.60) return 'text-green-400';
    if (probability >= 0.50) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getWinRateBg = (probability: number) => {
    if (probability >= 0.60) return 'bg-green-500/20 border-green-500/50';
    if (probability >= 0.50) return 'bg-yellow-500/20 border-yellow-500/50';
    return 'bg-red-500/20 border-red-500/50';
  };

  const renderChampionSlot = (slot: ChampionSlot, index: number, team: 'blue' | 'red') => {
    const isUser = team === 'blue' && index === userSlot;
    const borderColor = team === 'blue' ? 'border-blue-500' : 'border-red-500';
    const bgColor = team === 'blue' ? 'bg-blue-900/20' : 'bg-red-900/20';
    const hoverBorder = team === 'blue' ? 'hover:border-blue-500' : 'hover:border-red-500';

    return (
      <div
        key={`${team}-${index}`}
        className={`
          relative p-3 rounded-lg border-2 transition-all
          ${slot.champion
            ? `${borderColor}/50 ${bgColor}`
            : `border-slate-600 bg-slate-700/30 ${hoverBorder} hover:bg-slate-700/50`
          }
          ${selectedTeam === team && selectedSlot === index ? `ring-2 ring-${team === 'blue' ? 'blue' : 'red'}-500` : ''}
          ${isUser ? 'ring-2 ring-yellow-500' : ''}
        `}
      >
        {isUser && (
          <Badge className="absolute -top-2 -right-2 bg-yellow-500 text-black z-10">
            YOU
          </Badge>
        )}

        <div className="flex items-center gap-3 mb-2">
          <div
            onClick={() => slot.champion ? null : handleSlotClick(team, index)}
            className="cursor-pointer flex-1"
          >
            {slot.champion ? (
              <div className="flex items-center gap-3">
                <div className={`relative w-12 h-12 rounded-full overflow-hidden border-2 ${borderColor} flex-shrink-0`}>
                  <Image
                    src={getChampionImageUrl(slot.champion)}
                    alt={slot.champion}
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
                <span className="font-medium text-white flex-1">{slot.champion}</span>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleClearSlot(team, index);
                  }}
                  className="text-red-400 hover:text-red-300 hover:bg-red-900/20"
                >
                  ×
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-3 text-slate-400">
                <div className="w-12 h-12 rounded-full bg-slate-700 flex items-center justify-center text-2xl">
                  +
                </div>
                <span>Pick Champion</span>
              </div>
            )}
          </div>
        </div>

        {/* Role Selector */}
        <Select value={slot.role} onValueChange={(role) => handleRoleChange(team, index, role)}>
          <SelectTrigger className="w-full bg-slate-700/50 border-slate-600 text-white">
            <SelectValue placeholder="Select role" />
          </SelectTrigger>
          <SelectContent className="bg-slate-800 border-slate-700">
            {ROLES.map(role => (
              <SelectItem key={role} value={role} className="text-white hover:bg-slate-700">
                {role}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950">
      {/* Header */}
      <header className="border-b border-blue-800/30 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Button
              variant="ghost"
              onClick={() => router.push('/')}
              className="text-slate-300 hover:text-white"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>

            <div className="flex items-center gap-2">
              <Target className="h-6 w-6 text-blue-400" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                Draft Phase Assistant
              </h1>
            </div>

            <Button
              variant="outline"
              onClick={handleReset}
              className="border-red-600/50 text-red-400 hover:bg-red-900/20"
            >
              Reset Draft
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* User Selection */}
        <Card className="mb-6 bg-slate-800/50 border-yellow-600/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-yellow-400">
              <Users className="h-5 w-5" />
              Select Your Position
            </CardTitle>
            <CardDescription>Choose which champion you will be playing</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2">
              {ROLES.map((role, index) => (
                <Button
                  key={role}
                  onClick={() => setUserSlot(index)}
                  variant={userSlot === index ? "default" : "outline"}
                  className={userSlot === index ? "bg-yellow-500 text-black hover:bg-yellow-600" : ""}
                >
                  {role}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Blue Team */}
          <Card className="bg-slate-800/50 border-blue-600/30">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-400">
                <div className="w-3 h-3 bg-blue-500 rounded-full" />
                Blue Team (Your Team)
              </CardTitle>
              <CardDescription>Click a slot to select champion</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {blueTeam.map((slot, index) => renderChampionSlot(slot, index, 'blue'))}
              </div>
            </CardContent>
          </Card>

          {/* Prediction Result */}
          <Card className="bg-slate-800/50 border-purple-600/30">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-purple-400">
                <TrendingUp className="h-5 w-5" />
                Win Probability
              </CardTitle>
              <CardDescription>AI-powered matchup analysis</CardDescription>
            </CardHeader>
            <CardContent>
              {prediction ? (
                <div className="space-y-6">
                  {/* Blue Team Prediction */}
                  <div className={`p-4 rounded-lg border-2 ${getWinRateBg(prediction.blue_win_probability)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-blue-400 font-medium">Blue Team</span>
                      <span className={`text-3xl font-bold ${getWinRateColor(prediction.blue_win_probability)}`}>
                        {(prediction.blue_win_probability * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-cyan-500 h-3 rounded-full transition-all"
                        style={{ width: `${prediction.blue_win_probability * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Red Team Prediction */}
                  <div className={`p-4 rounded-lg border-2 ${getWinRateBg(prediction.red_win_probability)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-red-400 font-medium">Red Team</span>
                      <span className={`text-3xl font-bold ${getWinRateColor(prediction.red_win_probability)}`}>
                        {(prediction.red_win_probability * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-red-500 to-orange-500 h-3 rounded-full transition-all"
                        style={{ width: `${prediction.red_win_probability * 100}%` }}
                      />
                    </div>
                  </div>

                  <Separator className="bg-slate-700" />

                  {/* Prediction Details */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Confidence:</span>
                      <Badge className={`
                        ${prediction.confidence === 'High' ? 'bg-green-600' : ''}
                        ${prediction.confidence === 'Medium' ? 'bg-yellow-600' : ''}
                        ${prediction.confidence === 'Low' ? 'bg-red-600' : ''}
                      `}>
                        {prediction.confidence}
                      </Badge>
                    </div>

                    <div className="p-3 bg-slate-700/50 rounded-lg">
                      <p className="text-sm text-slate-300">
                        <AlertTriangle className="inline h-4 w-4 mr-1 text-yellow-400" />
                        {prediction.prediction}
                      </p>
                    </div>

                    {prediction.details && (
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div className="p-2 bg-blue-900/20 rounded border border-blue-500/30">
                          <div className="text-blue-400">Blue Avg WR</div>
                          <div className="text-white font-bold">
                            {(prediction.details.blue_avg_winrate * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="p-2 bg-red-900/20 rounded border border-red-500/30">
                          <div className="text-red-400">Red Avg WR</div>
                          <div className="text-white font-bold">
                            {(prediction.details.red_avg_winrate * 100).toFixed(1)}%
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Build Recommendation Button */}
                    <Button
                      onClick={generateDynamicBuild}
                      disabled={buildLoading || !blueTeam.every(s => s.champion) || !redTeam.every(s => s.champion)}
                      className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                    >
                      <Sparkles className="mr-2 h-4 w-4" />
                      {buildLoading ? 'Generating...' : 'Get AI Build Recommendation'}
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-slate-400">
                  <Target className="h-16 w-16 mx-auto mb-4 opacity-50" />
                  <p>Select champions for both teams to see prediction</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Red Team */}
          <Card className="bg-slate-800/50 border-red-600/30">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-red-400">
                <div className="w-3 h-3 bg-red-500 rounded-full" />
                Red Team (Enemy Team)
              </CardTitle>
              <CardDescription>Click a slot to select champion</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {redTeam.map((slot, index) => renderChampionSlot(slot, index, 'red'))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Item Build Display */}
        {itemBuild && (
          <Card className="mt-6 bg-slate-800/50 border-purple-600/30">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-purple-400">
                <ShoppingBag className="h-5 w-5" />
                AI-Generated Build for {blueTeam[userSlot].champion} ({blueTeam[userSlot].role})
              </CardTitle>
              <CardDescription>{itemBuild.explanation}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Core Items */}
              <div>
                <h3 className="text-lg font-bold text-green-400 mb-3">Core Items (Always Buy)</h3>
                <div className="flex flex-wrap gap-3">
                  {itemBuild.core_items.map(itemId => (
                    <div key={itemId} className="group relative">
                      <div className="w-16 h-16 rounded-lg overflow-hidden border-2 border-green-500/50 bg-slate-700">
                        <Image
                          src={getItemImageUrl(itemId)}
                          alt={getItemNameSync(itemId)}
                          width={64}
                          height={64}
                          className="object-cover"
                          unoptimized
                        />
                      </div>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                        {getItemNameSync(itemId)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Timeline */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Early Game */}
                <div>
                  <h3 className="text-sm font-bold text-blue-400 mb-2">Early Game (0-10 min)</h3>
                  <div className="flex flex-wrap gap-2">
                    {itemBuild.early_game.map(itemId => (
                      <div key={itemId} className="group relative">
                        <div className="w-12 h-12 rounded overflow-hidden border border-blue-500/30 bg-slate-700">
                          <Image
                            src={getItemImageUrl(itemId)}
                            alt={getItemNameSync(itemId)}
                            width={48}
                            height={48}
                            className="object-cover"
                            unoptimized
                          />
                        </div>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                          {getItemNameSync(itemId)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Mid Game */}
                <div>
                  <h3 className="text-sm font-bold text-yellow-400 mb-2">Mid Game (10-25 min)</h3>
                  <div className="flex flex-wrap gap-2">
                    {itemBuild.mid_game.map(itemId => (
                      <div key={itemId} className="group relative">
                        <div className="w-12 h-12 rounded overflow-hidden border border-yellow-500/30 bg-slate-700">
                          <Image
                            src={getItemImageUrl(itemId)}
                            alt={getItemNameSync(itemId)}
                            width={48}
                            height={48}
                            className="object-cover"
                            unoptimized
                          />
                        </div>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                          {getItemNameSync(itemId)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Late Game */}
                <div>
                  <h3 className="text-sm font-bold text-purple-400 mb-2">Late Game (25+ min)</h3>
                  <div className="flex flex-wrap gap-2">
                    {itemBuild.late_game.map(itemId => (
                      <div key={itemId} className="group relative">
                        <div className="w-12 h-12 rounded overflow-hidden border border-purple-500/30 bg-slate-700">
                          <Image
                            src={getItemImageUrl(itemId)}
                            alt={getItemNameSync(itemId)}
                            width={48}
                            height={48}
                            className="object-cover"
                            unoptimized
                          />
                        </div>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                          {getItemNameSync(itemId)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Situational Items */}
              {Object.keys(itemBuild.situational_items).length > 0 && (
                <div>
                  <h3 className="text-lg font-bold text-orange-400 mb-3">Situational Items</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {itemBuild.situational_items.vs_ap_heavy && itemBuild.situational_items.vs_ap_heavy.length > 0 && (
                      <div>
                        <Badge className="mb-2 bg-blue-600">vs AP Heavy</Badge>
                        <div className="flex flex-wrap gap-2">
                          {itemBuild.situational_items.vs_ap_heavy.map(itemId => (
                            <div key={itemId} className="group relative">
                              <div className="w-12 h-12 rounded overflow-hidden border border-blue-500/30 bg-slate-700">
                                <Image
                                  src={getItemImageUrl(itemId)}
                                  alt={getItemNameSync(itemId)}
                                  width={48}
                                  height={48}
                                  className="object-cover"
                                  unoptimized
                                />
                              </div>
                              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                                {getItemNameSync(itemId)}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {itemBuild.situational_items.vs_ad_heavy && itemBuild.situational_items.vs_ad_heavy.length > 0 && (
                      <div>
                        <Badge className="mb-2 bg-red-600">vs AD Heavy</Badge>
                        <div className="flex flex-wrap gap-2">
                          {itemBuild.situational_items.vs_ad_heavy.map(itemId => (
                            <div key={itemId} className="group relative">
                              <div className="w-12 h-12 rounded overflow-hidden border border-red-500/30 bg-slate-700">
                                <Image
                                  src={getItemImageUrl(itemId)}
                                  alt={getItemNameSync(itemId)}
                                  width={48}
                                  height={48}
                                  className="object-cover"
                                  unoptimized
                                />
                              </div>
                              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                                {getItemNameSync(itemId)}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {itemBuild.situational_items.vs_healers && itemBuild.situational_items.vs_healers.length > 0 && (
                      <div>
                        <Badge className="mb-2 bg-purple-600">vs Healers</Badge>
                        <div className="flex flex-wrap gap-2">
                          {itemBuild.situational_items.vs_healers.map(itemId => (
                            <div key={itemId} className="group relative">
                              <div className="w-12 h-12 rounded overflow-hidden border border-purple-500/30 bg-slate-700">
                                <Image
                                  src={getItemImageUrl(itemId)}
                                  alt={getItemNameSync(itemId)}
                                  width={48}
                                  height={48}
                                  className="object-cover"
                                  unoptimized
                                />
                              </div>
                              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                                {getItemNameSync(itemId)}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {itemBuild.situational_items.when_ahead && itemBuild.situational_items.when_ahead.length > 0 && (
                      <div>
                        <Badge className="mb-2 bg-green-600">When Ahead</Badge>
                        <div className="flex flex-wrap gap-2">
                          {itemBuild.situational_items.when_ahead.map(itemId => (
                            <div key={itemId} className="group relative">
                              <div className="w-12 h-12 rounded overflow-hidden border border-green-500/30 bg-slate-700">
                                <Image
                                  src={getItemImageUrl(itemId)}
                                  alt={getItemNameSync(itemId)}
                                  width={48}
                                  height={48}
                                  className="object-cover"
                                  unoptimized
                                />
                              </div>
                              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                                {getItemNameSync(itemId)}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {itemBuild.situational_items.when_behind && itemBuild.situational_items.when_behind.length > 0 && (
                      <div>
                        <Badge className="mb-2 bg-yellow-600">When Behind</Badge>
                        <div className="flex flex-wrap gap-2">
                          {itemBuild.situational_items.when_behind.map(itemId => (
                            <div key={itemId} className="group relative">
                              <div className="w-12 h-12 rounded overflow-hidden border border-yellow-500/30 bg-slate-700">
                                <Image
                                  src={getItemImageUrl(itemId)}
                                  alt={getItemNameSync(itemId)}
                                  width={48}
                                  height={48}
                                  className="object-cover"
                                  unoptimized
                                />
                              </div>
                              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                                {getItemNameSync(itemId)}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Champion Selector Modal */}
        {selectedTeam && selectedSlot !== null && (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <Card className="w-full max-w-2xl bg-slate-800 border-blue-600/30">
              <CardHeader>
                <CardTitle className="text-blue-400">
                  Select Champion for {selectedTeam === 'blue' ? 'Blue' : 'Red'} Team - {
                    selectedTeam === 'blue' ? blueTeam[selectedSlot].role : redTeam[selectedSlot].role
                  }
                </CardTitle>
                <CardDescription>Search and select a champion</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ChampionSearch onSelect={handleChampionSelect} />

                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSelectedTeam(null);
                      setSelectedSlot(null);
                    }}
                  >
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
