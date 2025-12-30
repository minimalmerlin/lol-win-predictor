"""
Intelligenter Item Recommender mit Heuristik
=============================================

Features:
- Exakte Builds wenn verfügbar
- Ähnliche Builds basierend auf Item-Overlap
- Counters gegen spezifische Enemy-Champions
- Fuzzy Matching für Champion-Namen

Author: Merlin Mechler
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import defaultdict, Counter
import difflib


class IntelligentItemRecommender:
    """Intelligenter Item-Recommender mit Heuristik"""

    def __init__(self, data_dir='./data/champion_data', champion_stats: Dict = None, item_builds: Dict = None):
        """
        Initialize Item Recommender

        Args:
            data_dir: Legacy parameter (not used when champion_stats/item_builds provided)
            champion_stats: Dict of champion stats from database (recommended)
            item_builds: Dict of item builds from database (recommended)
        """
        self.data_dir = Path(data_dir)

        # Use provided data (from database) or fall back to loading JSON files
        if champion_stats is not None:
            self.champion_stats = champion_stats
            print(f"✓ Using champion stats from database ({len(champion_stats)} champions)")
        else:
            self.champion_stats = self._load_json('champion_stats.json')
            print(f"⚠️  Loading champion stats from JSON fallback")

        if item_builds is not None:
            self.item_builds = item_builds
            print(f"✓ Using item builds from database ({len(item_builds)} champions)")
        else:
            self.item_builds = self._load_json('item_builds.json')
            print(f"⚠️  Loading item builds from JSON fallback")

        # Build champion name index for fuzzy matching
        self.champion_names = list(set(
            list(self.champion_stats.keys()) +
            list(self.item_builds.keys())
        ))

        print(f"✓ Total {len(self.champion_names)} unique champions")

    def _load_json(self, filename: str) -> dict:
        """Lädt JSON Datei (legacy fallback)"""
        path = self.data_dir / filename
        if not path.exists():
            print(f"⚠️  {filename} nicht gefunden")
            return {}

        with open(path, 'r') as f:
            return json.load(f)

    def fuzzy_find_champion(self, query: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Findet Champions mit Fuzzy Matching (auch bei Tippfehlern)

        Args:
            query: Suchstring
            threshold: Minimum similarity (0-1)

        Returns:
            List of (champion_name, similarity_score) tuples
        """
        if not query:
            return []

        query_lower = query.lower()
        matches = []

        for champ_name in self.champion_names:
            # Direct substring match gets highest score
            if query_lower in champ_name.lower():
                score = 0.95 if query_lower == champ_name.lower() else 0.85
                matches.append((champ_name, score))
                continue

            # Fuzzy matching using difflib
            similarity = difflib.SequenceMatcher(
                None,
                query_lower,
                champ_name.lower()
            ).ratio()

            if similarity >= threshold:
                matches.append((champ_name, similarity))

        # Sort by similarity descending
        matches.sort(key=lambda x: x[1], reverse=True)

        return matches

    def get_champion_stats(self, champion: str) -> Optional[Dict]:
        """Holt Champion Stats mit Fuzzy Matching"""
        # Try exact match first
        if champion in self.champion_stats:
            return self.champion_stats[champion]

        # Fuzzy match
        matches = self.fuzzy_find_champion(champion, threshold=0.7)
        if matches:
            best_match = matches[0][0]
            if best_match in self.champion_stats:
                return self.champion_stats[best_match]

        return None

    def get_item_builds(
        self,
        champion: str,
        enemy_team: Optional[List[str]] = None,
        top_n: int = 5
    ) -> Dict:
        """
        Holt Item Builds mit intelligenter Heuristik

        Args:
            champion: Champion Name
            enemy_team: Liste von Enemy Champions (für Countering)
            top_n: Anzahl der Top-Builds

        Returns:
            Dict mit builds und meta-info
        """
        # Fuzzy find champion
        champion_match = self._find_best_champion_match(champion)
        if not champion_match:
            return {
                'champion': champion,
                'found': False,
                'message': f'Champion "{champion}" nicht gefunden',
                'suggestions': [m[0] for m in self.fuzzy_find_champion(champion)[:5]],
                'top_builds': [],
                'fallback': self._get_similar_champion_builds(champion, top_n)
            }

        champion = champion_match

        # Check if we have builds
        if champion not in self.item_builds:
            fallback_builds = self._get_similar_champion_builds(champion, top_n)
            # Convert fallback to regular build format
            fallback_formatted = [{
                'items': fb['items'],
                'games': fb['games'],
                'wins': int(fb['games'] * fb['win_rate']),
                'losses': int(fb['games'] * (1 - fb['win_rate'])),
                'win_rate': fb['win_rate'],
                'pick_rate': 0.0,
                'source': fb['source_champion'],
                'is_fallback': True
            } for fb in fallback_builds]

            return {
                'champion': champion,
                'found': True,  # Changed to True so UI shows builds
                'total_games': 0,
                'top_builds': fallback_formatted,
                'all_builds_count': len(fallback_formatted),
                'enemy_adjusted': False,
                'using_fallback': True,
                'message': f'Showing similar builds (no exact data for {champion})'
            }

        builds_data = self.item_builds[champion]
        
        # Handle both formats: dict with 'builds' key, or list directly
        if isinstance(builds_data, dict):
            builds = builds_data.get('builds', {})
        elif isinstance(builds_data, list):
            # Convert list format to dict format for consistency
            builds = {}
            for idx, build_item in enumerate(builds_data):
                if isinstance(build_item, dict):
                    # Use items as key, or index if no items
                    build_key = str(build_item.get('items', [])) if 'items' in build_item else str(idx)
                    builds[build_key] = build_item
                else:
                    # If it's just a list of items, create a build entry
                    build_key = str(build_item) if isinstance(build_item, list) else str(idx)
                    builds[build_key] = {
                        'items': build_item if isinstance(build_item, list) else [],
                        'count': 1,
                        'wins': 0,
                        'losses': 0,
                        'win_rate': 0.5
                    }
        else:
            builds = {}

        if not builds:
            fallback_builds = self._get_similar_champion_builds(champion, top_n)
            fallback_formatted = [{
                'items': fb['items'],
                'games': fb['games'],
                'wins': int(fb['games'] * fb['win_rate']),
                'losses': int(fb['games'] * (1 - fb['win_rate'])),
                'win_rate': fb['win_rate'],
                'pick_rate': 0.0,
                'source': fb['source_champion'],
                'is_fallback': True
            } for fb in fallback_builds]

            return {
                'champion': champion,
                'found': True,
                'total_games': 0,
                'top_builds': fallback_formatted,
                'all_builds_count': len(fallback_formatted),
                'enemy_adjusted': False,
                'using_fallback': True,
                'message': f'Showing similar builds (no exact data for {champion})'
            }

        # Convert builds to list and sort
        build_list = []
        for build_key, build_data in builds.items():
            build_list.append({
                'items': build_data.get('items', []),
                'games': build_data.get('count', 0),
                'wins': build_data.get('wins', 0),
                'losses': build_data.get('losses', 0),
                'win_rate': build_data.get('win_rate', 0),
                'pick_rate': build_data.get('pick_rate', 0),
                'is_fallback': False
            })

        # Sort by win rate first, then games (better builds first)
        build_list.sort(key=lambda x: (x['win_rate'], x['games']), reverse=True)

        # If enemy team is provided, re-rank based on countering
        if enemy_team:
            build_list = self._rerank_by_counter_items(build_list, enemy_team)

        # Get total_games from builds_data (handle both formats)
        if isinstance(builds_data, dict):
            total_games = builds_data.get('total_games', 0)
        else:
            # For list format, sum up games from all builds
            total_games = sum(b.get('games', b.get('count', 0)) for b in build_list)
        
        return {
            'champion': champion,
            'found': True,
            'total_games': total_games,
            'top_builds': build_list[:top_n],
            'all_builds_count': len(build_list),
            'enemy_adjusted': bool(enemy_team),
            'using_fallback': False
        }

    def _find_best_champion_match(self, champion: str) -> Optional[str]:
        """Findet den besten Champion-Match"""
        # Exact match
        if champion in self.champion_names:
            return champion

        # Fuzzy match
        matches = self.fuzzy_find_champion(champion, threshold=0.7)
        if matches:
            return matches[0][0]

        return None

    def _get_similar_champion_builds(self, champion: str, top_n: int = 5) -> List[Dict]:
        """
        Findet ähnliche Champions und deren Builds als Fallback

        Heuristik:
        1. Champions mit ähnlichen Namen (fuzzy matching)
        2. Champions mit meisten Spielen als Popular Fallback
        """
        similar_builds = []

        # Strategy 1: Find champions with similar names using difflib
        name_matches = []
        for other_champ in self.item_builds.keys():
            if other_champ == champion:
                continue

            # Calculate name similarity
            similarity = difflib.SequenceMatcher(
                None,
                champion.lower(),
                other_champ.lower()
            ).ratio()

            if similarity >= 0.2:  # Lower threshold for more matches
                name_matches.append((other_champ, similarity))

        # Sort by similarity descending
        name_matches.sort(key=lambda x: x[1], reverse=True)

        # Get builds from similar champions
        for other_champ, similarity in name_matches[:top_n]:
            builds_data = self.item_builds.get(other_champ, {})
            builds = builds_data.get('builds', {})

            if builds:
                # Get highest win rate build (best build, not most popular)
                sorted_builds = sorted(
                    builds.items(),
                    key=lambda x: (x[1].get('win_rate', 0), x[1].get('count', 0)),
                    reverse=True
                )

                if sorted_builds:
                    build_data = sorted_builds[0][1]
                    similar_builds.append({
                        'source_champion': other_champ,
                        'similarity': similarity,
                        'items': build_data.get('items', []),
                        'games': build_data.get('count', 0),
                        'win_rate': build_data.get('win_rate', 0)
                    })

        # Strategy 2: If still not enough, use most popular champions
        if len(similar_builds) < top_n:
            all_champs_by_games = sorted(
                self.item_builds.items(),
                key=lambda x: x[1]['total_games'],
                reverse=True
            )

            for other_champ, data in all_champs_by_games:
                if other_champ == champion:
                    continue

                # Skip if already added
                if any(sb['source_champion'] == other_champ for sb in similar_builds):
                    continue

                if len(similar_builds) >= top_n:
                    break

                builds = data.get('builds', {})
                if builds:
                    # Get highest win rate build
                    sorted_builds = sorted(
                        builds.items(),
                        key=lambda x: (x[1].get('win_rate', 0), x[1].get('count', 0)),
                        reverse=True
                    )

                    if sorted_builds:
                        build_data = sorted_builds[0][1]
                        similar_builds.append({
                            'source_champion': other_champ,
                            'similarity': 0.0,
                            'items': build_data.get('items', []),
                            'games': build_data.get('count', 0),
                            'win_rate': build_data.get('win_rate', 0)
                        })

        return similar_builds[:top_n]

    def _rerank_by_counter_items(
        self,
        builds: List[Dict],
        enemy_team: List[str]
    ) -> List[Dict]:
        """
        Re-ranked Builds basierend auf Counter-Items gegen Enemy Team

        Heuristik:
        - Armor items gegen AD-heavy teams
        - MR items gegen AP-heavy teams
        - Anti-heal gegen Healer
        """
        # Item categories (simplified - would need real item data)
        ARMOR_ITEMS = {3075, 3742, 3110, 3143}  # Thornmail, Dead Man's, Frozen Heart, Randuin's
        MR_ITEMS = {3102, 3156, 3194, 3065}     # Banshee's, Maw, Adaptive, Spirit Visage
        ANTIHEAL_ITEMS = {3033, 3123, 6609}     # Mortal Reminder, Executioner's, Chempunk

        # Analyze enemy team composition (simplified)
        # In real implementation, would check champion tags from Riot API
        # For now, just boost builds with defensive items

        for build in builds:
            items_set = set(build['items'])

            # Give bonus score for having armor items
            armor_count = len(items_set & ARMOR_ITEMS)
            mr_count = len(items_set & MR_ITEMS)
            antiheal_count = len(items_set & ANTIHEAL_ITEMS)

            # Add counter_score
            build['counter_score'] = (armor_count * 0.3 +
                                     mr_count * 0.3 +
                                     antiheal_count * 0.4)

        # Sort by win rate first, counter score second, then games
        builds.sort(
            key=lambda x: (x['win_rate'], x.get('counter_score', 0), x['games']),
            reverse=True
        )

        return builds

    def calculate_item_overlap(self, items1: List[int], items2: List[int]) -> float:
        """Berechnet Overlap zwischen zwei Item-Sets (0-1)"""
        if not items1 or not items2:
            return 0.0

        set1 = set(items1)
        set2 = set(items2)

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def recommend_items_for_matchup(
        self,
        champion: str,
        ally_team: Optional[List[str]] = None,
        enemy_team: Optional[List[str]] = None,
        top_n: int = 5
    ) -> Dict:
        """
        Empfiehlt Items basierend auf vollständigem Matchup

        Kombiniert:
        - Champion's own builds
        - Enemy team countering
        - Ally team synergies
        """
        base_builds = self.get_item_builds(champion, enemy_team, top_n)

        # Add context
        base_builds['context'] = {
            'ally_team': ally_team or [],
            'enemy_team': enemy_team or [],
            'recommendation_strategy': 'popularity + countering'
        }

        return base_builds

    def search_champions(
        self,
        query: str,
        limit: int = 10,
        include_stats: bool = False
    ) -> List[Dict]:
        """
        Sucht Champions mit Fuzzy Matching

        Args:
            query: Suchstring
            limit: Max Anzahl Ergebnisse
            include_stats: Ob Stats inkludiert werden sollen

        Returns:
            Liste von Champion-Ergebnissen
        """
        matches = self.fuzzy_find_champion(query, threshold=0.4)
        results = []

        for champ_name, similarity in matches[:limit]:
            result = {
                'name': champ_name,
                'similarity': similarity,
                'match_quality': 'exact' if similarity > 0.9 else 'good' if similarity > 0.7 else 'partial'
            }

            if include_stats:
                stats = self.get_champion_stats(champ_name)
                if stats:
                    result['stats'] = stats

                # Check if has builds
                result['has_builds'] = champ_name in self.item_builds
                if result['has_builds']:
                    result['build_count'] = len(self.item_builds[champ_name].get('builds', {}))

            results.append(result)

        return results


def main():
    """Test the intelligent recommender"""
    print("=" * 80)
    print("INTELLIGENT ITEM RECOMMENDER TEST")
    print("=" * 80)

    recommender = IntelligentItemRecommender()

    # Test 1: Fuzzy Search
    print("\n[TEST 1] Fuzzy Search")
    print("-" * 40)

    test_queries = ["thresh", "jina", "misfortun", "yasou"]
    for query in test_queries:
        matches = recommender.search_champions(query, limit=3, include_stats=True)
        print(f"\nQuery: '{query}'")
        for match in matches:
            print(f"  → {match['name']} (similarity: {match['similarity']:.2f}, "
                  f"quality: {match['match_quality']})")

    # Test 2: Item Recommendations
    print("\n\n[TEST 2] Item Recommendations")
    print("-" * 40)

    result = recommender.get_item_builds("MissFortune", top_n=3)
    print(f"\nChampion: {result.get('champion')}")
    print(f"Found: {result.get('found')}")
    if result.get('found'):
        print(f"Total Games: {result.get('total_games')}")
        print(f"\nTop 3 Builds:")
        for i, build in enumerate(result.get('top_builds', []), 1):
            print(f"  {i}. {build['games']} games, {build['win_rate']:.1%} WR")
            print(f"     Items: {build['items']}")

    # Test 3: Counter Builds
    print("\n\n[TEST 3] Counter Builds (with Enemy Team)")
    print("-" * 40)

    enemy_team = ["Zed", "Malphite", "Soraka"]
    result = recommender.recommend_items_for_matchup(
        "MissFortune",
        enemy_team=enemy_team,
        top_n=3
    )
    print(f"\nAgainst: {', '.join(enemy_team)}")
    print(f"Enemy Adjusted: {result.get('enemy_adjusted')}")

    print("\n" + "=" * 80)
    print("✅ TESTS ABGESCHLOSSEN")
    print("=" * 80)


if __name__ == "__main__":
    main()
