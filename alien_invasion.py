import json
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from alien import Alien
from bullet import Bullet
from scoreboard import Scoreboard


class AlienInvasion:
    """Ogolna klasa przeznaczona do zarządzania zasobami i sposobem działania gry"""

    def __init__(self):
        """Inicjalizacja gry i utowrzenie jej zasobów"""
        pygame.init()
        self.settings = Settings()
        #Tryb w oknie
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #Tryb pełnoekranowy
        """self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""
        pygame.display.set_caption("Inwazja obcych")

        #Utowrzenie Game_stats do danych statystycznych
        #Utworzenie obiektu scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self._create_fleet()

        #Utworzenie przycisku gra
        self.play_button = Button(self, "Play")

        # zdefiniowaie koloru tła
        self.bg_color = (self.settings.bg_color)

    def run_game(self):
        """Rozpoczece petli glownej gry"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Reakcja na zdarzenie generowane przez klawaiature i mysz."""
        # Oczekiwanie na naciśniecie klawisza lub myszy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._shut_down_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _shut_down_game(self):
        #Wyłączenie gry
        with open('best_score.json', 'w') as file_object:
            json.dump(self.stats.high_score, file_object)

        sys.exit()

    def _start_game(self):
        """Rozpoczęcie gry"""
        # Wyzerowanie danych statystycznych gry.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Usunięcie zawartosci listy alien i bullets
        self.aliens.empty()
        self.bullets.empty()

        # Utworzenie nowej floty i wyśrodkowanie staktu
        self._create_fleet()
        self.ship.center_ship()

        # Ukrycie kursora myszy
        pygame.mouse.set_visible(False)


    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie gry po kliknieciu przycisku"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_keydown_events(self, event):
        """Reakcja na nacisniecie klawisza"""
        if event.key == pygame.K_RIGHT:
            # Przesuwanie statku w prawo
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Przesuwanie statku w lewo
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._shut_down_game()
        elif event.key == pygame.K_g and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reakcja na opuszczenie klawisza"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Utowrzenie pocisku i dodanie do grupy pociskow"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Zarządzanie pociskami"""
        #Uaktualnianie położenia pociku
        self.bullets.update()

        #Usuwanie pociskow poza ekranem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Sprawdzenie kolizji pocisku z obcym i usunęcie pocisku i obcego
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #dodanie puntków
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Nowa flota
        if not self.aliens:
            #Usuniecie i zwiekszenie predkosci
            self.bullets.empty()
            self._create_fleet()
            self.settings.incrase_speed()

            #Dodanie poziomu
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Utworzenie floty obcych"""
        #Utowrzenie obcego i ustalenie liczby obcych, którzy zmieszcza się w rzędzie.
        #Odleglosc pomiedzy poszczegolnymi obcymi jest jest równa szerokości obcego
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        #ustalenie rzędów obcych
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Utworzenie pelnej floty obcych
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Utworzenie obcego i umieszczenie go w rzędzie"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Sprawdzanie czy obcy dotarł do krawędzi"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Przesunieie całej floty w dół i zmiana kierunku poruszania"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Uaktualnienie pozycji wszystkich obcych"""
        self._check_fleet_edges()
        self.aliens.update()

        #Wykrywanie kolizji między graczem a statkiem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Wyszukiwanie obcych na dolnym ekranie
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Reakcja na zderzenie s UFO"""
        if self.stats.ship_left > 0:
            #Zmniejszenie liczby zyć
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            #Usunięcie zawartośći ekranu
            self.aliens.empty()
            self.bullets.empty()

            #Utworzenie nowej floty i wysrodkoanie statku
            self._create_fleet()
            self.ship.center_ship()

            #Pauza
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Sprawdzenie czy jakis obcy dotarł na dół ekranu"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #To samo co ze zderzeniem ze statkiem
                self._ship_hit()
                break

    def _update_screen(self):
        # Odswiezanie ekranu z kazda iteracja
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Wyświetlanie informacji o putkacji
        self.sb.show_score()

        #Wyświetlamy tylko wtedy gdy gra jest nieaktywna
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Wyswietlanie ostatnio zmodyfikowanego ekranu
        pygame.display.flip()


if __name__ == '__main__':
    #Utworzenie egzmptlarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()