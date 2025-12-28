# Image Management - Dynamic & Auto-Updating

## Overview

**All champion and item images are loaded dynamically from Riot's official CDN with automatic version detection.**

- ✅ **NO manual updates needed** - automatically fetches latest patch version
- ✅ **NO local image files** - everything from Riot Data Dragon API
- ✅ **NO outdated Mythic items** - always shows current items
- ✅ **Cached for performance** - 1 hour cache to reduce API calls

## Two-Layer Architecture

### 1. Core Dynamic API: `lib/riot-data.ts`

The intelligent layer that **automatically** fetches data from Riot:

```typescript
import { getLatestChampionData, getLatestItemData, getLatestVersion } from '@/lib/riot-data';

// Fetch latest patch version (e.g., "14.24.1")
const version = await getLatestVersion();

// Fetch ALL champions with correct IDs
const { champions } = await getLatestChampionData();
// Returns: [{ id: "MonkeyKing", name: "Wukong", ... }, ...]

// Fetch ALL items (no outdated Mythics!)
const { items } = await getLatestItemData();
```

**Benefits:**
- Auto-updates every hour
- Solves "Wukong vs MonkeyKing" problem automatically
- New champions work immediately
- Never recommends removed items

### 2. Compatibility Wrapper: `lib/riot-assets.ts`

Backward-compatible wrapper for existing components:

```typescript
import { getChampionImageUrl, getItemImageUrl } from '@/lib/riot-assets';

// Simple synchronous calls (uses cached version)
const url = getChampionImageUrl("Thresh");
const itemUrl = getItemImageUrl(3157);
```

## Usage Examples

### For New Code (Recommended)

Use the dynamic API directly:

```tsx
'use client';
import { useEffect, useState } from 'react';
import { getLatestChampionData, getChampionImageUrl } from '@/lib/riot-data';

export default function ChampionList() {
  const [version, setVersion] = useState('');
  const [champions, setChampions] = useState([]);

  useEffect(() => {
    async function load() {
      const data = await getLatestChampionData();
      setVersion(data.version);
      setChampions(data.champions);
    }
    load();
  }, []);

  return (
    <div>
      <p>Patch {version}</p>
      {champions.map(champ => (
        <img
          key={champ.id}
          src={getChampionImageUrl(champ.id, version)}
          alt={champ.name}
        />
      ))}
    </div>
  );
}
```

### For Existing Code (Backward Compatible)

Keep using the simple API:

```tsx
import { getChampionImageUrl, getItemImageUrl } from '@/lib/riot-assets';

<Image
  src={getChampionImageUrl("Thresh")}
  alt="Thresh"
  width={64}
  height={64}
  unoptimized
/>
```

## Key Functions

### Dynamic API (`riot-data.ts`)

| Function | Description | Returns |
|----------|-------------|---------|
| `getLatestVersion()` | Get current patch version | `Promise<string>` |
| `getLatestChampionData()` | Get all champions + version | `Promise<{ version, champions }>` |
| `getLatestItemData()` | Get all items + version | `Promise<{ version, items }>` |
| `getChampionIdByName(name)` | Find champion ID by name | `Promise<string \| null>` |
| `getItemName(itemId)` | Get item name (always current) | `Promise<string>` |
| `clearCache()` | Force refresh data | `void` |

### Wrapper API (`riot-assets.ts`)

| Function | Description | Returns |
|----------|-------------|---------|
| `getChampionImageUrl(name)` | Champion portrait URL | `string` |
| `getChampionSplashUrl(name)` | Splash art URL | `string` |
| `getItemImageUrl(itemId)` | Item icon URL | `string` |
| `getItemName(itemId)` | Item name (async) | `Promise<string>` |

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

## Migration Path

Existing code using `riot-assets.ts` will continue to work.

**To migrate to dynamic API:**

1. Replace imports:
```typescript
// Before
import { getChampionImageUrl } from '@/lib/riot-assets';

// After
import { getLatestChampionData, getChampionImageUrl } from '@/lib/riot-data';
```

2. Fetch data on component mount:
```typescript
const { version, champions } = await getLatestChampionData();
```

3. Use version in URL generation:
```typescript
getChampionImageUrl(champion.id, version)
```

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
