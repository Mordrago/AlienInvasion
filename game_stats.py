import json


class GameStats:
    """Monitorowanie statystyk w grze"""

    def __init__(self, ai_game):
        """Inicjalizacja danych statystyczncyh"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Uruchamianie gry inwazja obcych w trybie nieaktywnym
        self.game_active = False

        #Najlepszy wynik
        with open('best_score.json', 'r') as file_object:
            self.high_score = json.load(file_object)
        self.level = 1


    def reset_stats(self):
        """Inicjalizacja danych statystycznych, ktore moga zmieniac sie pdozas gry"""
        self.ship_left = self.settings.ship_limit
        self.score = 0

