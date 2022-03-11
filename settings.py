class Settings:
    """Klasa przeznaczona do przechwywania ustawien gry"""

    def __init__(self):
        """"Inicjalizacja ustawien gry"""
        #Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        #Ustawienie dotyczące statku
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Ustawienia pocisku
        self.bullet_width = 3
        self.bullet_hight = 17
        self.bullet_color = (200, 60, 50)
        self.bullet_allowed = 3

        #Ustawienia obcych
        self.fleet_drop_speed = 15

        #Zmiana szybkosci gry
        self.speedup_scale = 1.2

        #Zwiekszanie puntkow
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #Inicjalizacja ustawień, które ulegają zmianie
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.3

        # Wartość fleet_direction wyosząca 1 oznacza prwo a -1 lewo
        self.fleet_direction = 1

        #Punktacja
        self.alien_points = 50.0

    def incrase_speed(self):
        """Zmiana ustawien szybkosci"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        #zwiekszanie puntkow
        self.alien_points = int(self.score_scale * self.alien_points)