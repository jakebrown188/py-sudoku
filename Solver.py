import math
from tabulate import tabulate


class Solver:
    def __init__(self, board):
        self.board = board

        # Character used in the 2D board array to represent a blank cell
        self.blank_character = "-"

    def solve(self):
        pass

    def find_duplicates(self):
        duplicates = {
            "boxes": {},
            "rows": {},
            "columns": {}
        }

        for element_number in range(0,8+1):
            box_duplicates = self.test_box(element_number)
            row_duplicates = self.test_row(element_number)
            column_duplicates = self.test_column(element_number)

            if len(box_duplicates) > 0:
                duplicates["boxes"][element_number] = box_duplicates
            if len(row_duplicates) > 0:
                duplicates["rows"][element_number] = row_duplicates
            if len(column_duplicates) > 0:
                duplicates["columns"][element_number] = column_duplicates

        return duplicates

    def test_box(self, box_number):
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

    def test_row(self, row_number):
        return self.find_duplicates_in_list(self.board.get_board_rows(row_number))

    def test_column(self, column_number):
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