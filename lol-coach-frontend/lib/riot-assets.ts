/**
 * Riot Data Dragon Asset URLs
 * ============================
 *
 * Offizielle Riot Games CDN für Champion- und Item-Bilder
 * Docs: https://developer.riotgames.com/docs/lol#data-dragon
 */

// Aktuellste Version (wird regelmäßig von Riot aktualisiert)
const DDRAGON_VERSION = '14.24.1'; // LoL Patch 14.24
const DDRAGON_BASE = `https://ddragon.leagueoflegends.com/cdn/${DDRAGON_VERSION}`;

/**
 * Champion Portrait URL
 * @param championName - Champion name (e.g., "Thresh", "MissFortune")
 * @returns URL to champion portrait image
 */
export function getChampionImageUrl(championName: string): string {
  // Data Dragon verwendet manchmal andere Namen
  const nameMapping: Record<string, string> = {
    'MissFortune': 'MissFortune',
    'DrMundo': 'DrMundo',
    'JarvanIV': 'JarvanIV',
    'KhaZix': 'Khazix',
    'KogMaw': 'KogMaw',
    'LeBlanc': 'Leblanc',
    'LeeSin': 'LeeSin',
    'MasterYi': 'MasterYi',
    'MonkeyKing': 'MonkeyKing', // Wukong
    'RekSai': 'RekSai',
    'TahmKench': 'TahmKench',
    'TwistedFate': 'TwistedFate',
    'VelKoz': 'Velkoz',
    'XinZhao': 'XinZhao',
    // Füge hier weitere Mappings hinzu falls nötig
  };

  const mappedName = nameMapping[championName] || championName;
  return `${DDRAGON_BASE}/img/champion/${mappedName}.png`;
}

/**
 * Champion Splash Art URL (größeres Bild)
 * @param championName - Champion name
 * @returns URL to champion splash art
 */
export function getChampionSplashUrl(championName: string): string {
  const nameMapping: Record<string, string> = {
    'MissFortune': 'MissFortune',
    'DrMundo': 'DrMundo',
    'JarvanIV': 'JarvanIV',
    'KhaZix': 'Khazix',
    'KogMaw': 'KogMaw',
    'LeBlanc': 'Leblanc',
    'LeeSin': 'LeeSin',
    'MasterYi': 'MasterYi',
    'MonkeyKing': 'MonkeyKing',
    'RekSai': 'RekSai',
    'TahmKench': 'TahmKench',
    'TwistedFate': 'TwistedFate',
    'VelKoz': 'Velkoz',
    'XinZhao': 'XinZhao',
  };

  const mappedName = nameMapping[championName] || championName;
  return `https://ddragon.leagueoflegends.com/cdn/img/champion/splash/${mappedName}_0.jpg`;
}

/**
 * Item Image URL
 * @param itemId - Item ID (e.g., 3003, 6653)
 * @returns URL to item image
 */
export function getItemImageUrl(itemId: number): string {
  return `${DDRAGON_BASE}/img/item/${itemId}.png`;
}

/**
 * Item Name Mapping
 * Mapping von Item IDs zu Namen
 */
export const ITEM_NAMES: Record<number, string> = {
  // Starter Items
  2003: "Health Potion",
  2031: "Refillable Potion",
  2033: "Corrupting Potion",
  2055: "Control Ward",

  // Boots
  3006: "Berserker's Greaves",
  3009: "Boots of Swiftness",
  3020: "Sorcerer's Shoes",
  3047: "Plated Steelcaps",
  3111: "Mercury's Treads",
  3117: "Mobility Boots",
  3158: "Ionian Boots of Lucidity",

  // Support Items
  3190: "Locket of the Iron Solari",
  3222: "Mikael's Blessing",
  3504: "Ardent Censer",
  3107: "Redemption",
  3109: "Knight's Vow",
  3050: "Zeke's Convergence",
  3871: "Zeke's Convergence",
  3869: "Celestial Opposition",
  3865: "World Atlas",
  3864: "Runic Compass",

  // AD Items
  3031: "Infinity Edge",
  3046: "Phantom Dancer",
  3072: "Bloodthirster",
  3085: "Runaan's Hurricane",
  3094: "Rapid Firecannon",
  3139: "Mercurial Scimitar",
  3153: "Blade of the Ruined King",
  3508: "Essence Reaver",
  6672: "Kraken Slayer",
  6673: "Immortal Shieldbow",
  6676: "Galeforce",

  // AP Items
  3003: "Archangel's Staff",
  3100: "Lich Bane",
  3102: "Banshee's Veil",
  3115: "Nashor's Tooth",
  3116: "Rylai's Crystal Scepter",
  3135: "Void Staff",
  3152: "Hextech Rocketbelt",
  3157: "Zhonya's Hourglass",
  4628: "Horizon Focus",
  4636: "Night Harvester",
  6653: "Liandry's Anguish",

  // Tank Items
  3068: "Sunfire Aegis",
  3075: "Thornmail",
  3110: "Frozen Heart",
  3143: "Randuin's Omen",
  3742: "Dead Man's Plate",
  3748: "Titanic Hydra",
  6664: "Turbo Chemtank",

  // MR Items
  3065: "Spirit Visage",
  3156: "Maw of Malmortius",
  3193: "Gargoyle Stoneplate",
  3194: "Adaptive Helm",

  // Lethality Items
  3142: "Youmuu's Ghostblade",
  3179: "Umbral Glaive",
  6691: "Duskblade of Draktharr",
  6692: "Eclipse",
  6693: "Prowler's Claw",

  // Trinkets
  3340: "Stealth Ward",
  3363: "Farsight Alteration",
  3364: "Oracle Lens",

  // Consumables
  2010: "Total Biscuit of Everlasting Will",
  2138: "Elixir of Iron",
  2139: "Elixir of Sorcery",
  2140: "Elixir of Wrath",

  // Anti-Heal
  3033: "Mortal Reminder",
  3123: "Executioner's Calling",
  6609: "Chempunk Chainsword",
  3076: "Bramble Vest",

  // Mythic/Legendary Season 13+
  6630: "Goredrinker",
  6631: "Stridebreaker",
  6632: "Divine Sunderer",
  6633: "Riftmaker",
  6655: "Luden's Tempest",
  6656: "Everfrost",

  // Default für unbekannte Items
};

/**
 * Get Item Name
 * @param itemId - Item ID
 * @returns Item name or ID as string if not found
 */
export function getItemName(itemId: number): string {
  return ITEM_NAMES[itemId] || `Item ${itemId}`;
}

/**
 * Get Champion Image with fallback
 * @param championName - Champion name
 * @returns Object with URL and fallback handler
 */
export function getChampionImageWithFallback(championName: string) {
  return {
    url: getChampionImageUrl(championName),
    onError: (e: any) => {
      // Fallback zu Placeholder wenn Bild nicht lädt
      e.target.src = `https://via.placeholder.com/120x120/1e293b/60a5fa?text=${championName.substring(0, 2)}`;
    }
  };
}

/**
 * Get Item Image with fallback
 * @param itemId - Item ID
 * @returns Object with URL and fallback handler
 */
export function getItemImageWithFallback(itemId: number) {
  return {
    url: getItemImageUrl(itemId),
    name: getItemName(itemId),
    onError: (e: any) => {
      // Fallback zu Placeholder
      e.target.src = `https://via.placeholder.com/64x64/334155/94a3b8?text=${itemId}`;
    }
  };
}
