#Criar loop do jogo

from logic import (new_game, spawn_title, move_left, move_right, move_up, move_down, has_won, has_moves
)

from ui_cli import draw_grid, get_input

def main():
    state = new_game()

    while True:
        draw_grid(state["grid"],state["score"])

        if state["won"]:
            print("🎉 You reached 2048! You Win")
            break

        if not has_moves(state["grid"]):
            print("💀 No more moves. Game Over.")
            break

        move = get_input()

        if move == "a":
            new_grid, gained, moved = move_left(state["grid"])
        elif move == "d":
            new_grid, gained, moved = move_right(state["grid"])
        elif move == "w":
            new_grid, gained, moved = move_up(state["grid"])
        elif move == "s":
            new_grid, gained, moved = move_down(state["grid"])
        
        if moved:
            state["grid"] = new_grid
            state["score"] += gained
            spawn_title(state["grid"])

            if has_won(state["grid"]):
                state["won"] = True

        else:
            print("❌ Invalid move (no change). Try again.")

if __name__ == "__main__":
    main()