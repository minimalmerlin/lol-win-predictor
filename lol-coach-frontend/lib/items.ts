// League of Legends Item Data
// Using Data Dragon CDN for item images and names

export interface ItemData {
  id: number;
  name: string;
  image: string;
}

// Item names mapping (commonly used items)
export const ITEM_NAMES: Record<number, string> = {
  // Starter Items
  1036: "Long Sword",
  1037: "Pickaxe",
  1038: "B.F. Sword",
  1042: "Dagger",
  1043: "Recurve Bow",
  1052: "Amplifying Tome",
  1053: "Vampiric Scepter",
  1054: "Doran's Shield",
  1055: "Doran's Blade",
  1056: "Doran's Ring",
  1058: "Needlessly Large Rod",

  // Boots
  1001: "Boots",
  3006: "Berserker's Greaves",
  3009: "Boots of Swiftness",
  3020: "Sorcerer's Shoes",
  3047: "Plated Steelcaps",
  3111: "Mercury's Treads",
  3117: "Mobility Boots",
  3158: "Ionian Boots of Lucidity",

  // Legendary Items - AD
  3031: "Infinity Edge",
  3033: "Mortal Reminder",
  3036: "Lord Dominik's Regards",
  3046: "Phantom Dancer",
  3072: "Bloodthirster",
  3078: "Trinity Force",
  3085: "Runaan's Hurricane",
  3087: "Statikk Shiv",
  3094: "Rapid Firecannon",
  3095: "Stormrazor",
  3100: "Lich Bane",
  3153: "Blade of the Ruined King",
  3508: "Essence Reaver",
  6671: "Galeforce",
  6672: "Kraken Slayer",
  6673: "Immortal Shieldbow",

  // Legendary Items - AP
  3003: "Archangel's Staff",
  3089: "Rabadon's Deathcap",
  3102: "Banshee's Veil",
  3115: "Nashor's Tooth",
  3116: "Rylai's Crystal Scepter",
  3135: "Void Staff",
  3152: "Hextech Rocketbelt",
  3165: "Morellonomicon",
  4005: "Imperial Mandate",
  4628: "Horizon Focus",
  4633: "Riftmaker",
  6653: "Liandry's Torment",

  // Tank Items
  3001: "Evenshroud",
  3065: "Spirit Visage",
  3068: "Sunfire Aegis",
  3075: "Thornmail",
  3110: "Frozen Heart",
  3143: "Randuin's Omen",
  3190: "Locket of the Iron Solari",
  3193: "Gargoyle Stoneplate",
  6664: "Turbo Chemtank",

  // Support Items
  3107: "Redemption",
  3109: "Knight's Vow",
  3222: "Mikael's Blessing",
  3504: "Ardent Censer",
  3851: "Frostfang",
  3853: "Shard of True Ice",

  // Utility
  3074: "Ravenous Hydra",
  3077: "Tiamat",
  3142: "Youmuu's Ghostblade",
  3156: "Maw of Malmortius",
  3157: "Zhonya's Hourglass",
  3161: "Spear of Shojin",
  3748: "Titanic Hydra",
  6609: "Chempunk Chainsword",
  6630: "Goredrinker",
  6631: "Stridebreaker",
  6632: "Divine Sunderer",
  6655: "Luden's Companion",
  6656: "Everfrost",
  6662: "Iceborn Gauntlet",

  // Consumables & Trinkets
  2003: "Health Potion",
  2031: "Refillable Potion",
  2033: "Corrupting Potion",
  2055: "Control Ward",
  3340: "Stealth Ward",
  3363: "Farsight Alteration",
  3364: "Oracle Lens",

  // Mythic/Legendary Season 13+
  3170: "Mosstomper Seedling",
  3330: "Scarecrow Effigy",

  // Ornn Items
  7000: "Sandshrike's Claw",
  7001: "Syzygy",
  7002: "Draktharr's Shadowcarver",
};

// Get Data Dragon version (use latest)
const DDRAGON_VERSION = "14.24.1"; // Update this periodically
const DDRAGON_CDN = `https://ddragon.leagueoflegends.com/cdn/${DDRAGON_VERSION}`;

export function getItemName(itemId: number): string {
  return ITEM_NAMES[itemId] || `Item #${itemId}`;
}

export function getItemImage(itemId: number): string {
  return `${DDRAGON_CDN}/img/item/${itemId}.png`;
}

export function getItemData(itemId: number): ItemData {
  return {
    id: itemId,
    name: getItemName(itemId),
    image: getItemImage(itemId),
  };
}

// Get champion square icon
export function getChampionImage(championName: string): string {
  return `${DDRAGON_CDN}/img/champion/${championName}.png`;
}

// Fallback image for unknown items
export const UNKNOWN_ITEM_IMAGE = `${DDRAGON_CDN}/img/item/0.png`;
