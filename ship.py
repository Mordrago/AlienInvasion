import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Klasa przeznaczona do zarządzania statkiem kosmcznym"""

    def __init__(self, ai_game):
        """Inicjalizacja statku kosmicznego i jego polozenie początkowe"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #wczytywanie obrazu stattku kosmicznego i pobranie jego prostokąta
        self.image = pygame.image.load('images/ship2.bmp')
        self.rect = self.image.get_rect()

        #Kazdy nowy statek pojawia sie na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom

        #Położenie poziome statku jest przetrzymywane w liczbie zmiennoprzecinkowej

        self.x = float(self.rect.x)

        #Opcja wskazujaca na poruszanie sie statku
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Uaktualnenie położenia statku na podstawie opcji wskazuajcej an jego ruch"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed

        #Uaktualnienie obiektu rect na podstawie wartsci self.x
        self.rect.x = self.x

    def blitme(self):
        """Wyswietlanie statku w jego aktualnym polozeniu"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Umieszczanie statku na środku przy dolnej krawędzi ekranu"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
