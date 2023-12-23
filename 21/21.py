import numpy as np

def parse_input(iname:str):
    with open(iname, 'r') as f:
        lines = f.readlines()

    nb_lines = len(lines)
    nb_cols = len(lines[0]) - 1 #-1 because of \n
    rocks = set()
    for i, line in enumerate(lines):
        rocks.update([i+k*1j for k, char in enumerate(line) if char == '#'])
        if line.find('S') != -1:
            start_pos = i + line.find('S')*1j
    return nb_lines, nb_cols, rocks, start_pos


def update_positions(nb_lines:int,nb_cols:int, rocks:set[complex], positions:set[complex], check_bounds=True):
    new_pos = set()
    for pos in positions:
        for direction in (1, -1, 1j, -1j):
            test_pos = pos + direction
            if check_bounds and (test_pos.real < 0 or test_pos.real >= nb_lines or test_pos.imag < 0 or test_pos.imag >= nb_cols):
                continue #Outside the canvas bounds
            if test_pos in rocks:
                continue #Forbidden position
            new_pos.add(test_pos)
    return new_pos

def get_number_positions(size:int, rocks:set[complex], starting_point:complex, nb_steps:int) -> int:
    current_positions = set()
    current_positions.add(starting_point)
    for i in range(nb_steps):
        current_positions = update_positions(size, size, rocks, current_positions, True)
    return len(current_positions)



def prob1():
    print("##########First part of the problem##########")
    nb_lines, nb_cols, rocks, start_pos = parse_input('input.1')
    current_positions = set()
    current_positions.add(start_pos)

    for i in range(64):
        current_positions = update_positions(nb_lines, nb_cols, rocks, current_positions)
    print(f"Number or reachable plots: {len(current_positions)}")



def prob2():
    print("##########Second part of the problem##########")
    nb_lines, nb_cols, rocks, start_pos = parse_input('input.1')

    assert(nb_cols == nb_lines) #Square grid
    size = nb_cols
    assert(size % 2 == 1) #Odd grid size
    assert(start_pos == size//2*(1+1j)) #Starting point in the middle
    nb_steps = 26501365
    assert(nb_steps%size == size//2) #We end up on the center of a repeated tile

    nb_grids_axis = nb_steps//size - 1
    nb_odd_grids = (nb_grids_axis - nb_grids_axis%2 + 1)**2
    nb_even_grids = (nb_grids_axis + nb_grids_axis%2)**2

    nb_odd_points = get_number_positions(size, rocks, start_pos, size)
    nb_even_points = get_number_positions(size, rocks, start_pos, size+1)

    nb_points_bot = get_number_positions(size, rocks, size - 1 + start_pos.imag*1j, size - 1)
    nb_points_top = get_number_positions(size, rocks, 0 + start_pos.imag*1j, size - 1)
    nb_points_right = get_number_positions(size, rocks, start_pos.real + (size - 1)*1j, size - 1)
    nb_points_left = get_number_positions(size, rocks, start_pos.real + (0)*1j, size - 1)

    nb_points_bottomleft = get_number_positions(size, rocks, size - 1 + 0*1j ,size//2 - 1)
    nb_points_topright = get_number_positions(size, rocks, 0 + (size - 1)*1j ,size//2 - 1)
    nb_points_topleft = get_number_positions(size, rocks, 0 + (0)*1j ,size//2 - 1)
    nb_points_bottomright = get_number_positions(size, rocks, size - 1 + (size - 1)*1j ,size//2 - 1)

    nb_points_bottomleft_large = get_number_positions(size, rocks, size - 1 + 0*1j ,(size*3)//2 - 1)
    nb_points_topright_large = get_number_positions(size, rocks, 0 + (size - 1)*1j ,(size*3)//2 - 1)
    nb_points_topleft_large = get_number_positions(size, rocks, 0 + (0)*1j ,(size*3)//2 - 1)
    nb_points_bottomright_large = get_number_positions(size, rocks, size - 1 + (size - 1)*1j ,(size*3)//2 - 1)

    nb_points = (
        nb_odd_points*nb_odd_grids +
        nb_even_points*nb_even_grids +
        nb_points_bot +
        nb_points_top +
        nb_points_left +
        nb_points_right +
        (nb_grids_axis + 1)*(nb_points_bottomleft + nb_points_topright + nb_points_topleft + nb_points_bottomright) +
        nb_grids_axis*(nb_points_bottomleft_large + nb_points_topright_large + nb_points_topleft_large + nb_points_bottomright_large)
    )

    print(f"Number or reachable plots: {nb_points}")

if __name__ == '__main__':
    prob1()
    prob2()
