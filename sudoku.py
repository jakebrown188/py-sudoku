import json

from Board import Board
from Solver import Solver


def test_adding_and_removing_from_board():
    board = Board("puzzles/puzzle1-beginner.txt")
    print("Original:")
    board.print_board()
    print()

    print("Adding 5")
    board.insert_number_into_board(1, 0, 5)
    board.print_board()
    print()

    print("Removing 5")
    board.remove_number_from_board(1, 0)
    board.print_board()


def test_for_duplicates_in_board():
    board = Board("puzzles/puzzle1-beginner-dupes.txt")
    solver = Solver(board)
    duplicates = solver.find_duplicates()
    solver.print_duplicates(duplicates)


def test_for_solved_board():
    board = Board("puzzles/puzzle1-beginner.txt")
    solver = Solver(board)
    is_solved = solver.check_solve()
    if is_solved:
        print("Board is solved!")
    else:
        print("Board is not solved")


def test_scratch_space():
    board = Board("puzzles/puzzle1-beginner.txt")
    solver = Solver(board)
    solver.store_guess_in_scratch_space(0, 6, 3)
    solver.store_guess_in_scratch_space(0, 6, 3)
    solver.store_guess_in_scratch_space(0, 6, 4)
    options = solver.get_guess_options_from_scratch_space(0, 6)
    print(options)


def test_sudoku_diff():
    board = Board("puzzles/puzzle1-beginner.txt")
    solver = Solver(board)
    solver.generate_candidates()

    input_list = ["3","-","7","-","-","-","9","6","-"]
    options = solver.find_sudoku_diff(input_list)
    print(options)


def test_get_board_row_and_column():
    board = Board("puzzles/puzzle1-beginner.txt")

    board.print_board()

    row_index = 0
    column_index = 0

    row = board.get_board_rows(row_index)
    column = board.get_board_columns(column_index)

    print(f"Row: {row}")
    print(f"Column: {column}")


def test_generate_guesses():
    board = Board("puzzles/puzzle2-check_candidates.txt")
    solver = Solver(board)
    solver.generate_candidates()
    print()


def test_get_box_number():
    board = Board("puzzles/puzzle1-beginner.txt")

    for row_index in range(0,8+1):
        for column_index in range(0,8+1):
            print(f"Starting -> Row: {row_index}, Column: {column_index}")
            board.extract_box_from_cell_coordinates(row_index, column_index)
            print()


def test_get_box_from_number():
    board = Board("puzzles/puzzle1-beginner.txt")

    board.print_board()

    for box_number in range(0, 8+1):
        box = board.extract_box_from_box_number(box_number)
        board.print_box(box)


def test_get_box_from_coordinates():
    board = Board("puzzles/puzzle1-beginner.txt")

    board.print_board()

    for row_index in range(0,8+1):
        for column_index in range(0,8+1):
            box = board.extract_box_from_cell_coordinates(row_index, column_index)
            print(f"Row: {row_index}, Column: {column_index}")
            board.print_box(box)
            print()


def test_implement_candidates():
    board = Board("puzzles/puzzle1-beginner.txt")
    solver = Solver(board)

    board.print_board()

    solver.generate_candidates()
    solver.implement_candidates()

    board.print_board()


def test_remove_candidate():
    board = Board("puzzles/puzzle1-beginner.txt")
    solver = Solver(board)
    solver.generate_candidates()

    solver.remove_guess_from_scratch_space(0, 1, 5)
    solver.remove_guess_from_scratch_space(2, 0, 5)


def test_check_solve():
    board = Board("puzzles/puzzle1-beginner.txt")
    solver = Solver(board)

    solver.solve()


def test_get_board_column():
    board = Board("puzzles/puzzle1-beginner.txt")

    column = board.get_board_columns(0)
    columns = board.get_board_columns(0, 3)

    board.print_board()

    print()
    print(f"Column: {column}")
    print()
    print(f"Columns: {columns}")


def main():
    # test_adding_and_removing_from_board(board)
    # test_for_duplicates_in_board()
    # test_for_solved_board()
    # test_scratch_space()
    # test_sudoku_diff()
    # test_get_board_row_and_column()
    # test_generate_guesses()
    # test_get_box_number()
    # test_get_box_from_number()
    # test_get_box_from_coordinates()
    # test_implement_candidates()
    # test_remove_candidate()
    test_check_solve()

    # test_get_board_column()

    # board = Board("puzzles/puzzle1-beginner.txt")
    # solver = Solver(board)
    # solver.populate_guesses()


if __name__ == '__main__':
    main()
