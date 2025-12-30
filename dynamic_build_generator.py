"""
Dynamic Build Generator - AI-Powered Item Path Generation
==========================================================

Generiert individualisierte Item-Build-Pfade basierend auf:
- Champion & Role des Users
- Team & Enemy Composition
- Champion Roles (z.B. Lux Support vs Mid)
- Game State (Leading, Losing, Even)
- Item Stats & Synergies

Author: Merlin Mechler
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class GameState(Enum):
    """Current game state"""
    LEADING = "leading"      # Winning, ahead in gold
    EVEN = "even"           # Close game
    LOSING = "losing"       # Behind in gold


class ItemCategory(Enum):
    """Item categories by purpose"""
    DAMAGE = "damage"
    TANK = "tank"
    SUPPORT = "support"
    SUSTAIN = "sustain"
    MOBILITY = "mobility"
    UTILITY = "utility"
    ANTI_HEAL = "anti_heal"
    ARMOR = "armor"
    MAGIC_RESIST = "magic_resist"


@dataclass
class Champion:
    """Champion with role information"""
    name: str
    role: str  # Top, Jungle, Mid, ADC, Support


@dataclass
class ItemBuildPath:
    """Complete item build path with situational branches"""
    core_items: List[Dict]          # Core items (always buy)
    situational_items: Dict[str, List[Dict]]  # Conditional items
    early_game: List[Dict]          # First 10 minutes
    mid_game: List[Dict]            # 10-25 minutes
    late_game: List[Dict]           # 25+ minutes
    explanation: str                # Why this build


class DynamicBuildGenerator:
    """Generates dynamic, AI-powered item builds"""

    def __init__(self, data_dir='./data/champion_data', champion_stats: Dict = None, item_builds: Dict = None):
        """
        Initialize Dynamic Build Generator

        Args:
            data_dir: Legacy parameter (not used when champion_stats/item_builds provided)
            champion_stats: Dict of champion stats from database (recommended)
            item_builds: Dict of item builds from database (recommended)
        """
        self.data_dir = Path(data_dir)

        # Load item database
        self.items = self._load_item_database()

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

        print(f"✓ Loaded {len(self.items)} items")

    def _load_json(self, filename: str) -> dict:
        """Load JSON file (legacy fallback)"""
        path = self.data_dir / filename
        if not path.exists():
            return {}
        with open(path, 'r') as f:
            return json.load(f)

    def _load_item_database(self) -> Dict[int, Dict]:
        """
        Load comprehensive item database with stats and categories

        In production, this would load from Riot API or a complete database.
        For now, we define key items with their stats and purposes.
        """
        return {
            # ===== BOOTS =====
            3006: {
                "name": "Berserker's Greaves",
                "cost": 1100,
                "stats": {"attack_speed": 35},
                "categories": [ItemCategory.DAMAGE, ItemCategory.MOBILITY],
                "good_against": [],
                "synergizes_with": ["ADC", "Auto-Attack Champions"]
            },
            3020: {
                "name": "Sorcerer's Shoes",
                "cost": 1100,
                "stats": {"magic_pen": 18},
                "categories": [ItemCategory.DAMAGE, ItemCategory.MOBILITY],
                "good_against": ["Low MR Teams"],
                "synergizes_with": ["Mage", "AP Champions"]
            },
            3047: {
                "name": "Plated Steelcaps",
                "cost": 1100,
                "stats": {"armor": 25},
                "categories": [ItemCategory.TANK, ItemCategory.MOBILITY],
                "good_against": ["AD Heavy", "Auto-Attackers"],
                "synergizes_with": ["Tank", "Bruiser"]
            },
            3111: {
                "name": "Mercury's Treads",
                "cost": 1100,
                "stats": {"mr": 25, "tenacity": 30},
                "categories": [ItemCategory.MAGIC_RESIST, ItemCategory.MOBILITY],
                "good_against": ["AP Heavy", "CC Heavy"],
                "synergizes_with": ["All Roles"]
            },

            # ===== ADC ITEMS =====
            3031: {
                "name": "Infinity Edge",
                "cost": 3400,
                "stats": {"ad": 70, "crit": 20},
                "categories": [ItemCategory.DAMAGE],
                "good_against": [],
                "synergizes_with": ["ADC", "Crit Builds"],
                "power_spike": "late"
            },
            6672: {
                "name": "Kraken Slayer",
                "cost": 3100,
                "stats": {"ad": 40, "attack_speed": 25, "crit": 20},
                "categories": [ItemCategory.DAMAGE],
                "good_against": ["Tanks", "High HP"],
                "synergizes_with": ["ADC", "On-Hit"],
                "power_spike": "mid"
            },
            3153: {
                "name": "Blade of the Ruined King",
                "cost": 3200,
                "stats": {"ad": 40, "attack_speed": 25, "lifesteal": 10},
                "categories": [ItemCategory.DAMAGE, ItemCategory.SUSTAIN],
                "good_against": ["Tanks", "High HP"],
                "synergizes_with": ["ADC", "Bruiser"],
                "power_spike": "early"
            },

            # ===== MAGE ITEMS =====
            6653: {
                "name": "Liandry's Anguish",
                "cost": 3200,
                "stats": {"ap": 80, "hp": 300, "ability_haste": 20},
                "categories": [ItemCategory.DAMAGE],
                "good_against": ["Tanks", "High HP"],
                "synergizes_with": ["Mage", "DPS Mage"],
                "power_spike": "mid"
            },
            3157: {
                "name": "Zhonya's Hourglass",
                "cost": 3250,
                "stats": {"ap": 80, "armor": 45, "ability_haste": 15},
                "categories": [ItemCategory.DAMAGE, ItemCategory.ARMOR, ItemCategory.UTILITY],
                "good_against": ["AD Assassins", "Dive Comps"],
                "synergizes_with": ["Mage"],
                "power_spike": "mid"
            },
            3135: {
                "name": "Void Staff",
                "cost": 2800,
                "stats": {"ap": 100, "magic_pen_percent": 40},
                "categories": [ItemCategory.DAMAGE],
                "good_against": ["High MR Teams"],
                "synergizes_with": ["Mage"],
                "power_spike": "late"
            },

            # ===== TANK ITEMS =====
            3068: {
                "name": "Sunfire Aegis",
                "cost": 3200,
                "stats": {"hp": 450, "armor": 50},
                "categories": [ItemCategory.TANK, ItemCategory.DAMAGE],
                "good_against": ["AD Heavy"],
                "synergizes_with": ["Tank", "Bruiser"],
                "power_spike": "early"
            },
            3075: {
                "name": "Thornmail",
                "cost": 2700,
                "stats": {"hp": 350, "armor": 60},
                "categories": [ItemCategory.TANK, ItemCategory.ANTI_HEAL, ItemCategory.ARMOR],
                "good_against": ["Auto-Attackers", "Healers"],
                "synergizes_with": ["Tank"],
                "power_spike": "mid"
            },
            3065: {
                "name": "Spirit Visage",
                "cost": 2900,
                "stats": {"hp": 450, "mr": 60, "ability_haste": 10},
                "categories": [ItemCategory.TANK, ItemCategory.MAGIC_RESIST, ItemCategory.SUSTAIN],
                "good_against": ["AP Heavy"],
                "synergizes_with": ["Tank", "Healers"],
                "power_spike": "mid"
            },
            3110: {
                "name": "Frozen Heart",
                "cost": 2500,
                "stats": {"armor": 80, "mana": 400, "ability_haste": 20},
                "categories": [ItemCategory.TANK, ItemCategory.ARMOR],
                "good_against": ["Attack Speed Teams", "AD Heavy"],
                "synergizes_with": ["Tank", "Mana Users"],
                "power_spike": "mid"
            },

            # ===== SUPPORT ITEMS =====
            3190: {
                "name": "Locket of the Iron Solari",
                "cost": 2200,
                "stats": {"hp": 200, "armor": 30, "mr": 30, "ability_haste": 15},
                "categories": [ItemCategory.SUPPORT, ItemCategory.TANK],
                "good_against": ["Burst Damage"],
                "synergizes_with": ["Support"],
                "power_spike": "mid"
            },
            3504: {
                "name": "Ardent Censer",
                "cost": 2300,
                "stats": {"ap": 60, "ability_haste": 15},
                "categories": [ItemCategory.SUPPORT, ItemCategory.DAMAGE],
                "good_against": [],
                "synergizes_with": ["Enchanter Support", "ADC Teams"],
                "power_spike": "mid"
            },

            # ===== ANTI-HEAL =====
            3033: {
                "name": "Mortal Reminder",
                "cost": 2600,
                "stats": {"ad": 30, "crit": 20, "attack_speed": 25},
                "categories": [ItemCategory.DAMAGE, ItemCategory.ANTI_HEAL],
                "good_against": ["Healers", "Lifesteal"],
                "synergizes_with": ["ADC"],
                "power_spike": "mid"
            },
            6609: {
                "name": "Chempunk Chainsword",
                "cost": 2600,
                "stats": {"ad": 55, "hp": 250, "ability_haste": 15},
                "categories": [ItemCategory.DAMAGE, ItemCategory.ANTI_HEAL],
                "good_against": ["Healers", "Lifesteal"],
                "synergizes_with": ["Bruiser", "Fighter"],
                "power_spike": "mid"
            },

            # ===== MR ITEMS =====
            3102: {
                "name": "Banshee's Veil",
                "cost": 2600,
                "stats": {"ap": 120, "mr": 50, "ability_haste": 15},
                "categories": [ItemCategory.DAMAGE, ItemCategory.MAGIC_RESIST],
                "good_against": ["AP Burst", "Poke"],
                "synergizes_with": ["Mage"],
                "power_spike": "mid"
            },
            3156: {
                "name": "Maw of Malmortius",
                "cost": 2800,
                "stats": {"ad": 50, "mr": 50, "ability_haste": 15},
                "categories": [ItemCategory.DAMAGE, ItemCategory.MAGIC_RESIST],
                "good_against": ["AP Burst"],
                "synergizes_with": ["AD Champions"],
                "power_spike": "mid"
            },
        }

    def generate_build_path(
        self,
        user_champion: Champion,
        ally_team: List[Champion],
        enemy_team: List[Champion],
        game_state: GameState = GameState.EVEN
    ) -> ItemBuildPath:
        """
        Generate complete item build path with situational branches

        Args:
            user_champion: User's champion with role
            ally_team: Allied champions with roles
            enemy_team: Enemy champions with roles
            game_state: Current game state (leading/even/losing)

        Returns:
            Complete ItemBuildPath with core, situational, and timed items
        """

        # Analyze team compositions
        enemy_analysis = self._analyze_enemy_team(enemy_team)
        ally_analysis = self._analyze_ally_team(ally_team)

        # Determine build strategy
        strategy = self._determine_build_strategy(
            user_champion,
            enemy_analysis,
            ally_analysis,
            game_state
        )

        # Generate core items (always buy these)
        core_items = self._generate_core_items(user_champion, strategy)

        # Generate situational branches
        situational = self._generate_situational_items(
            user_champion,
            enemy_analysis,
            game_state
        )

        # Generate timing-based items
        early_game = self._generate_early_game_items(user_champion, enemy_analysis)
        mid_game = self._generate_mid_game_items(user_champion, enemy_analysis, game_state)
        late_game = self._generate_late_game_items(user_champion, strategy)

        # Generate explanation
        explanation = self._generate_explanation(
            user_champion,
            enemy_analysis,
            strategy,
            game_state
        )

        return ItemBuildPath(
            core_items=core_items,
            situational_items=situational,
            early_game=early_game,
            mid_game=mid_game,
            late_game=late_game,
            explanation=explanation
        )

    def _analyze_enemy_team(self, enemy_team: List[Champion]) -> Dict:
        """Analyze enemy team composition"""
        analysis = {
            'ad_count': 0,
            'ap_count': 0,
            'tank_count': 0,
            'assassin_count': 0,
            'support_count': 0,
            'has_healer': False,
            'has_burst': False,
            'has_dps': False,
            'roles': {},
            'threats': []
        }

        for champ in enemy_team:
            analysis['roles'][champ.name] = champ.role

            # Role-based categorization
            if champ.role == 'Support':
                analysis['support_count'] += 1
                # Simplified: Assume some supports are healers
                if champ.name in ['Soraka', 'Yuumi', 'Sona', 'Nami']:
                    analysis['has_healer'] = True

            # Simplified AD/AP detection (would use actual champion data)
            # For now, use heuristics based on typical roles
            if champ.role in ['ADC', 'Top']:
                analysis['ad_count'] += 1
            if champ.role in ['Mid', 'Support'] and champ.name not in ['Zed', 'Talon']:
                analysis['ap_count'] += 1

            # Detect threats
            if champ.name in ['Zed', 'Talon', 'Katarina', 'Fizz']:
                analysis['assassin_count'] += 1
                analysis['threats'].append(f"{champ.name} ({champ.role})")

        analysis['is_ad_heavy'] = analysis['ad_count'] >= 3
        analysis['is_ap_heavy'] = analysis['ap_count'] >= 3
        analysis['is_balanced'] = not (analysis['is_ad_heavy'] or analysis['is_ap_heavy'])

        return analysis

    def _analyze_ally_team(self, ally_team: List[Champion]) -> Dict:
        """Analyze ally team composition"""
        return {
            'has_tank': any(c.role == 'Top' for c in ally_team),
            'has_enchanter': any(c.role == 'Support' for c in ally_team),
            'adc_count': sum(1 for c in ally_team if c.role == 'ADC')
        }

    def _determine_build_strategy(
        self,
        user_champion: Champion,
        enemy_analysis: Dict,
        ally_analysis: Dict,
        game_state: GameState
    ) -> str:
        """Determine overall build strategy"""

        # Role-based base strategy
        if user_champion.role == 'ADC':
            base_strategy = 'damage_crit'
        elif user_champion.role == 'Support':
            base_strategy = 'support_utility'
        elif user_champion.role == 'Top':
            base_strategy = 'bruiser_tank'
        elif user_champion.role == 'Mid':
            base_strategy = 'mage_burst'
        elif user_champion.role == 'Jungle':
            base_strategy = 'jungle_flex'
        else:
            base_strategy = 'balanced'

        # Modify based on game state
        if game_state == GameState.LEADING:
            # When ahead, go aggressive
            if 'tank' in base_strategy:
                return 'aggressive_tank'
            return 'snowball_damage'
        elif game_state == GameState.LOSING:
            # When behind, go defensive/scaling
            return 'defensive_scaling'

        return base_strategy

    def _generate_core_items(self, champion: Champion, strategy: str) -> List[Dict]:
        """Generate core items that should always be built"""
        core = []

        # Add boots first (always core)
        if champion.role == 'ADC':
            core.append(self._item_to_dict(3006))  # Berserker's Greaves
        elif champion.role == 'Support':
            core.append(self._item_to_dict(3111))  # Mercury's Treads
        elif champion.role in ['Mid', 'Mage']:
            core.append(self._item_to_dict(3020))  # Sorcerer's Shoes
        else:
            core.append(self._item_to_dict(3047))  # Plated Steelcaps

        # Role-specific core items
        if champion.role == 'ADC':
            core.extend([
                self._item_to_dict(6672),  # Kraken Slayer
                self._item_to_dict(3031),  # Infinity Edge
            ])
        elif champion.role == 'Support':
            core.append(self._item_to_dict(3190))  # Locket
        elif champion.role in ['Mid', 'Mage']:
            core.extend([
                self._item_to_dict(6653),  # Liandry's
                self._item_to_dict(3157),  # Zhonya's
            ])
        elif champion.role in ['Top', 'Tank']:
            core.extend([
                self._item_to_dict(3068),  # Sunfire
                self._item_to_dict(3075),  # Thornmail
            ])

        return core[:3]  # Max 3 core items

    def _generate_situational_items(
        self,
        champion: Champion,
        enemy_analysis: Dict,
        game_state: GameState
    ) -> Dict[str, List[Dict]]:
        """Generate situational item branches"""

        situational = {}

        # VS AP Heavy
        if enemy_analysis['is_ap_heavy']:
            situational['vs_ap_heavy'] = [
                self._item_to_dict(3111),  # Mercury's Treads
                self._item_to_dict(3065) if champion.role in ['Top', 'Tank'] else self._item_to_dict(3102),
            ]

        # VS AD Heavy
        if enemy_analysis['is_ad_heavy']:
            situational['vs_ad_heavy'] = [
                self._item_to_dict(3047),  # Plated Steelcaps
                self._item_to_dict(3075) if champion.role in ['Top', 'Tank'] else self._item_to_dict(3157),
            ]

        # VS Healers
        if enemy_analysis['has_healer']:
            if champion.role == 'ADC':
                situational['vs_healers'] = [self._item_to_dict(3033)]  # Mortal Reminder
            else:
                situational['vs_healers'] = [self._item_to_dict(6609)]  # Chempunk

        # When Leading
        if game_state == GameState.LEADING:
            situational['when_ahead'] = [
                self._item_to_dict(3153) if champion.role == 'ADC' else self._item_to_dict(6653)
            ]

        # When Losing
        if game_state == GameState.LOSING:
            situational['when_behind'] = [
                self._item_to_dict(3110) if champion.role in ['Top', 'Tank'] else self._item_to_dict(3157)
            ]

        # VS Assassins
        if enemy_analysis['assassin_count'] >= 2:
            if champion.role in ['ADC', 'Mage', 'Mid']:
                situational['vs_assassins'] = [
                    self._item_to_dict(3157),  # Zhonya's for mages
                ]

        return situational

    def _generate_early_game_items(self, champion: Champion, enemy_analysis: Dict) -> List[Dict]:
        """Items for first 10 minutes"""
        early = []

        # Boots
        if champion.role == 'ADC':
            early.append(self._item_to_dict(3006))
        elif enemy_analysis['is_ap_heavy']:
            early.append(self._item_to_dict(3111))
        else:
            early.append(self._item_to_dict(3047))

        return early

    def _generate_mid_game_items(
        self,
        champion: Champion,
        enemy_analysis: Dict,
        game_state: GameState
    ) -> List[Dict]:
        """Items for 10-25 minutes"""
        mid = []

        # First core item
        if champion.role == 'ADC':
            mid.append(self._item_to_dict(6672))  # Kraken
        elif champion.role in ['Mid', 'Mage']:
            mid.append(self._item_to_dict(6653))  # Liandry's
        elif champion.role in ['Top', 'Tank']:
            mid.append(self._item_to_dict(3068))  # Sunfire

        # Situational mid-game
        if enemy_analysis['has_healer']:
            if champion.role == 'ADC':
                mid.append(self._item_to_dict(3033))

        return mid

    def _generate_late_game_items(self, champion: Champion, strategy: str) -> List[Dict]:
        """Items for 25+ minutes"""
        late = []

        if champion.role == 'ADC':
            late.append(self._item_to_dict(3031))  # IE
        elif champion.role in ['Mid', 'Mage']:
            late.append(self._item_to_dict(3135))  # Void Staff

        return late

    def _generate_explanation(
        self,
        champion: Champion,
        enemy_analysis: Dict,
        strategy: str,
        game_state: GameState
    ) -> str:
        """Generate human-readable explanation of the build"""

        parts = []
        parts.append(f"Build for {champion.name} ({champion.role})")

        if game_state == GameState.LEADING:
            parts.append("🔥 When ahead: Focus on snowballing with damage items")
        elif game_state == GameState.LOSING:
            parts.append("🛡️ When behind: Prioritize defensive items and scaling")

        if enemy_analysis['is_ap_heavy']:
            parts.append(f"⚡ Enemy is AP-heavy ({enemy_analysis['ap_count']} AP) → Build MR early")
        elif enemy_analysis['is_ad_heavy']:
            parts.append(f"⚔️ Enemy is AD-heavy ({enemy_analysis['ad_count']} AD) → Build Armor early")

        if enemy_analysis['has_healer']:
            parts.append("💉 Enemy has healers → Anti-heal is critical")

        if enemy_analysis['threats']:
            parts.append(f"🎯 Key threats: {', '.join(enemy_analysis['threats'])}")

        return " | ".join(parts)

    def _item_to_dict(self, item_id: int) -> Dict:
        """Convert item ID to dictionary with all info"""
        item = self.items.get(item_id, {})
        return {
            'id': item_id,
            'name': item.get('name', f'Item {item_id}'),
            'cost': item.get('cost', 0),
            'stats': item.get('stats', {}),
            'categories': [c.value for c in item.get('categories', [])],
            'good_against': item.get('good_against', []),
            'synergizes_with': item.get('synergizes_with', []),
            'power_spike': item.get('power_spike', 'mid')
        }


def test_dynamic_builds():
    """Test the dynamic build generator"""
    print("=" * 80)
    print("DYNAMIC BUILD GENERATOR TEST")
    print("=" * 80)

    generator = DynamicBuildGenerator()

    # Test Scenario 1: ADC vs AP-heavy team
    print("\n[TEST 1] ADC (MissFortune) vs AP-Heavy Team")
    print("-" * 40)

    user_champ = Champion("MissFortune", "ADC")
    ally_team = [
        Champion("MissFortune", "ADC"),
        Champion("Leona", "Support"),
        Champion("Darius", "Top"),
        Champion("Lee Sin", "Jungle"),
        Champion("Ahri", "Mid")
    ]
    enemy_team = [
        Champion("Lux", "Support"),  # Support, not Mid!
        Champion("Syndra", "Mid"),
        Champion("Malphite", "Top"),
        Champion("Evelynn", "Jungle"),
        Champion("Jinx", "ADC")
    ]

    build = generator.generate_build_path(
        user_champ,
        ally_team,
        enemy_team,
        GameState.EVEN
    )

    print(f"\n📋 {build.explanation}\n")
    print("Core Items (Always Buy):")
    for item in build.core_items:
        print(f"  → {item['name']} ({item['cost']}g)")

    print("\nEarly Game (0-10 min):")
    for item in build.early_game:
        print(f"  → {item['name']}")

    print("\nMid Game (10-25 min):")
    for item in build.mid_game:
        print(f"  → {item['name']}")

    print("\nSituational Options:")
    for condition, items in build.situational_items.items():
        print(f"  {condition.replace('_', ' ').title()}:")
        for item in items:
            print(f"    → {item['name']}")

    # Test Scenario 2: Tank when losing
    print("\n\n[TEST 2] Tank (Nautilus) When Behind vs Healers")
    print("-" * 40)

    user_champ2 = Champion("Nautilus", "Support")
    enemy_team2 = [
        Champion("Soraka", "Support"),
        Champion("Zed", "Mid"),
        Champion("Darius", "Top"),
        Champion("Graves", "Jungle"),
        Champion("Vayne", "ADC")
    ]

    build2 = generator.generate_build_path(
        user_champ2,
        ally_team,
        enemy_team2,
        GameState.LOSING
    )

    print(f"\n📋 {build2.explanation}\n")
    print("Core Items:")
    for item in build2.core_items:
        print(f"  → {item['name']}")

    print("\nSituational:")
    for condition, items in build2.situational_items.items():
        print(f"  {condition.replace('_', ' ').title()}:")
        for item in items:
            print(f"    → {item['name']}")

    print("\n" + "=" * 80)
    print("✅ TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_dynamic_builds()
