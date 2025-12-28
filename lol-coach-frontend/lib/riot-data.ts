export interface ChampionDto {
  id: string; key: string; name: string; title: string; tags: string[]; image: { full: string };
}
export interface ChampionDetailDto extends ChampionDto {
  lore: string;
  spells: Array<{ id: string; name: string; description: string; image: { full: string }; }>;
  passive: { name: string; description: string; image: { full: string }; };
  allytips: string[]; enemytips: string[];
}

let cachedVersion: string | null = null;
let cachedChampions: ChampionDto[] | null = null;

export async function getLatestVersion(): Promise<string> {
  if (cachedVersion) return cachedVersion;
  try {
    const res = await fetch('https://ddragon.leagueoflegends.com/api/versions.json');
    const versions = await res.json();
    cachedVersion = versions[0];
    return cachedVersion || "14.1.1";
  } catch { return "14.1.1"; }
}

export async function getLatestChampionData() {
  const version = await getLatestVersion();
  if (cachedChampions) return { version, champions: cachedChampions };
  try {
    const res = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/champion.json`);
    const json = await res.json();
    cachedChampions = Object.values(json.data) as ChampionDto[];
    return { version, champions: cachedChampions };
  } catch (e) { return { version, champions: [] }; }
}

export async function getChampionDetailByName(nameOrId: string): Promise<ChampionDetailDto | null> {
  const { champions } = await getLatestChampionData();
  const target = champions.find(c => c.id.toLowerCase() === nameOrId.toLowerCase() || c.name.toLowerCase() === nameOrId.toLowerCase());
  if (!target) return null;
  const version = await getLatestVersion();
  try {
    const res = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/champion/${target.id}.json`);
    const json = await res.json();
    return json.data[target.id] as ChampionDetailDto;
  } catch { return null; }
}

export function getChampionImageUrl(id: string, version: string = "14.24.1"): string {
  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/champion/${id}.png`;
}
export function getSpellImageUrl(imgName: string, version: string = "14.24.1"): string {
  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/spell/${imgName}`;
}
export function getPassiveImageUrl(imgName: string, version: string = "14.24.1"): string {
  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/passive/${imgName}`;
}

// --- ITEM HELPERS (Added to fix Build Errors in Draft Page) ---

/**
 * Generiert die URL für ein Item-Icon basierend auf der ID.
 * Default Version fallback, falls keine Version übergeben wird.
 */
export function getItemImageUrl(id: string | number, version: string = "14.24.1"): string {
  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/item/${id}.png`;
}

/**
 * Legacy Support: Früher hatten wir eine lokale Item-Datenbank für Namen.
 * Da wir jetzt API-first sind, geben wir als Fallback die ID zurück,
 * bis wir einen asynchronen Item-Fetcher gebaut haben.
 * Dies verhindert, dass app/draft/page.tsx abstürzt.
 */
export function getItemNameSync(id: string | number): string {
  // TODO: Später durch echten Async-Call ersetzen oder Item-Liste cachen
  return `Item ${id}`;
}
