import pygame
import math

class Pistolet:
    def __init__(self, screen_width, screen_height):
        """
        input: screen_width (int), screen_height (int) - dimensions de l'écran.
        --------------------------------------------------------------------------
        Initialise l'objet Pistolet avec une position centrale, une liste de balles, et charge une image de pistolet.
        --------------------------------------------------------------------------
        output: Aucun, initialise les attributs de la classe.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullets = []  # Liste des balles
        self.bullet_speed = 15  # Vitesse des balles
        self.pistol_image = pygame.image.load("pistol.png")  # Image du pistolet
        self.pistol_image = pygame.transform.scale(self.pistol_image, (200, 100))  # Redimensionner
        self.center = (screen_width // 2, screen_height // 2)  # Centre de l'écran

    def draw_pistol(self, screen):
        """
        input: screen (pygame.Surface) - surface d'affichage.
        --------------------------------------------------------------------------
        Calcule l'angle de rotation pour orienter le pistolet vers le curseur, puis dessine le pistolet sur l'écran.
        --------------------------------------------------------------------------
        output: Aucun, dessine sur l'écran.
        """
        dx = self.center[0]
        dy = self.center[1]
        angle = math.degrees(math.atan2(-dy, dx))
        rotated_image = pygame.transform.rotate(self.pistol_image, angle)
        rect = rotated_image.get_rect(center=self.center)
        screen.blit(rotated_image, rect.topleft)

    def draw_crosshair(self, screen):
        """
        input: screen (pygame.Surface) - surface d'affichage.
        --------------------------------------------------------------------------
        Dessine une croix au centre de l'écran pour représenter un viseur.
        --------------------------------------------------------------------------
        output: Aucun, dessine sur l'écran.
        """
        pygame.draw.line(screen, (255, 0, 0), (self.center[0] - 10, self.center[1]),
                         (self.center[0] + 10, self.center[1]), 2)
        pygame.draw.line(screen, (255, 0, 0), (self.center[0], self.center[1] - 10),
                         (self.center[0], self.center[1] + 10), 2)

    def fire(self):
        """
        input: Aucun.
        --------------------------------------------------------------------------
        Crée une balle partant du centre de l'écran et se dirigeant vers une direction donnée.
        --------------------------------------------------------------------------
        output: Ajoute une nouvelle balle à la liste des balles.
        """
        dx = self.center[0]
        dy = self.center[1]
        angle = math.atan2(dy, dx)
        bullet_dx = math.cos(angle) * self.bullet_speed
        bullet_dy = math.sin(angle) * self.bullet_speed
        self.bullets.append({
            "x": self.center[0],
            "y": self.center[1],
            "dx": bullet_dx,
            "dy": bullet_dy,
        })

    def update_bullets(self, screen):
        """
        input: screen (pygame.Surface) - surface d'affichage.
        --------------------------------------------------------------------------
        Met à jour la position des balles, les dessine à l'écran et les supprime si elles sortent des limites.
        --------------------------------------------------------------------------
        output: Aucun, met à jour la liste des balles et dessine sur l'écran.
        """
        for bullet in self.bullets[:]:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]
            pygame.draw.circle(screen, (255, 255, 0), (int(bullet["x"]), int(bullet["y"])), 5)
            if (bullet["x"] < 0 or bullet["x"] > self.screen_width or
                bullet["y"] < 0 or bullet["y"] > self.screen_height):
                self.bullets.remove(bullet)

### musique.py
import tkinter as tk
from tkinter import ttk
import math
from tkinter import Scale, Button, Listbox, END, Label
import pygame

class MusicPlayer:
    def __init__(self, initial_musique_list, initial_volume=0.5):
        """
        input: initial_musique_list (list[str]), initial_volume (float).
        --------------------------------------------------------------------------
        Initialise le lecteur de musique avec une liste de morceaux et un volume initial.
        --------------------------------------------------------------------------
        output: Aucun, initialise les attributs de la classe.
        """
        assert type(initial_musique_list) == list
        assert type(initial_musique_list[0]) == str
        assert type(initial_volume) == float
        self.musique_list = initial_musique_list
        self.musique_index = 0
        self.volume = initial_volume
        pygame.init()
        pygame.mixer.init()
        if self.musique_list:
            self.load_musique(0)

    def load_musique(self, n):
        """
        input: n (int) - index du morceau à charger.
        --------------------------------------------------------------------------
        Charge la musique correspondant à l'index donné et la joue en boucle.
        --------------------------------------------------------------------------
        output: Aucun.
        """
        pygame.mixer.music.load(self.musique_list[n])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops=-1)

    def set_volume(self, volume):
        """
        input: volume (float).
        --------------------------------------------------------------------------
        Change le volume de la musique jouée.
        --------------------------------------------------------------------------
        output: Aucun.
        """
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def stop_musique(self):
        """
        input: Aucun.
        --------------------------------------------------------------------------
        Arrête la musique en cours.
        --------------------------------------------------------------------------
        output: Aucun.
        """
        pygame.mixer.music.stop()

    def pause_musique(self):
        """
        input: Aucun.
        --------------------------------------------------------------------------
        Met la musique en pause ou reprend la lecture si elle est déjà en pause.
        --------------------------------------------------------------------------
        output: Aucun.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def next_musique(self):
        """
        input: Aucun.
        --------------------------------------------------------------------------
        Passe à la musique suivante dans la liste.
        --------------------------------------------------------------------------
        output: Aucun.
        """
        self.musique_index = (self.musique_index + 1) % len(self.musique_list)
        self.load_musique(self.musique_index)

    def previous_musique(self):
        """
        input: Aucun.
        --------------------------------------------------------------------------
        Revient à la musique précédente dans la liste.
        --------------------------------------------------------------------------
        output: Aucun.
        """
        self.musique_index = (self.musique_index - 1) % len(self.musique_list)
        self.load_musique(self.musique_index)
