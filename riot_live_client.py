"""
Riot Games Live Client Data API Integration
============================================

Holt Echtzeit-Daten aus laufenden League of Legends Spielen.

Offizielle Dokumentation:
https://developer.riotgames.com/docs/lol#game-client-api

API läuft lokal auf: https://127.0.0.1:2999/liveclientdata/

Author: Merlin Mechler
"""

import requests
import urllib3
from typing import Optional, Dict, List
import time

# Disable SSL warnings (Riot uses self-signed certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RiotLiveClient:
    """Client für Riot Games Live Client Data API"""

    BASE_URL = "https://127.0.0.1:2999/liveclientdata"

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Riot uses self-signed cert

    def is_game_running(self) -> bool:
        """
        Prüft ob gerade ein Spiel läuft

        Returns:
            bool: True wenn Spiel läuft, False sonst
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/gamedata",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False

    def get_all_game_data(self) -> Optional[Dict]:
        """
        Holt alle Spiel-Daten (vollständiger Dump)

        Returns:
            Dict mit allen Spiel-Daten oder None wenn kein Spiel läuft
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/allgamedata",
                timeout=5
            )

            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching game data: {e}")
            return None

    def get_active_player(self) -> Optional[Dict]:
        """
        Holt Daten des aktiven Spielers (du selbst)

        Returns:
            Dict mit Spieler-Daten oder None
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/activeplayer",
                timeout=2
            )

            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def extract_team_data(self, all_data: Dict) -> Dict:
        """
        Extrahiert Team-Daten für unser ML-Modell

        Args:
            all_data: Vollständige Spiel-Daten von get_all_game_data()

        Returns:
            Dict mit strukturierten Team-Daten für Prediction
        """
        if not all_data:
            return {}

        all_players = all_data.get('allPlayers', [])
        events = all_data.get('events', {}).get('Events', [])
        game_data = all_data.get('gameData', {})

        # Separate teams
        blue_team = [p for p in all_players if p.get('team') == 'ORDER']
        red_team = [p for p in all_players if p.get('team') == 'CHAOS']

        # Calculate team stats
        blue_stats = self._calculate_team_stats(blue_team, events, team='ORDER')
        red_stats = self._calculate_team_stats(red_team, events, team='CHAOS')

        return {
            'game_time': game_data.get('gameTime', 0),
            'game_mode': game_data.get('gameMode', 'CLASSIC'),
            'map_number': game_data.get('mapNumber', 11),
            'blue_team': {
                'champions': [p.get('championName') for p in blue_team],
                'summoners': [p.get('summonerName') for p in blue_team],
                **blue_stats
            },
            'red_team': {
                'champions': [p.get('championName') for p in red_team],
                'summoners': [p.get('summonerName') for p in red_team],
                **red_stats
            },
            'raw_data': all_data  # Für Debugging
        }

    def _calculate_team_stats(self, team_players: List[Dict], events: List[Dict], team: str) -> Dict:
        """
        Berechnet aggregierte Team-Stats

        Args:
            team_players: Liste der Spieler im Team
            events: Liste aller Game-Events
            team: 'ORDER' oder 'CHAOS'

        Returns:
            Dict mit Team-Stats
        """
        stats = {
            'kills': 0,
            'deaths': 0,
            'assists': 0,
            'total_gold': 0,
            'avg_level': 0,
            'towers_destroyed': 0,
            'dragons_killed': 0,
            'barons_killed': 0,
            'heralds_killed': 0,
            'vision_score': 0
        }

        # Aggregate player stats
        for player in team_players:
            scores = player.get('scores', {})
            stats['kills'] += scores.get('kills', 0)
            stats['deaths'] += scores.get('deaths', 0)
            stats['assists'] += scores.get('assists', 0)
            stats['total_gold'] += player.get('currentGold', 0)
            stats['avg_level'] += player.get('level', 0)
            stats['vision_score'] += scores.get('wardScore', 0)

        # Calculate averages
        if len(team_players) > 0:
            stats['avg_level'] = stats['avg_level'] / len(team_players)

        # Count objectives from events
        for event in events:
            event_name = event.get('EventName', '')

            # Towers
            if event_name == 'TurretKilled':
                killer_team = event.get('KillerName', '')
                # Check if killer is from this team
                if any(killer_team == p.get('summonerName') for p in team_players):
                    stats['towers_destroyed'] += 1

            # Dragons
            elif event_name == 'DragonKill':
                killer = event.get('KillerName', '')
                if any(killer == p.get('summonerName') for p in team_players):
                    stats['dragons_killed'] += 1

            # Baron
            elif event_name == 'BaronKill':
                killer = event.get('KillerName', '')
                if any(killer == p.get('summonerName') for p in team_players):
                    stats['barons_killed'] += 1

            # Herald
            elif event_name == 'HeraldKill':
                killer = event.get('KillerName', '')
                if any(killer == p.get('summonerName') for p in team_players):
                    stats['heralds_killed'] += 1

        return stats

    def format_for_prediction(self, team_data: Dict) -> Dict:
        """
        Formatiert Team-Daten für unser Win-Prediction Model

        Args:
            team_data: Output von extract_team_data()

        Returns:
            Dict im Format das unser ML-Model erwartet
        """
        blue = team_data.get('blue_team', {})
        red = team_data.get('red_team', {})

        return {
            'game_duration': int(team_data.get('game_time', 0) / 60),  # Convert to minutes
            'blue_champions': blue.get('champions', []),
            'red_champions': red.get('champions', []),
            'blue_kills': blue.get('kills', 0),
            'blue_deaths': blue.get('deaths', 0),
            'blue_assists': blue.get('assists', 0),
            'blue_gold': blue.get('total_gold', 0),
            'blue_towers': blue.get('towers_destroyed', 0),
            'blue_dragons': blue.get('dragons_killed', 0),
            'blue_barons': blue.get('barons_killed', 0),
            'blue_vision_score': blue.get('vision_score', 0),
            'red_kills': red.get('kills', 0),
            'red_deaths': red.get('deaths', 0),
            'red_assists': red.get('assists', 0),
            'red_gold': red.get('total_gold', 0),
            'red_towers': red.get('towers_destroyed', 0),
            'red_dragons': red.get('dragons_killed', 0),
            'red_barons': red.get('barons_killed', 0),
            'red_vision_score': red.get('vision_score', 0)
        }

    def get_live_prediction_data(self) -> Optional[Dict]:
        """
        Convenience-Methode: Holt Daten und formatiert sie direkt für Prediction

        Returns:
            Dict bereit für Win-Prediction oder None
        """
        all_data = self.get_all_game_data()
        if not all_data:
            return None

        team_data = self.extract_team_data(all_data)
        return self.format_for_prediction(team_data)


def test_live_api():
    """Test-Funktion - zeigt ob API erreichbar ist"""
    print("=" * 80)
    print("RIOT LIVE CLIENT API TEST")
    print("=" * 80)

    client = RiotLiveClient()

    print("\n[1] Checking if game is running...")
    is_running = client.is_game_running()
    print(f"    → Game running: {is_running}")

    if not is_running:
        print("\n⚠️  Kein Spiel läuft gerade!")
        print("    Starte ein Practice Game oder Custom Game um die API zu testen.")
        return

    print("\n[2] Fetching all game data...")
    all_data = client.get_all_game_data()

    if all_data:
        print(f"    ✓ Data received")
        print(f"    → Game Mode: {all_data.get('gameData', {}).get('gameMode')}")
        print(f"    → Game Time: {all_data.get('gameData', {}).get('gameTime'):.1f}s")
        print(f"    → Players: {len(all_data.get('allPlayers', []))}")

        print("\n[3] Extracting team data...")
        team_data = client.extract_team_data(all_data)

        blue = team_data.get('blue_team', {})
        red = team_data.get('red_team', {})

        print(f"\n    Blue Team:")
        print(f"      Champions: {', '.join(blue.get('champions', []))}")
        print(f"      Kills: {blue.get('kills', 0)} | Gold: {blue.get('total_gold', 0):,}")

        print(f"\n    Red Team:")
        print(f"      Champions: {', '.join(red.get('champions', []))}")
        print(f"      Kills: {red.get('kills', 0)} | Gold: {red.get('total_gold', 0):,}")

        print("\n[4] Formatting for prediction...")
        pred_data = client.format_for_prediction(team_data)
        print(f"    ✓ Ready for ML model")
        print(f"    → Blue Win Features: {pred_data.get('blue_kills')}K / {pred_data.get('blue_deaths')}D / {pred_data.get('blue_assists')}A")

    else:
        print("    ✗ Failed to fetch data")

    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_live_api()
