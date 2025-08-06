import random

#Fuction new game:
def new_game():
    grid = [[0] * 4 for _ in range(4)]
    score = 0

    #Insere inicialmente duas peças
    spawn_tile(grid)
    spawn_tile(grid)

    return {
        "grid": grid,
        "score": score,
        "won": False,
        "over": False
    }


#Insere um número 2 com 90% de chance ou um número 4 com 10% de chance em uma célula aleatória vazia.
def spawn_tile(grid):
    empty_cells = [(i,j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if not empty_cells:
        return
    
    i, j = random.choice(empty_cells)
    grid [i][j] = 4 if random.random() < 0.1 else 2

"""" Teste 1:
if __name__ == "__main__":
    state = new_game()
    for row in state["grid"]:
        print(row)
"""

#Defenindo a função quando apertado a seta para esquerda.
def merge_left(line):
    original = list(line)
    non_zero = [x for x in line if x != 0]
    merged = []
    score_gain = 0
    moved = False
    merged_indices = []

    i = 0
    while i < len(non_zero):
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            val = non_zero[i] * 2
            merged.append(val)
            score_gain += val
            merged_indices.append(len(merged) - 1)
            i += 2
        else:
            merged.append(non_zero[i])
            i += 1

    while len(merged) < 4:
        merged.append(0)

    if merged != original:
        moved = True

    return merged, score_gain, moved, merged_indices



""" Teste 2:
if __name__ == "__main__":
    tests = [
        [2, 0, 2, 2],
        [2, 2, 2, 2],
        [0, 0, 0, 0],
        [4, 4, 8, 8],
        [2, 2, 4, 4]
    ]
    for line in tests:
        merged, score, moved = merge_left(line)
        print(f"{line} -> {merged} | Score: {score} | Moved: {moved}")
"""

#Função que irá mover todas as linhas
def move_left(grid):
    new_grid = []
    gained = 0
    merged_cells = [[] for _ in range(4)]

    for i in range(4):
        row = [num for num in grid[i] if num != 0]
        new_row = []
        j = 0
        while j < len(row):
            if j + 1 < len(row) and row[j] == row[j + 1]:
                new_row.append(row[j] * 2)
                gained += row[j] * 2
                merged_cells[i].append(len(new_row) - 1)
                j += 2
            else:
                new_row.append(row[j])
                j += 1
        new_row += [0] * (4 - len(new_row))
        new_grid.append(new_row)

    return new_grid, gained, True if gained > 0 or new_grid != grid else False, merged_cells




""""
#Teste 3:
if __name__ == "__main__":
    grid = [
        [2, 0, 2, 2],
        [0, 0, 2, 2],
        [4, 4, 8, 0],
        [2, 2, 2, 2],
    ]
    new_grid, score, moved = move_left(grid)
    print("Before:")
    for row in grid:
        print(row)
    print("\nAfter:")
    for row in new_grid:
        print(row)
    print(f"Score gained: {score}")
    print(f"Moved? {moved}")
"""

# Para economizar código não vamos repetir a mesma lógica para as funções das outras direções
# Vamos colocar: Esquerda (Direto), Direita (inverter linha), Cima (transpor matriz) e Baixo (Transpor + Inverter)

#Funções utilitárias
def transpose(grid):
    return [list(row) for row in zip(*grid)]

def invert(grid):
    return [row[::-1] for row in grid]

#Movimentos:

#Seta para direita:
def move_right(grid):
    new_grid = []
    gained = 0
    merged_cells = [[] for _ in range(4)]

    for i in range(4):
        row = [num for num in grid[i] if num != 0]
        row.reverse()
        new_row = []
        j = 0
        while j < len(row):
            if j + 1 < len(row) and row[j] == row[j + 1]:
                new_row.append(row[j] * 2)
                gained += row[j] * 2
                merged_cells[i].append(3 - (len(new_row) - 1))  # posição original invertida
                j += 2
            else:
                new_row.append(row[j])
                j += 1
        new_row += [0] * (4 - len(new_row))
        new_row.reverse()
        new_grid.append(new_row)

    return new_grid, gained, True if gained > 0 or new_grid != grid else False, merged_cells



#Seta para cima
def move_up(grid):
    new_grid = [[0] * 4 for _ in range(4)]
    gained = 0
    merged_cells = [[] for _ in range(4)]

    for j in range(4):
        col = [grid[i][j] for i in range(4) if grid[i][j] != 0]
        new_col = []
        i = 0
        while i < len(col):
            if i + 1 < len(col) and col[i] == col[i + 1]:
                new_col.append(col[i] * 2)
                gained += col[i] * 2
                merged_cells[i].append(j)
                i += 2
            else:
                new_col.append(col[i])
                i += 1
        new_col += [0] * (4 - len(new_col))
        for i in range(4):
            new_grid[i][j] = new_col[i]

    return new_grid, gained, True if gained > 0 or new_grid != grid else False, merged_cells




#Seta para baixo:
def move_down(grid):
    new_grid = [[0] * 4 for _ in range(4)]
    gained = 0
    merged_cells = [[] for _ in range(4)]

    for j in range(4):
        col = [grid[i][j] for i in range(4) if grid[i][j] != 0]
        col.reverse()
        new_col = []
        i = 0
        while i < len(col):
            if i + 1 < len(col) and col[i] == col[i + 1]:
                new_col.append(col[i] * 2)
                gained += col[i] * 2
                merged_cells[3 - (len(new_col) - 1)].append(j)
                i += 2
            else:
                new_col.append(col[i])
                i += 1
        new_col += [0] * (4 - len(new_col))
        new_col.reverse()
        for i in range(4):
            new_grid[i][j] = new_col[i]

    return new_grid, gained, True if gained > 0 or new_grid != grid else False, merged_cells




""""
#Teste 4:
if __name__ == "__main__":
    from pprint import pprint

    grid = [
        [2, 2, 0, 0],
        [4, 0, 4, 0],
        [2, 2, 2, 2],
        [0, 0, 0, 0]
    ]

    directions = {
        "Left": move_left,
        "Right": move_right,
        "Up": move_up,
        "Down": move_down
    }

    for name, func in directions.items():
        print(f"\n{name}:")
        new_grid, score, moved = func(grid)
        pprint(new_grid)
        print(f"Score: {score} | Moved: {moved}")
"""

#Verificar se o jogador atingiu o bloco 2048.
def has_won(grid):
    return any(cell == 2048 for row in grid for cell in row)

#Verifica se ainda há movimentos possíveis.
def has_moves(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return True #Célula vazia
            if j < 3 and grid [i][j] == grid [i][j+1]:
                return True #par horizontal
            if i < 3 and grid[i][j] == grid[i+1][j]:
                return True #Par vertical
    return False
