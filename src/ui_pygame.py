#Interface vizual com pygame:

import json
import os
import pygame
import sys
from logic import new_game, move_left, move_right, move_up, move_down, spawn_tile, has_won,has_moves

pygame.init()

#Definindo as configurações:
WIDTH, HEIGHT = 500,600
TILE_SIZE = 110
GRID_POS = (WIDTH // 2 - 2 * TILE_SIZE, 150)  # centraliza a grade horizontalmente
FPS = 60

# Definindo as cores:
BG_COLLOR = (250, 240, 239)
EMPTY_COLLOR = (205,193,180)
FONT_COLLOR = (119,110,101)
TITLE_COLLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),}

#Definindo as fontes:
FONT = pygame.font.SysFont("arial",40)
SMALL_FONT = pygame.font.SysFont("arial",24)

#Definindo a Tela:
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - Pygame Edition")
clock = pygame.time.Clock()

def draw_grid(state):
    screen.fill(BG_COLLOR)
    now = pygame.time.get_ticks()
    grid = state["grid"]
    merged = state.get("merged_cells", [[ ] for _ in range(4)])
    merge_time = state.get("merge_time", 0)
    highlight = (now - merge_time) < 150  # duração do efeito em ms

    # TÍTULO
    title = FONT.render("2048", True, FONT_COLLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # SCORE
    score_text = SMALL_FONT.render(f"Score: {state['score']}", True, FONT_COLLOR)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 70))

    # GRID
    for i in range(4):
        for j in range(4):
            value = grid[i][j]
            x = GRID_POS[0] + j * TILE_SIZE
            y = GRID_POS[1] + i * TILE_SIZE

            color = TITLE_COLLORS.get(value, EMPTY_COLLOR)

            # aplica efeito visual se a célula foi fundida recentemente
            size_offset = 0
            if highlight and j in merged[i]:
                size_offset = 8  # incha o bloco

            pygame.draw.rect(
                screen,
                color,
                (
                    x - size_offset // 2,
                    y - size_offset // 2,
                    TILE_SIZE - 5 + size_offset,
                    TILE_SIZE - 5 + size_offset
                ),
                border_radius=6
            )

            if value > 0:
                text = FONT.render(str(value), True, FONT_COLLOR)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)




STATS_FILE = "stats.json"



def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"highscore": 0, "wins": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def show_start_screen(stats):
    waiting = True
    while waiting:
        screen.fill(BG_COLLOR)

        # Título
        title = FONT.render("2048", True, FONT_COLLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # Botão
        button_text = SMALL_FONT.render("JOGAR", True, (255, 255, 255))
        button_rect = pygame.Rect(WIDTH // 2 - 60, 200, 120, 50)
        pygame.draw.rect(screen, (119, 110, 101), button_rect, border_radius=10)
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                  button_rect.centery - button_text.get_height() // 2))

        # Estatísticas
        highscore = SMALL_FONT.render(f"Melhor Pontuação: {stats['highscore']}", True, FONT_COLLOR)
        wins = SMALL_FONT.render(f"Vitórias: {stats['wins']}", True, FONT_COLLOR)
        screen.blit(highscore, (WIDTH // 2 - highscore.get_width() // 2, 280))
        screen.blit(wins, (WIDTH // 2 - wins.get_width() // 2, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

def show_game_over_screen(score, stats):
    waiting = True
    while waiting:
        screen.fill(BG_COLLOR)

        # Título
        title = FONT.render("FIM DE JOGO", True, FONT_COLLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        # Pontuação final
        score_text = SMALL_FONT.render(f"Sua pontuação: {score}", True, FONT_COLLOR)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 120))

        # Melhor pontuação
        highscore = SMALL_FONT.render(f"Melhor pontuação: {stats['highscore']}", True, FONT_COLLOR)
        screen.blit(highscore, (WIDTH // 2 - highscore.get_width() // 2, 150))

        # Botões
        again_rect = pygame.Rect(WIDTH // 2 - 140, 230, 120, 50)
        quit_rect = pygame.Rect(WIDTH // 2 + 20, 230, 120, 50)

        pygame.draw.rect(screen, (119, 110, 101), again_rect, border_radius=8)
        pygame.draw.rect(screen, (119, 110, 101), quit_rect, border_radius=8)

        again_text = SMALL_FONT.render("Jogar de novo", True, (255, 255, 255))
        quit_text = SMALL_FONT.render("Sair", True, (255, 255, 255))

        screen.blit(again_text, (again_rect.centerx - again_text.get_width() // 2,
                                 again_rect.centery - again_text.get_height() // 2))
        screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                quit_rect.centery - quit_text.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if again_rect.collidepoint(event.pos):
                    waiting = False
                    return True  # Jogar de novo
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def show_victory_screen(score, stats):
    waiting = True
    while waiting:
        screen.fill(BG_COLLOR)

        # Título
        title = FONT.render("VOCÊ VENCEU! 🎉", True, FONT_COLLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        # Pontuação
        score_text = SMALL_FONT.render(f"Pontuação: {score}", True, FONT_COLLOR)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 120))

        highscore = SMALL_FONT.render(f"Melhor pontuação: {stats['highscore']}", True, FONT_COLLOR)
        screen.blit(highscore, (WIDTH // 2 - highscore.get_width() // 2, 150))

        # Botões
        continue_rect = pygame.Rect(WIDTH // 2 - 140, 230, 120, 50)
        restart_rect = pygame.Rect(WIDTH // 2 + 20, 230, 120, 50)

        pygame.draw.rect(screen, (119, 110, 101), continue_rect, border_radius=8)
        pygame.draw.rect(screen, (119, 110, 101), restart_rect, border_radius=8)

        continue_text = SMALL_FONT.render("Continuar", True, (255, 255, 255))
        restart_text = SMALL_FONT.render("Reiniciar", True, (255, 255, 255))

        screen.blit(continue_text, (continue_rect.centerx - continue_text.get_width() // 2,
                                    continue_rect.centery - continue_text.get_height() // 2))
        screen.blit(restart_text, (restart_rect.centerx - restart_text.get_width() // 2,
                                   restart_rect.centery - restart_text.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos):
                    return "continue"
                elif restart_rect.collidepoint(event.pos):
                    return "restart"



def main():
    stats = load_stats()
    show_start_screen(stats)

    state = new_game()
    running = True

    while running:
        clock.tick(FPS)
        draw_grid(state)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                moved = False

                if event.key == pygame.K_LEFT:
                    new_grid, gained, moved, merged_cells = move_left(state["grid"])
                elif event.key == pygame.K_RIGHT:
                    new_grid, gained, moved, merged_cells = move_right(state["grid"])
                elif event.key == pygame.K_UP:
                    new_grid, gained, moved, merged_cells = move_up(state["grid"])
                elif event.key == pygame.K_DOWN:
                    new_grid, gained, moved, merged_cells = move_down(state["grid"])
                else:
                    continue

                if moved:
                    state["grid"] = new_grid
                    state["score"] += gained
                    spawn_tile(state["grid"])

                    state["merged_cells"] = merged_cells
                    state["merge_time"] = pygame.time.get_ticks()

                    if has_won(state["grid"]) and not state.get("won"):
                        stats["wins"] += 1
                        save_stats(stats)
                        state["won"] = True  # evita que apareça de novo se continuar jogando

                        escolha = show_victory_screen(state["score"], stats)
                        if escolha == "restart":
                            state = new_game()
                            continue  # volta para o topo do loop


                    elif not has_moves(state["grid"]):
                        if state["score"] > stats["highscore"]:
                            stats["highscore"] = state["score"]
                        save_stats(stats)

                        jogar_novamente = show_game_over_screen(state["score"], stats)
                        if jogar_novamente:
                            state = new_game()
                        else:
                            running = False

    pygame.quit()
    sys.exit()






if __name__ == "__main__":
    main()
