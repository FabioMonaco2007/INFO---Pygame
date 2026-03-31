import pygame
import sys
import time
import math

# ------------------------------------------------------------------ #
# COSTANTI                                                            #
# ------------------------------------------------------------------ #

#Finestra
SCREEN_W = 800
SCREEN_H = 600

#Barra del timer
BAR_X = 50
BAR_Y = 50
BAR_W = 700
BAR_H = 30
BAR_BG_COLOR = (100, 0, 0) 
BAR_FG_COLOR = (0, 200, 0)

#Testo
TEXT_COLOR = (255, 255, 255)

#Pallina
BALL_COLOR = (255, 255, 0)
BALL_EXPIRED = (128, 128, 128) 
BALL_RADIUS = 20

# ------------------------------------------------------------------ #
# FUNZIONI — Logica del timer                                          #
# ------------------------------------------------------------------ #

def time_elapsed(start: float) -> float:
    """Restituisce i secondi trascorsi sottraendo il tempo iniziale da quello attuale."""
    return time.time() - start


def time_remaining(start: float, duration: int) -> float:
    """Sottrae il tempo trascorso dalla durata totale, senza scendere sotto lo zero."""
    rimanente = duration - time_elapsed(start)
    return max(0.0, rimanente)


def is_expired(start: float, duration: int) -> bool:
    """Controlla se il tempo trascorso ha superato la durata impostata."""
    return time_elapsed(start) >= duration


def bar_fill_width(remaining: float, duration: int, bar_width: int) -> int:
    """Calcola la larghezza della barra in base alla percentuale di tempo rimasto."""
    rapporto = remaining / duration
    larghezza = int(rapporto * bar_width)
    # Clamp del valore tra 0 e bar_width
    return max(0, min(larghezza, bar_width))

# ------------------------------------------------------------------ #
# FUNZIONI — Disegno                                                   #
# ------------------------------------------------------------------ #

def draw_timer_bar(surface: pygame.Surface,
                   remaining: float, duration: int):
    """Disegna lo sfondo della barra e il riempimento proporzionale."""
    # 1. Disegno lo sfondo (rosso scuro)
    sfondo_rect = pygame.Rect(BAR_X, BAR_Y, BAR_W, BAR_H)
    pygame.draw.rect(surface, BAR_BG_COLOR, sfondo_rect, border_radius=6)
    
    # 2. Disegno il riempimento (verde)
    larghezza_piena = bar_fill_width(remaining, duration, BAR_W)
    riempimento_rect = pygame.Rect(BAR_X, BAR_Y, larghezza_piena, BAR_H)
    pygame.draw.rect(surface, BAR_FG_COLOR, riempimento_rect, border_radius=6)


def draw_timer_text(surface: pygame.Surface,
                    remaining: float, expired: bool, font_large, font_medium):
    """Mostra il countdown numerico o il messaggio di chiusura."""
    y_pos = BAR_Y + BAR_H + 10
    
    if expired:
        testo = "Tempo scaduto!"
        surf = font_large.render(testo, True, TEXT_COLOR)
    else:
        #Arrotondo per eccesso per mostrare "10" appena parte e non "9"
        testo = str(math.ceil(remaining))
        surf = font_medium.render(testo, True, TEXT_COLOR)
    
    #Centratura orizzontale
    rect = surf.get_rect(centerx=SCREEN_W // 2, top=y_pos)
    surface.blit(surf, rect)


def draw_ball(surface: pygame.Surface,
              x: int, y: int, expired: bool):
    """Disegna la pallina cambiando colore se il tempo è finito."""
    colore = BALL_EXPIRED if expired else BALL_COLOR
    pygame.draw.circle(surface, colore, (x, y), BALL_RADIUS)

# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                     #
# ------------------------------------------------------------------ #

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Timer con Pygame")
    
    #Font
    font_large = pygame.font.SysFont(None, 48)
    font_medium = pygame.font.SysFont(None, 36)
    
    #Timer
    start_time = time.time()
    duration = 10  # secondi
    
    #Pallina
    ball_x = SCREEN_W // 2
    ball_y = SCREEN_H // 2 + 100
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #Calcoli del timer
        remaining = time_remaining(start_time, duration)
        expired = is_expired(start_time, duration)
        
        #Disegno
        screen.fill((0, 0, 0))
        
        draw_timer_bar(screen, remaining, duration)
        draw_timer_text(screen, remaining, expired, font_large, font_medium)
        draw_ball(screen, ball_x, ball_y, expired)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()