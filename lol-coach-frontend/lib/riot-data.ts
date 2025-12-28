/**
 * RIOT DATA SERVICE (Dynamic)
 * ===========================
 * Automatically fetches the latest patch version and correct mappings from Riot's API.
 * No manual updates needed - always stays current with the game.
 */

export interface ChampionDto {
  id: string;    // Image ID (e.g., "MonkeyKing" for Wukong)
  key: string;   // Numeric ID (e.g., "62")
  name: string;  // Display name (e.g., "Wukong")
  title: string;
  image: {
    full: string;
  };
  tags: string[];
}

export interface ItemDto {
  name: string;
  description: string;
  plaintext: string;
  image: {
    full: string;
  };
  gold: {
    total: number;
  };
  tags: string[];
}

// Cache variables (so we don't fetch on every click)
let cachedVersion: string | null = null;
let cachedChampions: ChampionDto[] | null = null;
let cachedItems: Map<string, ItemDto> | null = null;
const CACHE_DURATION = 3600000; // 1 hour in milliseconds
let lastFetch = 0;

/**
 * Fetches the latest LoL version (e.g., "14.24.1")
 * Cached for 1 hour to reduce API calls
 */
export async function getLatestVersion(): Promise<string> {
  const now = Date.now();

  if (cachedVersion && now - lastFetch < CACHE_DURATION) {
    return cachedVersion;
  }

  try {
    const res = await fetch('https://ddragon.leagueoflegends.com/api/versions.json', {
      next: { revalidate: 3600 } // Next.js cache for 1 hour
    });
    const versions = await res.json();
    cachedVersion = versions[0]; // First element is always the latest patch
    lastFetch = now;
    return cachedVersion || "14.24.1";
  } catch (e) {
    console.error("Failed to fetch version:", e);
    return cachedVersion || "14.24.1"; // Fallback to cached or default
  }
}

/**
 * Fetches ALL current champions directly from Riot
 * Solves the "Wukong vs. MonkeyKing" problem automatically
 */
export async function getLatestChampionData() {
  const now = Date.now();
  const version = await getLatestVersion();

  if (cachedChampions && now - lastFetch < CACHE_DURATION) {
    return { version, champions: cachedChampions };
  }

  try {
    const res = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/champion.json`, {
      next: { revalidate: 3600 }
    });
    const json = await res.json();

    // Convert object { "Aatrox": {...}, "Ahri": {...} } to array
    const champions: ChampionDto[] = Object.values(json.data);

    cachedChampions = champions;
    return { version, champions };
  } catch (e) {
    console.error("Failed to fetch champions:", e);
    return {
      version,
      champions: cachedChampions || []
    };
  }
}

/**
 * Fetches ALL current items directly from Riot
 * No more outdated Mythic items!
 */
export async function getLatestItemData() {
  const now = Date.now();
  const version = await getLatestVersion();

  if (cachedItems && now - lastFetch < CACHE_DURATION) {
    return { version, items: cachedItems };
  }

  try {
    const res = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/item.json`, {
      next: { revalidate: 3600 }
    });
    const json = await res.json();

    // Convert to Map for easy lookup
    const itemsMap = new Map<string, ItemDto>();
    Object.entries(json.data).forEach(([id, item]) => {
      itemsMap.set(id, item as ItemDto);
    });

    cachedItems = itemsMap;
    return { version, items: cachedItems };
  } catch (e) {
    console.error("Failed to fetch items:", e);
    return {
      version,
      items: cachedItems || new Map()
    };
  }
}

/**
 * Find champion by name (handles name variations)
 * Returns the correct image ID
 */
export async function getChampionIdByName(name: string): Promise<string | null> {
  const { champions } = await getLatestChampionData();

  // Normalize name for comparison
  const normalized = name.toLowerCase().replace(/['\s]/g, '');

  const champion = champions.find(c =>
    c.name.toLowerCase().replace(/['\s]/g, '') === normalized ||
    c.id.toLowerCase() === normalized
  );

  return champion?.id || null;
}

/**
 * URL Helpers
 */

// Synchronous cached version for immediate use
let syncCachedVersion = '14.24.1';

// Update sync cache when version is fetched
getLatestVersion().then(v => {
  syncCachedVersion = v;
  console.log(`🎮 Riot Data Dragon v${v} loaded`);
});

// Champion name mapping for common variations
const CHAMPION_NAME_MAP: Record<string, string> = {
  'MissFortune': 'MissFortune',
  'Miss Fortune': 'MissFortune',
  'DrMundo': 'DrMundo',
  'Dr. Mundo': 'DrMundo',
  'Dr Mundo': 'DrMundo',
  'JarvanIV': 'JarvanIV',
  'Jarvan IV': 'JarvanIV',
  'KhaZix': 'Khazix',
  "Kha'Zix": 'Khazix',
  'KogMaw': 'KogMaw',
  "Kog'Maw": 'KogMaw',
  'LeBlanc': 'Leblanc',
  'LeeSin': 'LeeSin',
  'Lee Sin': 'LeeSin',
  'MasterYi': 'MasterYi',
  'Master Yi': 'MasterYi',
  'MonkeyKing': 'MonkeyKing',
  'Wukong': 'MonkeyKing',
  'RekSai': 'RekSai',
  "Rek'Sai": 'RekSai',
  'TahmKench': 'TahmKench',
  'Tahm Kench': 'TahmKench',
  'TwistedFate': 'TwistedFate',
  'Twisted Fate': 'TwistedFate',
  'VelKoz': 'Velkoz',
  "Vel'Koz": 'Velkoz',
  'XinZhao': 'XinZhao',
  'Xin Zhao': 'XinZhao',
  "Cho'Gath": 'Chogath',
  'ChoGath': 'Chogath',
  'AurelionSol': 'AurelionSol',
  'Aurelion Sol': 'AurelionSol',
};

/**
 * Get champion image URL (synchronous - uses cached version)
 * Handles name variations automatically
 */
export function getChampionImageUrl(championName: string): string {
  const mappedName = CHAMPION_NAME_MAP[championName] || championName.replace(/\s/g, '');
  return `https://ddragon.leagueoflegends.com/cdn/${syncCachedVersion}/img/champion/${mappedName}.png`;
}

/**
 * Get champion splash art URL (synchronous)
 */
export function getChampionSplashUrl(championName: string): string {
  const mappedName = CHAMPION_NAME_MAP[championName] || championName.replace(/\s/g, '');
  return `https://ddragon.leagueoflegends.com/cdn/img/champion/splash/${mappedName}_0.jpg`;
}

/**
 * Get item image URL (synchronous - uses cached version)
 */
export function getItemImageUrl(itemId: number | string): string {
  return `https://ddragon.leagueoflegends.com/cdn/${syncCachedVersion}/img/item/${itemId}.png`;
}

/**
 * Get item name from ID (dynamic, always current)
 */
export async function getItemName(itemId: number | string): Promise<string> {
  const { items } = await getLatestItemData();
  const item = items.get(String(itemId));
  return item?.name || `Item ${itemId}`;
}

/**
 * Get item name synchronously (may not have latest data immediately)
 */
export function getItemNameSync(itemId: number | string): string {
  if (cachedItems) {
    const item = cachedItems.get(String(itemId));
    if (item) return item.name;
  }
  return `Item ${itemId}`;
}

/**
 * Clear cache (useful for manual refresh)
 */
export function clearCache() {
  cachedVersion = null;
  cachedChampions = null;
  cachedItems = null;
  lastFetch = 0;
}