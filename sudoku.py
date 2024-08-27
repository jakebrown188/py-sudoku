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


def main():
    # test_adding_and_removing_from_board(board)
    # test_for_duplicates_in_board()
    # test_for_solved_board()
    test_scratch_space()


if __name__ == '__main__':
    main()
