import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Klasa przeznaczona do zarządzania pociskami"""

    def __init__(self, ai_game):
        """Utowrzenie obiektu pocisk w aktualnym położeniu statku"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Utowrzenie prostokąta pocisku w punkcie (0,0),  następnie zdefiniowanie dla niego odpowiedniego polzoenia
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_hight)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Położenie pocisku jest zdefiniowane za pomoa float
        self.y = float(self.rect.y)

    def update(self):
        """Poruszanie pociskiem po ekranie"""
        #Uaktualnienie położenia pocisku
        self.y -= self.settings.bullet_speed
        #Uaktualneinie położenia prostokąta
        self.rect.y = self.y

    def draw_bullet(self):
        """Wysweitlanie pocisku an ekranie"""
        pygame.draw.rect(self.screen, self.color, self.rect)


