/**
 * Riot Data Dragon Asset URLs (Dynamic Wrapper)
 * ==============================================
 *
 * This file wraps the dynamic riot-data.ts API for backward compatibility.
 * All data is fetched automatically from Riot's API - no manual updates needed!
 *
 * MIGRATION NOTE: This is a compatibility layer. New code should use riot-data.ts directly.
 *
 * Docs: https://developer.riotgames.com/docs/lol#data-dragon
 */

import {
  getLatestVersion,
  getChampionIdByName,
  getChampionImageUrl as getDynamicChampionUrl,
  getChampionSplashUrl as getDynamicSplashUrl,
  getItemImageUrl as getDynamicItemUrl,
  getItemName as getDynamicItemName,
} from './riot-data';

// Cache the version for synchronous access
let cachedVersion = '14.24.1';

// Initialize version on module load
getLatestVersion().then(v => {
  cachedVersion = v;
  console.log(`🎮 Riot Data Dragon v${v} loaded`);
});

/**
 * Champion Portrait URL (Synchronous wrapper)
 * Uses cached version - automatically updates every hour
 * @param championName - Champion name (e.g., "Thresh", "Master Yi")
 * @returns URL to champion portrait image
 */
export function getChampionImageUrl(championName: string): string {
  // Handle name variations synchronously with best-effort mapping
  const nameMapping: Record<string, string> = {
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

  const mappedName = nameMapping[championName] || championName.replace(/\s/g, '');
  return getDynamicChampionUrl(mappedName, cachedVersion);
}

/**
 * Champion Splash Art URL
 * @param championName - Champion name
 * @returns URL to champion splash art
 */
export function getChampionSplashUrl(championName: string): string {
  const nameMapping: Record<string, string> = {
    'Miss Fortune': 'MissFortune',
    'Dr. Mundo': 'DrMundo',
    'Jarvan IV': 'JarvanIV',
    "Kha'Zix": 'Khazix',
    "Kog'Maw": 'KogMaw',
    'Lee Sin': 'LeeSin',
    'Master Yi': 'MasterYi',
    'Wukong': 'MonkeyKing',
    "Rek'Sai": 'RekSai',
    'Tahm Kench': 'TahmKench',
    'Twisted Fate': 'TwistedFate',
    "Vel'Koz": 'Velkoz',
    'Xin Zhao': 'XinZhao',
    "Cho'Gath": 'Chogath',
    'Aurelion Sol': 'AurelionSol',
  };

  const mappedName = nameMapping[championName] || championName.replace(/\s/g, '');
  return getDynamicSplashUrl(mappedName);
}

/**
 * Item Image URL
 * @param itemId - Item ID (e.g., 3003, 6653)
 * @returns URL to item image
 */
export function getItemImageUrl(itemId: number): string {
  return getDynamicItemUrl(itemId, cachedVersion);
}

/**
 * Get Item Name (Async)
 * Fetches the current item name from Riot's API
 * @param itemId - Item ID
 * @returns Promise with item name
 */
export async function getItemName(itemId: number): Promise<string> {
  return getDynamicItemName(itemId);
}

/**
 * DEPRECATED: Static item names mapping
 * This is kept for backward compatibility but may be outdated.
 * Use getItemName(itemId) instead for always-current data.
 */
export const ITEM_NAMES: Record<number, string> = {
  // Common consumables (rarely change)
  2003: "Health Potion",
  2031: "Refillable Potion",
  2033: "Corrupting Potion",
  2055: "Control Ward",

  // Boots (stable items)
  3006: "Berserker's Greaves",
  3009: "Boots of Swiftness",
  3020: "Sorcerer's Shoes",
  3047: "Plated Steelcaps",
  3111: "Mercury's Treads",
  3117: "Mobility Boots",
  3158: "Ionian Boots of Lucidity",

  // NOTE: Full item list is fetched dynamically from Riot API
  // Use getItemName(itemId) for accurate, up-to-date names
};

/**
 * Get Champion Image with fallback
 * @param championName - Champion name
 * @returns Object with URL and fallback handler
 */
export function getChampionImageWithFallback(championName: string) {
  return {
    url: getChampionImageUrl(championName),
    onError: (e: any) => {
      e.target.src = `https://via.placeholder.com/120x120/1e293b/60a5fa?text=${championName.substring(0, 2)}`;
    }
  };
}

/**
 * Get Item Image with fallback
 * @param itemId - Item ID
 * @returns Object with URL, name, and fallback handler
 */
export function getItemImageWithFallback(itemId: number) {
  return {
    url: getItemImageUrl(itemId),
    name: ITEM_NAMES[itemId] || `Item ${itemId}`,
    onError: (e: any) => {
      e.target.src = `https://via.placeholder.com/64x64/334155/94a3b8?text=${itemId}`;
    }
  };
}

/**
 * Re-export dynamic functions for direct use
 */
export {
  getLatestVersion,
  getChampionIdByName,
} from './riot-data';

export type { ChampionDto, ItemDto } from './riot-data';
