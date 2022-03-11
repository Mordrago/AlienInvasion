import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Klasa przeznaczona do zarządzania pojedynczym obcym"""

    def __init__(self, ai_game):
        """Inicjalizacja obcego i jego polozenie początkowe"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # wczytywanie obrazu stattku kosmicznego i pobranie jego prostokąta
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Umieszczenie nowego obcego w pobliżu lewego górego rogu ekranu
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Przechowywanie poziomego położenia obecgo
        self.x = float(self.rect.x)

    def check_edges(self):
        """Zwraca true jeżeli obcy zmajduje sie na krawedzi"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        """Przesuniecie obcego w prawo lub  lewo"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x