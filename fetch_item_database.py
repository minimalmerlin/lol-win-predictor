"""
Item Database Fetcher from Data Dragon API
===========================================

Fetches complete item database from Riot's Data Dragon static API.

This provides:
1. All items with stats, costs, and build paths
2. Item relationships (builds_into, builds_from)
3. Item categories (Starter, Legendary, Mythic, etc.)
4. Gold costs and sell values

Data Dragon is Riot's CDN for static game data - no API key needed!

Data Dragon URL Pattern:
https://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/item.json

Output:
- data/items/items_full.json (complete item database)
- data/items/items_relational.json (processed with relationships)

Author: Victory AI System
Date: 2025-12-29
"""

import requests
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# ================= CONFIGURATION =================
DATA_DRAGON_BASE = "https://ddragon.leagueoflegends.com"
LANGUAGE = "en_US"
OUTPUT_DIR = Path("data/items")
# =================================================


def get_latest_version() -> str:
    """
    Get the latest League of Legends patch version

    Returns:
        Version string (e.g., "14.1.1")
    """
    url = f"{DATA_DRAGON_BASE}/api/versions.json"
    resp = requests.get(url)

    if resp.status_code == 200:
        versions = resp.json()
        return versions[0]  # First item is always latest

    raise Exception(f"Failed to fetch versions: {resp.status_code}")


def fetch_items(version: str) -> Dict:
    """
    Fetch complete item database for a specific patch version

    Args:
        version: Patch version (e.g., "14.1.1")

    Returns:
        Dict with all items data
    """
    url = f"{DATA_DRAGON_BASE}/cdn/{version}/data/{LANGUAGE}/item.json"

    print(f"Fetching items from: {url}")
    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.json()

    raise Exception(f"Failed to fetch items: {resp.status_code}")


def process_item_relationships(items_data: Dict) -> Dict:
    """
    Process items to extract relationships and create cleaner structure

    Args:
        items_data: Raw Data Dragon items response

    Returns:
        Dict with processed items including relationships
    """
    items = items_data['data']
    processed = {
        'version': items_data['version'],
        'type': items_data['type'],
        'items': {},
        'categories': {
            'starter': [],
            'boots': [],
            'basic': [],
            'epic': [],
            'legendary': [],
            'mythic': [],
            'consumable': [],
            'trinket': []
        }
    }

    for item_id, item_data in items.items():
        # Skip items that can't be purchased (e.g., Ornn items, Viktor items)
        if item_data.get('gold', {}).get('purchasable', True) is False:
            continue

        # Extract clean item data
        clean_item = {
            'id': int(item_id),
            'name': item_data['name'],
            'description': item_data.get('plaintext', ''),
            'gold': {
                'total': item_data['gold']['total'],
                'base': item_data['gold']['base'],
                'sell': item_data['gold']['sell'],
            },
            'stats': extract_stats(item_data),
            'tags': item_data.get('tags', []),
            'builds_from': item_data.get('from', []),
            'builds_into': item_data.get('into', []),
            'maps': item_data.get('maps', {}),
            'depth': item_data.get('depth', 1),  # Build depth (1 = starter, 2 = upgraded, etc.)
            'in_store': item_data.get('inStore', True),
            'image': item_data['image']['full']
        }

        processed['items'][item_id] = clean_item

        # Categorize
        categorize_item(clean_item, processed['categories'])

    return processed


def extract_stats(item_data: Dict) -> Dict:
    """
    Extract and clean item stats

    Args:
        item_data: Raw item data from Data Dragon

    Returns:
        Dict with cleaned stats
    """
    stats = item_data.get('stats', {})

    # Map Data Dragon stat names to readable names
    stat_mapping = {
        'FlatHPPoolMod': 'health',
        'FlatMPPoolMod': 'mana',
        'FlatArmorMod': 'armor',
        'FlatSpellBlockMod': 'magic_resist',
        'FlatPhysicalDamageMod': 'attack_damage',
        'FlatMagicDamageMod': 'ability_power',
        'PercentAttackSpeedMod': 'attack_speed',
        'PercentLifeStealMod': 'life_steal',
        'PercentMovementSpeedMod': 'movement_speed',
        'FlatCritChanceMod': 'critical_strike',
        'FlatMovementSpeedMod': 'flat_movement_speed',
        'PercentBaseHPRegenMod': 'health_regen',
        'PercentBaseMPRegenMod': 'mana_regen'
    }

    clean_stats = {}
    for dd_stat, value in stats.items():
        readable_name = stat_mapping.get(dd_stat, dd_stat)
        clean_stats[readable_name] = value

    return clean_stats


def categorize_item(item: Dict, categories: Dict):
    """
    Categorize item into appropriate category

    Args:
        item: Processed item dict
        categories: Categories dict to update
    """
    tags = item['tags']
    depth = item['depth']
    gold = item['gold']['total']
    name = item['name'].lower()

    # Boots
    if 'Boots' in tags:
        categories['boots'].append(item['id'])

    # Consumables
    elif 'Consumable' in tags or 'Potion' in name or 'Elixir' in name:
        categories['consumable'].append(item['id'])

    # Trinkets
    elif 'Trinket' in tags or 'trinket' in name.lower():
        categories['trinket'].append(item['id'])

    # Starter items (< 500 gold, depth 1)
    elif gold < 500 and depth == 1:
        categories['starter'].append(item['id'])

    # Mythic (look for Mythic in tags or name)
    elif 'Mythic' in name:
        categories['mythic'].append(item['id'])

    # Legendary (expensive, depth 2+, 2500+ gold)
    elif gold >= 2500 and depth >= 2:
        categories['legendary'].append(item['id'])

    # Epic (mid-tier, 1300-2500 gold)
    elif 1300 <= gold < 2500:
        categories['epic'].append(item['id'])

    # Basic (everything else)
    else:
        categories['basic'].append(item['id'])


def create_item_counter_matrix(items: Dict) -> Dict:
    """
    Create a simple counter matrix for items (placeholder for ML enhancement later)

    This is a simplified heuristic approach - in Month 2 we'll enhance with ML.

    Args:
        items: Processed items dict

    Returns:
        Dict mapping item IDs to counter items
    """
    counters = {}

    for item_id, item in items.items():
        stats = item['stats']
        tags = item['tags']

        counter_items = []

        # If item gives AD, counter with armor
        if stats.get('attack_damage', 0) > 0:
            # Find armor items
            for other_id, other_item in items.items():
                if other_item['stats'].get('armor', 0) >= 40:
                    counter_items.append(int(other_id))

        # If item gives AP, counter with MR
        if stats.get('ability_power', 0) > 0:
            # Find MR items
            for other_id, other_item in items.items():
                if other_item['stats'].get('magic_resist', 0) >= 40:
                    counter_items.append(int(other_id))

        # If item gives lifesteal, counter with grievous wounds
        if stats.get('life_steal', 0) > 0:
            # Find grievous wounds items (Thornmail, Morellonomicon, etc.)
            for other_id, other_item in items.items():
                if 'grievous' in other_item['description'].lower():
                    counter_items.append(int(other_id))

        if counter_items:
            counters[item_id] = list(set(counter_items))[:5]  # Top 5 counters

    return counters


def main():
    """Main execution"""
    print("=" * 80)
    print("ITEM DATABASE FETCHER - DATA DRAGON API")
    print("=" * 80)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}")

    # Get latest version
    print("\nFetching latest patch version...")
    version = get_latest_version()
    print(f"✓ Latest version: {version}")

    # Fetch items
    print(f"\nFetching items for patch {version}...")
    items_data = fetch_items(version)
    print(f"✓ Fetched {len(items_data['data'])} items")

    # Save raw data
    raw_output = OUTPUT_DIR / 'items_full.json'
    with open(raw_output, 'w', encoding='utf-8') as f:
        json.dump(items_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved raw data to: {raw_output}")

    # Process relationships
    print("\nProcessing item relationships...")
    processed = process_item_relationships(items_data)
    print(f"✓ Processed {len(processed['items'])} purchasable items")

    # Show categories
    print("\nItem categories:")
    for category, items in processed['categories'].items():
        print(f"  {category.capitalize()}: {len(items)} items")

    # Create counter matrix
    print("\nCreating item counter matrix (heuristic)...")
    counters = create_item_counter_matrix(processed['items'])
    processed['counters'] = counters
    print(f"✓ Created counters for {len(counters)} items")

    # Save processed data
    processed_output = OUTPUT_DIR / 'items_relational.json'
    with open(processed_output, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved processed data to: {processed_output}")

    # Show sample items
    print("\nSample items:")
    sample_items = list(processed['items'].items())[:5]
    for item_id, item in sample_items:
        print(f"\n  {item['name']} (ID: {item_id})")
        print(f"    Gold: {item['gold']['total']}")
        print(f"    Stats: {item['stats']}")
        print(f"    Tags: {item['tags']}")
        if item['builds_from']:
            print(f"    Builds from: {item['builds_from']}")
        if item['builds_into']:
            print(f"    Builds into: {item['builds_into']}")

    # Metadata
    metadata = {
        'fetched_at': datetime.now().isoformat(),
        'patch_version': version,
        'total_items': len(items_data['data']),
        'purchasable_items': len(processed['items']),
        'categories': {k: len(v) for k, v in processed['categories'].items()},
        'items_with_counters': len(counters)
    }

    metadata_output = OUTPUT_DIR / 'metadata.json'
    with open(metadata_output, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✓ Saved metadata to: {metadata_output}")

    print("\n" + "=" * 80)
    print("✅ ITEM DATABASE FETCH COMPLETE!")
    print("=" * 80)
    print(f"\nFiles created:")
    print(f"  1. {raw_output.name} - Raw Data Dragon response")
    print(f"  2. {processed_output.name} - Processed with relationships")
    print(f"  3. {metadata_output.name} - Fetch metadata")
    print(f"\nNext steps:")
    print(f"  - Use items_relational.json for item recommendations")
    print(f"  - Enhance counter matrix with ML in Month 2")
    print(f"  - Build item recommendation API endpoint")


if __name__ == "__main__":
    main()
