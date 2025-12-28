# Image Management - Single Source of Truth

## Overview

**All champion and item images are loaded dynamically from Riot's official CDN.**

There are **NO local image files** for champions or items. Everything comes from:
- Riot Data Dragon API: `https://ddragon.leagueoflegends.com/cdn/`

## Single Source: `lib/riot-assets.ts`

This is the **only file** that defines image URLs. All components import from here.

### Usage

```tsx
import { getChampionImageUrl, getItemImageUrl, getItemName } from '@/lib/riot-assets';

// Champion image
<Image
  src={getChampionImageUrl("Thresh")}
  alt="Thresh"
  width={64}
  height={64}
  unoptimized
  onError={(e) => {
    const target = e.target as HTMLImageElement;
    target.src = `https://via.placeholder.com/64x64?text=Thresh`;
  }}
/>

// Item image
<Image
  src={getItemImageUrl(3157)}
  alt={getItemName(3157)}
  width={48}
  height={48}
  unoptimized
/>
```

## Functions Available

### Champion Images

- `getChampionImageUrl(name: string)`: Champion portrait (120x120)
- `getChampionSplashUrl(name: string)`: Splash art (large background)
- `getChampionImageWithFallback(name: string)`: Returns object with URL + error handler

### Item Images

- `getItemImageUrl(itemId: number)`: Item icon (64x64)
- `getItemName(itemId: number)`: Human-readable item name
- `ITEM_NAMES`: Full mapping of item IDs to names
- `getItemImageWithFallback(itemId: number)`: Returns object with URL + error handler + name

## Champion Name Mapping

Some champions have special naming in Riot's API. The `riot-assets.ts` handles this automatically:

```typescript
'Master Yi' -> 'MasterYi'
'Dr. Mundo' -> 'DrMundo'
"Kha'Zix" -> 'Khazix'
"Kog'Maw" -> 'KogMaw'
'Twisted Fate' -> 'TwistedFate'
// etc.
```

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
    },
    {
      protocol: 'https',
      hostname: 'via.placeholder.com', // Fallback
    },
  ],
}
```

## NO Local Images!

❌ **Do NOT add champion/item images to `/public`**

✅ **Always use `riot-assets.ts` functions**

### Why?

1. **Single source of truth**: One place to update API version
2. **Always up-to-date**: New champions/items work automatically
3. **No maintenance**: No need to download/update images
4. **Smaller bundle**: No large image files in the repository
5. **Official assets**: Always matches current game patch

## Current Patch Version

The CDN version is set in `riot-assets.ts`:

```typescript
const DDRAGON_VERSION = '14.24.1'; // LoL Patch 14.24
```

Update this when a new patch is released to get the latest champion/item images.

## Error Handling

All images have fallback placeholders in case the Riot CDN fails:

- Champion images → Placeholder with first 2 letters of name
- Item images → Placeholder with item ID

This is handled automatically by the `onError` handlers in components.

## Components Using Images

Currently used in:
- `app/champion/[name]/page.tsx` - Champion detail page
- `components/ChampionStatsExplorer.tsx` - Champion stats table
- `app/draft/page.tsx` - Draft predictor
- `app/live/page.tsx` - Live game tracker
- `components/ChampionCard.tsx` - Champion selection cards

All import from `@/lib/riot-assets` - **do not use any other source!**
