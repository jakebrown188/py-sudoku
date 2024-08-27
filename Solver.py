import math
from tabulate import tabulate


class Solver:
    def __init__(self, board):
        self.board = board

        # Character used in the 2D board array to represent a blank cell
        self.blank_character = "-"

        # Create scratch space for possible guesses
        self.scratch_space = {}

    def solve(self):
        pass

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
        for row in self.board.get_board():
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
        """
        Boxes identified by number using the following pattern:
        0,1,2
        3,4,5
        6,7,8
        :param box_number: number used to identify what box to check
        :return: True if box contains no errors, false otherwise
        """
        box = self.extract_box(box_number)

        flattened_box = sum(box, [])
        return self.find_duplicates_in_list(flattened_box)

    def find_row_duplicates(self, row_number):
        return self.find_duplicates_in_list(self.board.get_board_rows(row_number))

    def find_column_duplicates(self, column_number):
        vertical_line = []

        for line in self.board.get_board():
            vertical_line.append(line[column_number])

        return self.find_duplicates_in_list(vertical_line)

    def extract_box(self, box_number):
        starting_row = math.floor(box_number / 3) * 3
        starting_column = box_number % 3 * 3

        box = []
        relevant_rows = self.board.get_board_rows(starting_row, starting_row + 3)
        for row in relevant_rows:
            box.append(row[starting_column:starting_column + 3])

        return box

    def find_duplicates_in_list(self, input_list):
        duplicates = set()

        for element in input_list:
            if element != self.blank_character and input_list.count(element) > 1:
                duplicates.add(element)

        return duplicates

    def store_guess_in_scratch_space(self, row, column, guess):
        if row > 8 or column > 8 or guess > 9:
            print("The following are invalid options: row > 8, column > 8, guess > 9")
            exit(1)

        self.initialize_scratch_space(row, column)
        self.scratch_space[row][column].add(guess)

    def initialize_scratch_space(self, row, column):
        if row not in self.scratch_space.keys():
            self.scratch_space[row] = {}

        if column not in self.scratch_space[row]:
            self.scratch_space[row][column] = set()

    def get_guess_options_from_scratch_space(self, row, column):
        return self.scratch_space[row][column]

    def check_candidates(self, row, column):
        # Loop through every cell of the board
        

        # Find what box the cell is in

        # Check box, row, and column for options
        pass

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
