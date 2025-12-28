'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Search, ExternalLink } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface SearchResult {
  name: string;
  id: string; // Riot champion ID for proper navigation (e.g. "MonkeyKing" instead of "Wukong")
  similarity: number;
  match_quality: string;
  has_builds: boolean;
  stats?: {
    games: number;
    win_rate: number;
  };
}

interface ChampionSearchProps {
  onSelect?: (championName: string) => void;
}

export default function ChampionSearch({ onSelect }: ChampionSearchProps = {}) {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const searchChampions = useCallback(async (searchQuery: string) => {
    if (!searchQuery || searchQuery.length < 2) {
      setResults([]);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${API_URL}/api/champions/search?query=${encodeURIComponent(searchQuery)}&limit=10&include_stats=true`
      );

      if (response.ok) {
        const data = await response.json();
        setResults(data.results || []);
      }
    } catch (error) {
      console.error('Failed to search champions:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      searchChampions(query);
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [query, searchChampions]);

  const handleSelect = (championId: string, championName: string) => {
    if (onSelect) {
      onSelect(championName); // Callback still gets the name for compatibility
    } else {
      router.push(`/champion/${championId}`); // Navigation uses ID
    }
    setQuery('');
    setIsOpen(false);
  };

  const getMatchQualityBadge = (quality: string) => {
    if (quality === 'exact') return <Badge className="bg-green-600 text-xs">Exact</Badge>;
    if (quality === 'good') return <Badge className="bg-blue-600 text-xs">Good</Badge>;
    return <Badge className="bg-yellow-600 text-xs">Partial</Badge>;
  };

  return (
    <div className="relative w-full max-w-md">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
        <Input
          placeholder="Search champions... (fuzzy search)"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          onBlur={() => setTimeout(() => setIsOpen(false), 200)}
          className="pl-10 bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400"
        />
      </div>

      {/* Results Dropdown */}
      {isOpen && results.length > 0 && (
        <Card className="absolute z-[9999] w-full mt-2 bg-slate-800 border-blue-700/30 shadow-xl max-h-96 overflow-y-auto">
          <div className="p-2 space-y-1">
            {results.map((result) => (
              <div
                key={result.id}
                onClick={() => handleSelect(result.id, result.name)}
                className="p-3 rounded-lg hover:bg-slate-700/50 cursor-pointer transition-colors group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-white font-medium group-hover:text-blue-400 transition-colors">
                      {result.name}
                    </span>
                    {getMatchQualityBadge(result.match_quality)}
                    <ExternalLink className="h-3 w-3 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <div className="text-xs text-slate-400">
                    {(result.similarity * 100).toFixed(0)}% match
                  </div>
                </div>
                {result.stats && (
                  <div className="text-xs text-slate-400 mt-1">
                    {result.stats.games} games | {(result.stats.win_rate * 100).toFixed(1)}% WR
                  </div>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* No Results */}
      {isOpen && query.length >= 2 && !loading && results.length === 0 && (
        <Card className="absolute z-[9999] w-full mt-2 bg-slate-800 border-blue-700/30 shadow-xl">
          <div className="p-4 text-center text-slate-400 text-sm">
            No champions found for "{query}"
          </div>
        </Card>
      )}
    </div>
  );
}
