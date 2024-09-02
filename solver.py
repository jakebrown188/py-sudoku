import copy
from typing import Dict, Set, List

from tabulate import tabulate

from board import Board


class Solver:
    """
    Class used to solve the Sudoku puzzle
    """

    DuplicateDataStructure = Dict[str, Dict[int, Set]]

    def __init__(self, board: Board) -> None:
        """
        Initialize the Solver object with a given board
        :param board: Board to solve
        """
        self.board_object = board
        self.board_array = self.board_object.get_board()

        # Character used in the 2D board array to represent a blank cell
        self.blank_character = "-"
        self.valid_sudoku_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # Create scratch space for possible guesses
        self.scratch_space = {}

    def solve(self) -> None:
        """
        Solve the puzzle and print puzzle if solved
        :return: None
        """
        is_solved = self.check_solve()
        count = 0

        while not is_solved:
            if count > 10000:
                print("Could not find solution")
                exit(1)

            self.generate_candidates()
            self.implement_candidates()
            self.reset_scratch_space()

            is_solved = self.check_solve()

            count += 1

        self.board_object.print_board()
        print()
        print("SOLVED")
        print(f"Took {count} rounds")


    def check_solve(self) -> bool:
        """
        Check if the puzzle is a valid solution. To be solved, it must meet these conditions:
            - There are no empty cells
            - There are no duplicates in each box, row, and column
            - All rows, boxes, and columns contain every number in self.valid_sudoku_options
        :return: True if puzzle is solved, False otherwise
        """
        duplicates = self.find_duplicates()
        found_duplicates = self.check_duplicates(duplicates)
        found_blank_cells = self.find_blank_cells()

        if not found_duplicates and not found_blank_cells:
            return True
        else:
            return False

    @staticmethod
    def check_duplicates(duplicates: DuplicateDataStructure) -> bool:
        """
        Loop through the duplicates data structure and find any keys that contain elements.
        :param duplicates: Duplicate data structure to check
        :return: True if duplicates are found, False otherwise
        """
        for element in ["boxes", "rows", "columns"]:
            if len(duplicates[element]) > 0:
                return True

        return False

    def find_blank_cells(self) -> bool:
        """
        Loop through every cell of the board array and see if it contains any blank characters
        :return: True if blanks cells are found, False otherwise
        """
        for row in self.board_array:
            if self.blank_character in row:
                return True

        return False

    def find_duplicates(self) -> DuplicateDataStructure:
        """
        Check each box, row, and column for duplicates. Return the duplicates found
        :return: Duplicates found for each box, row, and column
        """
        duplicates = {
            "boxes": {},
            "rows": {},
            "columns": {}
        }

        for element_number in range(0,8+1):
            box_duplicates = self.find_box_duplicates(element_number)
            row_duplicates = self.find_row_duplicates(element_number)
            column_duplicates = self.find_column_duplicates(element_number)

            if len(box_duplicates) > 0:
                duplicates["boxes"][element_number] = box_duplicates
            if len(row_duplicates) > 0:
                duplicates["rows"][element_number] = row_duplicates
            if len(column_duplicates) > 0:
                duplicates["columns"][element_number] = column_duplicates

        return duplicates

    def find_box_duplicates(self, box_number: int) -> Set:
        """
        For a given box number, find any duplicates and return them if found
        :param box_number: Box number to check
        :return: Duplicates found
        """
        box = self.board_object.extract_box_from_box_number(box_number)

        flattened_box = self.board_object.flatten_box(box)
        return self.find_duplicates_in_list(flattened_box)

    def find_row_duplicates(self, row_number: int) -> Set:
        """
        For a given row number, find any duplicates and return them if found
        :param row_number: Row number to check
        :return: Duplicates found
        """
        return self.find_duplicates_in_list(self.board_object.get_board_rows(row_number))

    def find_column_duplicates(self, column_number: int) -> Set:
        """
        For a given column number, find any duplicates and return them if found
        :param column_number: Column number to check
        :return: Duplicates found
        """
        vertical_line = []

        for line in self.board_array:
            vertical_line.append(line[column_number])

        return self.find_duplicates_in_list(vertical_line)


    def find_duplicates_in_list(self, input_list: List) -> Set:
        """
        Find any duplicates in the given list excluding any duplicates of the blank character
        :param input_list: List to check for duplicates from
        :return: Duplicates found
        """
        duplicates = set()

        for element in input_list:
            if element != self.blank_character and input_list.count(element) > 1:
                duplicates.add(element)

        return duplicates

    def store_guess_in_scratch_space(self, row: int, column: int, guess: int) -> None:
        """
        Store a number in the scratch space given the coordinates that the guess relates to. Scratch space is used for
        storing potential candidates for each cell
        :param row: Row of the cell this guess relates to
        :param column: Column of the cell this guess relates to
        :param guess: Candidate for the cell coordinates given
        :return: None
        """
        if row > 8 or column > 8 or int(guess) > 9:
            print("The following are invalid options: row > 8, column > 8, guess > 9")
            exit(1)


        self.initialize_scratch_space(row, column)
        self.scratch_space[row][column].add(guess)

    def store_guesses_in_scratch_space(self, row_index: int, column_index: int, guesses: List) -> None:
        """
        Given a list of guesses, store all of them in the scratch space for the same cell coordinates
        :param row_index: Row of the cell these guesses relate to
        :param column_index: Column of the cell these guesses relate to
        :param guesses: Candidates for the cell coordinate given
        :return: None
        """
        for guess in guesses:
            self.store_guess_in_scratch_space(row_index, column_index, guess)

    def initialize_scratch_space(self, row: int, column: int) -> None:
        """
        Initialize the scratch space with the relevant data structures if they are not already present
        :param row: Row to initialize scratch space with
        :param column: Column to initialize scratch space with
        :return: None
        """
        if row not in self.scratch_space.keys():
            self.scratch_space[row] = {}

        if column not in self.scratch_space[row]:
            self.scratch_space[row][column] = set()

    def remove_guess_from_scratch_space(self, row_index: int, column_index: int, candidate: str) -> None:
        """
        Remove guess from scratch space
        :param row_index: Row of the cell to remove
        :param column_index: Column of the cell to remove
        :param candidate: Candidate to remove at the given cell coordinates
        :return: None
        """
        candidates = self.scratch_space[row_index][column_index]

        if len(candidates) == 1:
            self.scratch_space[row_index].pop(column_index)
        if len(candidates) > 1:
            self.scratch_space[row_index][column_index].remove(candidate)

    def reset_scratch_space(self) -> None:
        """
        Reset the scratch space class variable by overwriting it with an empty dictionary
        :return: None
        """
        self.scratch_space = {}

    def get_guess_options_from_scratch_space(self, row: int, column: int) -> Set:
        """
        Get the set of possible candidates at the given coordinates
        :param row: Row related to the stored cell candidates
        :param column: Column related to the stored cell candidates
        :return: Candidates
        """
        return self.scratch_space[row][column]

    def implement_candidates(self) -> None:
        """
        Take the candidates in the scratch space and implement them into the board where only one candidate for a
        given cell exists
        :return: None
        """
        scratch_space_copy = copy.deepcopy(self.scratch_space)
        for row_index in scratch_space_copy.keys():
            for column_index in scratch_space_copy[row_index]:
                candidates = scratch_space_copy[row_index][column_index]
                if len(candidates) == 1:
                    candidate = str(list(candidates)[0])
                    self.board_object.insert_number_into_board(row_index, column_index, candidate)
                    self.remove_guess_from_scratch_space(row_index, column_index, candidate)

    def generate_candidates(self) -> None:
        """
        Loop through every cell of the board and generate all valid candidates for each
        :return: None
        """
        board = self.board_array
        for row_index in range(len(board)):
            for column_index in range(len(board[row_index])):
                cell_value = board[row_index][column_index]

                if cell_value == self.blank_character:
                    guesses = self.generate_candidate(row_index, column_index)
                    self.store_guesses_in_scratch_space(row_index, column_index, guesses)

    def generate_candidate(self, row_index: int, column_index: int) -> List:
        """
        For a given cell, generate all box, row, and column valid candidates and return them
        :param row_index: Row of the cell to generate candidates for
        :param column_index: Column of the cell to generate candidates for
        :return: List of valid candidates for the given cell
        """
        # get row options
        row = self.board_array[row_index]
        row_guesses = self.find_sudoku_diff(row)
        row_guesses.sort()

        # get column options
        column = self.board_object.get_board_columns(column_index)
        column_guesses = self.find_sudoku_diff(column)
        column_guesses.sort()

        # get box guesses
        box = self.board_object.extract_box_from_cell_coordinates(row_index, column_index)
        box = self.board_object.flatten_box(box)
        box_guesses = self.find_sudoku_diff(box)
        box_guesses.sort()

        return list(set(row_guesses) & set(column_guesses) & set(box_guesses))


    def find_sudoku_diff(self, input_list: List) -> List:
        """
        Return list of valid options given an input list representing a box, row, or column
        :param input_list: List representing the values already present in a box, row, or column
        :return: List of valid options
        """
        return list(set(self.valid_sudoku_options) - set(input_list))

    @staticmethod
    def print_duplicates(duplicates: DuplicateDataStructure) -> None:
        """
        Print duplicates found broken out into box, row, and column duplicates
        :param duplicates: Duplicates found for boxes, rows, and columns
        :return: None
        """
        for element in ["Boxes", "Rows", "Columns"]:
            print(f"Duplicates in {element}:")
            element_duplicates = []
            element_key_name = element.lower()
            for element_number in duplicates[element_key_name]:
                individual_element_duplicates = (str(duplicates[element_key_name][element_number])
                                                 .replace("\'", "")
                                                 .replace("{", "")
                                                 .replace("}", ""))
                element_number_duplicates = [element_number, individual_element_duplicates]
                element_duplicates.append(element_number_duplicates)

            plural_to_singular_lookup = {
                "Boxes": "Box",
                "Rows": "Row",
                "Columns": "Column"
            }

            element_header = f"{plural_to_singular_lookup[element]} Number"
            print(tabulate(element_duplicates, headers=[element_header, "Duplicates Found"], tablefmt="pretty"))
