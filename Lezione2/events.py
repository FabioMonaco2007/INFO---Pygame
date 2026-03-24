import pygame
import sys

# ------------------------------------------------------------------ #
# COSTANTI                                                           #
# ------------------------------------------------------------------ #

SCREEN_W = 800
SCREEN_H = 600
FPS      = 60

BALL_RADIUS = 30
BALL_SPEED  = 4  #pixel per frame (tastiera)

BG_COLOR   = ( 30,  30,  30)
TEXT_COLOR = (200, 200, 200)

COLORS = [
    (220,  80,  80),   #rosso
    ( 80, 180, 220),   #azzurro
    ( 80, 220, 120),   #verde
    (220, 200,  80),   #giallo
    (180,  80, 220),   #viola
]

# ------------------------------------------------------------------ #
# INIZIALIZZAZIONE                                                   #
# ------------------------------------------------------------------ #

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Pallina interattiva")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 22)

# ------------------------------------------------------------------ #
# STATO                                                              #
# ------------------------------------------------------------------ #

ball_x      = SCREEN_W // 2
ball_y      = SCREEN_H // 2
color_index = 0
ball_color  = COLORS[color_index]

# ------------------------------------------------------------------ #
# FUNZIONI DI SUPPORTO                                               #
# ------------------------------------------------------------------ #

def clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(value, max_val))

def point_in_circle(px: int, py: int, cx: int, cy: int, radius: int) -> bool:
    """
    Usa il teorema di Pitagora: a² + b² = c²
    Se la distanza al quadrato tra il punto e il centro è minore del raggio al quadrato,
    il punto è dentro il cerchio.
    """
    dx = px - cx
    dy = py - cy
    distanza_quadrata = dx**2 + dy**2
    return distanza_quadrata <= radius**2

def next_color(current_index: int) -> tuple:
    """
    Calcola il prossimo indice usando l'operatore modulo per ricominciare da zero.
    """
    nuovo_indice = (current_index + 1) % len(COLORS)
    nuovo_colore = COLORS[nuovo_indice]
    return nuovo_indice, nuovo_colore

# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                    #
# ------------------------------------------------------------------ #

running = True

while running:

    # ---- 1. EVENTI ------------------------------------------------ #

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Gestione clic del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Tasto sinistro
                mouse_x, mouse_y = event.pos
                if point_in_circle(mouse_x, mouse_y, ball_x, ball_y, BALL_RADIUS):
                    color_index, ball_color = next_color(color_index)

    # ---- 2. AGGIORNA ---------------------------------------------- #

    keys = pygame.key.get_pressed()

    #Movimento continuo
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= BALL_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ball_x += BALL_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        ball_y -= BALL_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ball_y += BALL_SPEED

    #Limitiamo la pallina dentro lo schermo (tenendo conto del raggio)
    ball_x = clamp(ball_x, BALL_RADIUS, SCREEN_W - BALL_RADIUS)
    ball_y = clamp(ball_y, BALL_RADIUS, SCREEN_H - BALL_RADIUS)

    # ---- 3. DISEGNA ----------------------------------------------- #

    screen.fill(BG_COLOR)

    #Disegno della pallina
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), BALL_RADIUS)

    #HUD: istruzioni a schermo
    hints = [
        "Frecce - WASD: muovi la pallina",
        "Clic sinistro sulla pallina: cambia colore",
    ]
    for i, line in enumerate(hints):
        surf = font.render(line, True, TEXT_COLOR)
        screen.blit(surf, (10, 10 + i * 28))

    pygame.display.flip()
    clock.tick(FPS)

# ------------------------------------------------------------------ #
# USCITA                                                             #
# ------------------------------------------------------------------ #

pygame.quit()
sys.exit()