import pygame
import math
from teste_labyrinthe import Labyrinthe, labyrinthe_to_game_map, plus_court_chemin_D2
import tkinter as tk
pygame.init()
from musique import *




def get_screen_size():
    """
    input
    -----------------------
    Aucune (fonction sans paramètres)
    -----------------------
    Fonctionnement
    -----------------------
    Obtient la taille de l'écran de l'utilisateur en utilisant tkinter.
    -----------------------
    output
    -----------------------
    Retourne une largeur (int) et une hauteur (int) de l'écran.
    """
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width, height

def transform_path(path):
    """
    input
    -----------------------
    path : liste de tuples (int, int)
        Liste représentant les coordonnées d'un chemin.
    -----------------------
    Fonctionnement
    -----------------------
    Transforme un chemin en ajustant chaque coordonnée (y, x) pour les adapter à un repère élargi.
    Chaque coordonnée est multipliée par 2 et augmentée de 1.
    -----------------------
    output
    -----------------------
    Liste de tuples (int, int) avec les coordonnées transformées.
    """
    return [(2 * y + 1, 2 * x + 1) for (y, x) in path]



def draw_minimap():
    """
    input
    -----------------------
    Aucune (utilise des variables globales comme screen, game_map, etc.)
    -----------------------
    Fonctionnement
    -----------------------
    Dessine la mini-carte en haut à gauche de l'écran avec les murs, le champ de vision et le chemin le plus court.
    -----------------------
    output
    -----------------------
    Aucun (dessine directement sur l'écran pygame).
    """
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = LIGHT_GREEN if tile == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (x * TILE_SIZE * MINIMAP_SCALE, y * TILE_SIZE * MINIMAP_SCALE,
                 TILE_SIZE * MINIMAP_SCALE, TILE_SIZE * MINIMAP_SCALE),
            )
    if transformed_best_path:
        for (l, c) in transformed_best_path:
            pygame.draw.rect(
                screen,
                BLUE,
                (c * TILE_SIZE * MINIMAP_SCALE, l * TILE_SIZE * MINIMAP_SCALE,
                 TILE_SIZE * MINIMAP_SCALE, TILE_SIZE * MINIMAP_SCALE),
            )
    for i in range(0, 120):
        ray_angle = player_angle - FOV / 2 + FOV * (i / 120)
        depth = 0
        while depth < 800:
            depth += 2
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)
            tile_x = int(target_x / TILE_SIZE)
            tile_y = int(target_y / TILE_SIZE)
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                if game_map[tile_y][tile_x] == 1:
                    break
            pygame.draw.line(
                screen,
                RED,
                (int(player_x * MINIMAP_SCALE), int(player_y * MINIMAP_SCALE)),
                (int(target_x * MINIMAP_SCALE), int(target_y * MINIMAP_SCALE)),
                1,
            )

    pygame.draw.circle(
        screen,
        RED,
        (int(player_x * MINIMAP_SCALE), int(player_y * MINIMAP_SCALE)),
        5,
    )

def cast_rays():
    """
    input
    -----------------------
    Aucune (utilise des variables globales comme screen, game_map, player_x, player_y, etc.)
    -----------------------
    Fonctionnement
    -----------------------
    Trace des rayons à partir de la position du joueur dans son champ de vision. 
    Simule un effet 3D en calculant la profondeur des murs rencontrés.
    -----------------------
    output
    -----------------------
    Aucun (dessine directement sur l'écran pygame).
    """
    pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, WIDTH, HEIGHT // 2))
    is_on_dijkstra_path = (int(player_y / TILE_SIZE), int(player_x / TILE_SIZE)) in transformed_best_path
    floor_color = RED if is_on_dijkstra_path else LIGHT_GREEN
    pygame.draw.rect(screen, floor_color, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    ray_angle = player_angle - FOV / 2
    num_rays = 120
    step_angle = FOV / num_rays
    for ray in range(num_rays):
        for depth in range(1, 800):
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)
            tile_x = int(target_x / TILE_SIZE)
            tile_y = int(target_y / TILE_SIZE)
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                if game_map[tile_y][tile_x] == 1:
                    wall_height = HEIGHT / (depth * 0.01)
                    intensity = max(30, 255 - depth * 1.2)
                    wall_color = (
                        int(BROWN[0] * intensity / 255),
                        int(BROWN[1] * intensity / 255),
                        int(BROWN[2] * intensity / 255),
                    )
                    pygame.draw.rect(
                        screen,
                        wall_color,
                        (
                            ray * (WIDTH // num_rays),
                            HEIGHT // 2 - wall_height // 2,
                            WIDTH // num_rays,
                            wall_height,
                        ),
                    )
                    is_edge = (
                        tile_x > 0 and game_map[tile_y][tile_x - 1] == 0 or
                        tile_x < MAP_WIDTH - 1 and game_map[tile_y][tile_x + 1] == 0 or
                        tile_y > 0 and game_map[tile_y - 1][tile_x] == 0 or
                        tile_y < MAP_HEIGHT - 1 and game_map[tile_y + 1][tile_x] == 0
                    )

                    if is_edge:
                        pygame.draw.line(
                            screen,
                            (0, 0, 0),
                            (ray * (WIDTH / num_rays), HEIGHT / 2 - wall_height / 2),
                            (ray * (WIDTH / num_rays), HEIGHT / 2 + wall_height / 2),
                            2,
                        )
                    break
        ray_angle += step_angle

def main():
    """
    input
    -----------------------
    Aucune (fonction principale sans paramètres)
    -----------------------
    Fonctionnement
    -----------------------
    Initialise le jeu, gère les entrées utilisateur et met à jour l'état du jeu à chaque frame.
    -----------------------
    output
    -----------------------
    Aucun (le jeu tourne jusqu'à ce que l'utilisateur le quitte).
    """
    global player_x, player_y, player_angle, FOV
    move_speed = 3
    rotation_speed = 0.05
    clock = pygame.time.Clock()
    running = True
    music = MusicPlayer(["musique.mp3"])

    while running:
        screen.fill(BLACK)
        cursor_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_z]:
            new_x = player_x + move_speed * math.cos(player_angle)
            new_y = player_y + move_speed * math.sin(player_angle)
            if game_map[int(new_y / TILE_SIZE)][int(new_x / TILE_SIZE)] == 0:
                player_x, player_y = new_x, new_y
            moving = True
        if keys[pygame.K_s]:
            new_x = player_x - move_speed * math.cos(player_angle)
            new_y = player_y - move_speed * math.sin(player_angle)
            if game_map[int(new_y / TILE_SIZE)][int(new_x / TILE_SIZE)] == 0:
                player_x, player_y = new_x, new_y
            moving = True
        if keys[pygame.K_d]:
            new_x = player_x - move_speed * math.sin(player_angle)
            new_y = player_y + move_speed * math.cos(player_angle)
            if game_map[int(new_y / TILE_SIZE)][int(new_x / TILE_SIZE)] == 0:
                player_x, player_y = new_x, new_y
            moving = True
        if keys[pygame.K_q]:
            new_x = player_x + move_speed * math.sin(player_angle)
            new_y = player_y - move_speed * math.cos(player_angle)
            if game_map[int(new_y / TILE_SIZE)][int(new_x / TILE_SIZE)] == 0:
                player_x, player_y = new_x, new_y
            moving = True
        if keys[pygame.K_LEFT]:
            player_angle -= rotation_speed
        if keys[pygame.K_RIGHT]:
            player_angle += rotation_speed
        if keys[pygame.K_UP]:
            FOV = min(math.pi, FOV + 0.01)
        if keys[pygame.K_DOWN]:
            FOV = max(math.pi / 6, FOV - 0.01)
        if keys[pygame.K_LSHIFT]:
            move_speed += 3
        if keys[pygame.K_RSHIFT]:
            move_speed -= 3
        if keys[pygame.K_ESCAPE]:
            running = False
        cast_rays()
        draw_minimap()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

WIDTH, HEIGHT = get_screen_size()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doom-like Ray Tracing")
BLACK = (0, 0, 0)
LIGHT_GRAY = (192, 192, 192)
LIGHT_BLUE = (135, 206, 235)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
labyrinthe = Labyrinthe(5,5)
labyrinthe.generer_labyrinthe_growing_tree()
game_map = labyrinthe_to_game_map(labyrinthe)
start = (0, 0)
end = (labyrinthe.h - 1, labyrinthe.w - 1)
best_path = plus_court_chemin_D2(labyrinthe, start, end)
print(best_path)

TILE_SIZE = 64
MAP_WIDTH = len(game_map[0])
MAP_HEIGHT = len(game_map)
MINIMAP_SCALE = 0.1
player_x, player_y = TILE_SIZE * (start[1] * 2 + 1), TILE_SIZE * (start[0] * 2 + 1)
player_angle = 0
FOV = math.pi / 3
transformed_best_path = transform_path(best_path)
if __name__ == "__main__":
    main()
