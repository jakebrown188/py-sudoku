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


def main():
    # test_adding_and_removing_from_board(board)
    test_for_duplicates_in_board()


if __name__ == '__main__':
    main()
