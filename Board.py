import math


class Board:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

        self.board = None
        self.initialize_board(input_file_path)

    def initialize_board(self, input_file_path):
        board = []

        with open(input_file_path, 'r') as puzzle:
            for line in puzzle:
                line = line.strip()
                board.append(line.split(","))

        self.board = board

    def insert_number_into_board(self, row_number, column_number, number):
        if isinstance(number, int):
            number = str(number)

        row = self.board[row_number]
        row[column_number] = number

    def remove_number_from_board(self, row_number, column_number):
        row = self.board[row_number]
        row[column_number] = "-"

    def get_board_rows(self, start, finish=None):
        if finish is None:
            rows = self.board[start]
        else:
            rows = self.board[start:finish]

        return rows

    def get_board_column(self, column_index):
        column_data = []

        for row in self.board:
            column_data.append(row[column_index])

        return column_data

    def extract_box_from_box_number(self, box_number):
        """
        Boxes identified by number using the following pattern:
        0,1,2
        3,4,5
        6,7,8
        :param box_number: number used to identify what box to check
        :return: True if box contains no errors, false otherwise
        """
        starting_row = math.floor(box_number / 3) * 3
        starting_column = box_number % 3 * 3

        return self.get_box_array(starting_row, starting_column)

    def extract_box_from_cell_coordinates(self, row_index, column_index):
        if column_index % 3 != 0:
            column_index = column_index - (column_index % 3)

        if row_index % 3 != 0:
            row_index = row_index - (row_index % 3
                                     )
        return self.get_box_array(row_index, column_index)

    def get_box_array(self, starting_row, starting_column):
        box = []

        relevant_rows = self.get_board_rows(starting_row, starting_row + 3)
        for row in relevant_rows:
            box.append(row[starting_column:starting_column + 3])

        return box

    def get_board(self):
        return self.board

    def print_board(self):
        print("+-------+-------+-------+")
        line_count = 1

        for line in self.board:
            print("| ", end="")
            element_count = 1

            for number in line:
                number = number.replace("-", " ")
                print(f"{number} ", end="")
                if element_count % 3 == 0:
                    print("| ", end="")
                element_count += 1
            print()

            if line_count % 3 == 0:
                print("+-------+-------+-------+")
            line_count += 1

    @staticmethod
    def print_box(box):
        print("+-------+")
        for line in box:
            print("| ", end="")
            for element in line:
                element = element.replace("-", " ")
                print(f"{element} ", end="")
            print("|")
        print("+-------+")