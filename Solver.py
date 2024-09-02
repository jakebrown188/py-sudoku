import copy
from tabulate import tabulate

from Board import Board


class Solver:
    def __init__(self, board: Board) -> None:
        self.board_object = board
        self.board_array = self.board_object.get_board()

        # Character used in the 2D board array to represent a blank cell
        self.blank_character = "-"
        self.valid_sudoku_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # Create scratch space for possible guesses
        self.scratch_space = {}

    def solve(self):
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


    def check_solve(self):
        duplicates = self.find_duplicates()
        found_duplicates = self.check_duplicates(duplicates)
        found_blank_cells = self.find_blank_cells()

        if not found_duplicates and not found_blank_cells:
            return True
        else:
            return False

    @staticmethod
    def check_duplicates(duplicates):
        for element in ["boxes", "rows", "columns"]:
            if len(duplicates[element]) > 0:
                return True

        return False

    def find_blank_cells(self):
        for row in self.board_array:
            if "-" in row:
                return True

        return False

    def find_duplicates(self):
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

    def find_box_duplicates(self, box_number):
        box = self.board_object.extract_box_from_box_number(box_number)

        flattened_box = self.board_object.flatten_box(box)
        return self.find_duplicates_in_list(flattened_box)

    def find_row_duplicates(self, row_number):
        return self.find_duplicates_in_list(self.board_object.get_board_rows(row_number))

    def find_column_duplicates(self, column_number):
        vertical_line = []

        for line in self.board_array:
            vertical_line.append(line[column_number])

        return self.find_duplicates_in_list(vertical_line)


    def find_duplicates_in_list(self, input_list):
        duplicates = set()

        for element in input_list:
            if element != self.blank_character and input_list.count(element) > 1:
                duplicates.add(element)

        return duplicates

    def store_guess_in_scratch_space(self, row, column, guess):
        if not isinstance(row, int):
            row = int(row)
        if not isinstance(column, int):
            column = int(column)
        if not isinstance(guess, int):
            guess = int(guess)

        if row > 8 or column > 8 or guess > 9:
            print("The following are invalid options: row > 8, column > 8, guess > 9")
            exit(1)


        self.initialize_scratch_space(row, column)
        self.scratch_space[row][column].add(guess)

    def store_guesses_in_scratch_space(self, row_index, column_index, guesses):
        for guess in guesses:
            self.store_guess_in_scratch_space(row_index, column_index, guess)

    def initialize_scratch_space(self, row, column):
        if row not in self.scratch_space.keys():
            self.scratch_space[row] = {}

        if column not in self.scratch_space[row]:
            self.scratch_space[row][column] = set()

    def remove_guess_from_scratch_space(self, row_index, column_index, candidate):
        candidates = self.scratch_space[row_index][column_index]

        if len(candidates) == 1:
            self.scratch_space[row_index].pop(column_index)
        if len(candidates) > 1:
            self.scratch_space[row_index][column_index].remove(candidate)

    def reset_scratch_space(self):
        self.scratch_space = {}

    def get_guess_options_from_scratch_space(self, row, column):
        return self.scratch_space[row][column]

    def implement_candidates(self):
        scratch_space_copy = copy.deepcopy(self.scratch_space)
        for row_index in scratch_space_copy.keys():
            for column_index in scratch_space_copy[row_index]:
                candidates = scratch_space_copy[row_index][column_index]
                if len(candidates) == 1:
                    candidate = str(list(candidates)[0])
                    self.board_object.insert_number_into_board(row_index, column_index, candidate)
                    self.remove_guess_from_scratch_space(row_index, column_index, candidate)

    def generate_candidates(self):
        board = self.board_array
        for row_index in range(len(board)):
            for column_index in range(len(board[row_index])):
                cell_value = board[row_index][column_index]

                if cell_value == self.blank_character:
                    guesses = self.generate_candidate(row_index, column_index)
                    self.store_guesses_in_scratch_space(row_index, column_index, guesses)

    def generate_candidate(self, row_index, column_index):
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


    def find_sudoku_diff(self, input_list):
        return list(set(self.valid_sudoku_options) - set(input_list))

    def print_duplicates(self, duplicates):
        for element in ["Boxes", "Rows", "Columns"]:
            self.print_element_duplicates(duplicates, element)
            print()

    @staticmethod
    def print_element_duplicates(duplicates, element_name):
        print(f"Duplicates in {element_name}:")
        element_duplicates = []
        element_key_name = element_name.lower()
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

        element_header = f"{plural_to_singular_lookup[element_name]} Number"
        print(tabulate(element_duplicates, headers=[element_header, "Duplicates Found"], tablefmt="pretty"))
