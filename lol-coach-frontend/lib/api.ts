// API Configuration and Client
// Empty string uses relative paths (same domain), perfect for Next.js API routes
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';
// ⚠️  SECURITY: API Key should be set via environment variable, not hardcoded
const API_KEY = process.env.NEXT_PUBLIC_INTERNAL_API_KEY || '';
if (!API_KEY && process.env.NODE_ENV === 'production') {
  console.error('⚠️  WARNING: NEXT_PUBLIC_INTERNAL_API_KEY not set in production!');
}

// Helper to get headers with API key
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'X-INTERNAL-API-KEY': API_KEY,
});

export interface Champion {
  name: string;
  games: number;
  wins: number;
  losses: number;
  win_rate: number;
  roles?: Record<string, number>;
}

export interface ChampionMatchupPrediction {
  blue_win_probability: number;
  red_win_probability: number;
  prediction: string;
  confidence: string;
  details?: {
    blue_avg_winrate: number;
    red_avg_winrate: number;
    model: string;
    accuracy: string;
  };
}

export interface ItemRecommendation {
  item_id: number;
  games: number;
  wins: number;
  win_rate: number;
}

export interface ItemBuild {
  items: number[];
  games: number;
  wins: number;
  win_rate: number;
}

export interface ItemRecommendationResponse {
  champion: string;
  recommended_items: ItemRecommendation[];
  popular_builds: ItemBuild[];
}

// API Client
export const api = {
  // Get all champions list
  async getChampionsList(): Promise<string[]> {
    const res = await fetch(`${API_BASE_URL}/api/champions/list`);
    if (!res.ok) throw new Error('Failed to fetch champions');
    const data = await res.json();
    return data.champions;
  },

  // Get champion statistics
  async getChampionStats(params?: {
    min_games?: number;
    sort_by?: string;
    limit?: number;
  }): Promise<{ champions: Champion[]; total_champions: number }> {
    const query = new URLSearchParams(
      params as Record<string, string>
    ).toString();
    const res = await fetch(`${API_BASE_URL}/api/champion-stats?${query}`);
    if (!res.ok) throw new Error('Failed to fetch champion stats');
    return res.json();
  },

  // Predict champion matchup
  async predictChampionMatchup(
    blueChampions: string[],
    redChampions: string[]
  ): Promise<ChampionMatchupPrediction> {
    const res = await fetch(`${API_BASE_URL}/api/predict-champion-matchup`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        blue_champions: blueChampions,
        red_champions: redChampions,
      }),
    });
    if (!res.ok) throw new Error('Failed to predict matchup');
    return res.json();
  },

  // Get item recommendations
  async getItemRecommendations(
    champion: string,
    enemyTeam: string[],
    topN: number = 5
  ): Promise<ItemRecommendationResponse> {
    const res = await fetch(`${API_BASE_URL}/api/item-recommendations`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        champion,
        enemy_team: enemyTeam,
        top_n: topN,
      }),
    });
    if (!res.ok) throw new Error('Failed to fetch item recommendations');
    return res.json();
  },

  // Health check
  async healthCheck(): Promise<{
    status: string;
    models_loaded: Record<string, boolean>;
  }> {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error('API health check failed');
    return res.json();
  },
};
