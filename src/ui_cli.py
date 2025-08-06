#Centraliza os números em 5 colunas, espaços em branco para 0s

def draw_grid(grid,score):
    print("\n"+"="*25)
    print(f"SCORE: {score}")
    print("-"*25)
    for row in grid:
        line = "|".join(f"{num:^5}" if num > 0 else "     " for num in row)
        print(f"|{line}|")
        print("-"*25)

#Capturar imput

def get_input():
    while True:
        move = input("Move (W/A/S/D): ").strip().lower()
        if move in ["w","a","s","d"]:
            return move
        print("Invalid input. Use W (up), A (left), S (down), D (right).")
