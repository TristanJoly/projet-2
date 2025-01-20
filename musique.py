import tkinter as tk
from tkinter import ttk
import math
from tkinter import Scale, Button, Listbox, END, Label
import pygame
class MusicPlayer:
    def __init__(self, initial_musique_list, initial_volume=0.5):
        """"
        Prend en entrée une liste initial_musique_liste, une liste de str, et peut prendre en entrée un flottant correspondant au volume.
        ----------------------------------------------------------------------------------------------
        Crée le dessin correspondant au réservoir vide
        ----------------------------------------------------------------------------------------------
        """
        assert type(initial_musique_list) == list
        assert type (initial_musique_list[0]) == str
        assert type  (initial_volume) == float
        self.musique_list = initial_musique_list
        self.musique_index = 0
        self.volume = initial_volume
        pygame.init()
        pygame.mixer.init()
        if self.musique_list:
            self.load_musique(0)
        
    
    def load_musique(self,n):
        """"
        Prend en entrée l'objet de la classe créé
        ----------------------------------------------------------------------------------------------
        Permet de charger la musique correspondant a l'index défini, initial
        Ou alors modifié lors d'un appel de fonction.
        ----------------------------------------------------------------------------------------------
        """
        pygame.mixer.music.load(self.musique_list[n])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops=-1)  # -1 pour jouer en boucle infinie
    
    def set_volume(self, volume):
        """"
        Prend en entrée l'objet créé ainsi qu'un flottant correspondant à un nouveau volume.
        ----------------------------------------------------------------------------------------------
        Permet de modifier le volume de la musique. 
        ----------------------------------------------------------------------------------------------
        """
        self.volume = max(0.0, min(1.0, volume))#permet de s'assurer que le volume reste un floatant et ne depasse pas 1.
        pygame.mixer.music.set_volume(self.volume)
    
    def stop_musique(self):#Permet de arreter la musique
        pygame.mixer.music.stop()
    
    def pause_musique(self):#Permet de soit mettre en pause la musique , ou bien si elle l'est deja , de la remettre en route.
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def next_musique(self):#Permet de passer à la musique suivante selon l'indexe, appele la fonction load
        self.musique_index = (self.musique_index + 1) % len(self.musique_list)
        self.load_musique()
    
    def previous_musique(self):#Permet de passer à la musique précédante selon l'indexe, appele la fonction load
        self.musique_index = (self.musique_index - 1) % len(self.musique_list)
        self.load_musique()
