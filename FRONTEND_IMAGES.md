# Image Management - Dynamic & Auto-Updating

## Overview

**All champion and item images are loaded dynamically from Riot's official CDN with automatic version detection.**

- ✅ **NO manual updates needed** - automatically fetches latest patch version
- ✅ **NO local image files** - everything from Riot Data Dragon API
- ✅ **NO outdated Mythic items** - always shows current items
- ✅ **Cached for performance** - 1 hour cache to reduce API calls
- ✅ **Single source of truth** - `lib/riot-data.ts` handles everything

## Single Source: `lib/riot-data.ts`

The **only** file that defines image URLs and Riot API integration:

```typescript
import {
  getLatestChampionData,
  getLatestItemData,
  getLatestVersion,
  getChampionImageUrl,
  getItemImageUrl,
  getItemNameSync
} from '@/lib/riot-data';

// Async: Fetch latest patch version (e.g., "14.24.1")
const version = await getLatestVersion();

// Async: Fetch ALL champions with correct IDs
const { champions } = await getLatestChampionData();
// Returns: [{ id: "MonkeyKing", name: "Wukong", ... }, ...]

// Async: Fetch ALL items (no outdated Mythics!)
const { items } = await getLatestItemData();

// Sync: Get champion image URL (uses cached version)
const champUrl = getChampionImageUrl("Thresh");

// Sync: Get item image URL (uses cached version)
const itemUrl = getItemImageUrl(3157);

// Sync: Get item name (uses cached data)
const itemName = getItemNameSync(3157);
```

**Benefits:**
- Auto-updates every hour
- Solves "Wukong vs MonkeyKing" problem automatically
- New champions work immediately
- Never recommends removed items
- Single file to maintain

## Usage Examples

### Simple Synchronous Usage

For most components, use the synchronous helpers:

```tsx
import { getChampionImageUrl, getItemImageUrl, getItemNameSync } from '@/lib/riot-data';

// Champion image
<Image
  src={getChampionImageUrl("Thresh")}
  alt="Thresh"
  width={64}
  height={64}
  unoptimized
/>

// Item image with name
<Image
  src={getItemImageUrl(3157)}
  alt={getItemNameSync(3157)}
  width={48}
  height={48}
  unoptimized
/>
```

### Advanced: Async Data Fetching

For components that need the full dataset:

```tsx
'use client';
import { useEffect, useState } from 'react';
import { getLatestChampionData, getChampionImageUrl } from '@/lib/riot-data';

export default function ChampionList() {
  const [champions, setChampions] = useState([]);

  useEffect(() => {
    async function load() {
      const { champions } = await getLatestChampionData();
      setChampions(champions);
    }
    load();
  }, []);

  return (
    <div>
      {champions.map(champ => (
        <img
          key={champ.id}
          src={getChampionImageUrl(champ.name)}
          alt={champ.name}
        />
      ))}
    </div>
  );
}
```

## Key Functions

### Async Functions (Data Fetching)

| Function | Description | Returns |
|----------|-------------|---------|
| `getLatestVersion()` | Get current patch version | `Promise<string>` |
| `getLatestChampionData()` | Get all champions + version | `Promise<{ version, champions }>` |
| `getLatestItemData()` | Get all items + version | `Promise<{ version, items }>` |
| `getChampionIdByName(name)` | Find champion ID by name | `Promise<string \| null>` |
| `getItemName(itemId)` | Get item name (always current) | `Promise<string>` |

### Sync Functions (URL Helpers)

| Function | Description | Returns |
|----------|-------------|---------|
| `getChampionImageUrl(name)` | Champion portrait URL | `string` |
| `getChampionSplashUrl(name)` | Splash art URL | `string` |
| `getItemImageUrl(itemId)` | Item icon URL | `string` |
| `getItemNameSync(itemId)` | Item name (from cache) | `string` |
| `clearCache()` | Force refresh all cached data | `void` |

## Caching Strategy

- **Duration**: 1 hour per fetch
- **Scope**: Module-level (shared across all components)
- **Refresh**: Automatic after cache expires
- **Manual**: Call `clearCache()` to force refresh

```typescript
import { clearCache } from '@/lib/riot-data';

// Force refresh (e.g., on new patch day)
clearCache();
```

## Why This Is Better

### ❌ Old Static Approach

```typescript
const DDRAGON_VERSION = '14.24.1'; // Manual update required!
const ITEM_NAMES = {
  6630: "Goredrinker", // REMOVED ITEM - Bug!
  6631: "Stridebreaker", // REMOVED ITEM - Bug!
}
```

**Problems:**
1. Breaks on new patch day
2. Recommends removed items
3. New champions don't work
4. Manual maintenance nightmare

### ✅ New Dynamic Approach

```typescript
const { version } = await getLatestVersion(); // Auto-detects "14.24.1"
const { items } = await getLatestItemData(); // Only current items
```

**Benefits:**
1. Works on new patch day automatically
2. Never shows removed items
3. New champions work immediately
4. Zero maintenance

## Champion Name Mapping

The wrapper handles name variations automatically:

```
"Master Yi" → "MasterYi"
"Dr. Mundo" → "DrMundo"
"Kha'Zix" → "Khazix"
"Wukong" → "MonkeyKing"
```

For new champions, the dynamic API fetches the correct ID directly from Riot.

## Configuration

Next.js is configured to allow images from Riot's CDN:

```typescript
// next.config.ts
images: {
  remotePatterns: [
    {
      protocol: 'https',
      hostname: 'ddragon.leagueoflegends.com',
      pathname: '/cdn/**',
    }
  ]
}
```

## Important Notes

- **Single source of truth**: Only `lib/riot-data.ts` exists - `riot-assets.ts` has been removed
- **Auto-updates**: Version is fetched automatically on module load and cached for 1 hour
- **Name variations**: Champion name mapping (e.g., "Wukong" → "MonkeyKing") is handled automatically
- **Fallback**: If cache is empty, uses fallback version "14.24.1"

## Components Using Images

- `app/champion/[name]/page.tsx` - Champion details
- `components/ChampionStatsExplorer.tsx` - Stats table
- `app/draft/page.tsx` - Draft predictor
- `app/live/page.tsx` - Live game tracker

## Error Handling

All images have automatic fallback:

```typescript
<Image
  src={getChampionImageUrl("Thresh")}
  onError={(e) => {
    e.target.src = 'https://via.placeholder.com/64x64?text=TH';
  }}
/>
```

## Summary

- ✅ **Single source of truth**: `riot-data.ts`
- ✅ **Auto-updating**: Checks Riot API every hour
- ✅ **Always current**: New patches work automatically
- ✅ **No maintenance**: Zero manual updates needed
- ✅ **Backward compatible**: Old code still works
