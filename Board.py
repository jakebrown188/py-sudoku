import math
from typing import List, Union


class Board:
    """
    Class used to represent and interact with the Sudoku puzzle board
    """
    TwoDBoard = List[List[str]]
    Box = TwoDBoard

    def __init__(self, input_file_path: str) -> None:
        """
        Initialize the Board object by loading the puzzle at the file name specified
        :param input_file_path: Path to the file with the board text
        """
        self.input_file_path = input_file_path

        self.board = None
        self.initialize_board(input_file_path)

    def initialize_board(self, input_file_path: str) -> None:
        """
        Set the board class variable using the data in the file path specified
        :param input_file_path: Path to the file with the board text
        :return: None
        """
        board = []

        with open(input_file_path, 'r') as puzzle:
            for line in puzzle:
                line = line.strip()
                board.append(line.split(","))

        self.board = board

    def insert_number_into_board(self, row_number: int, column_number: int, number: str) -> None:
        """
        Insert a number into the class board variable at the given coordinates
        :param row_number: Row to insert the number into
        :param column_number: Column to insert the number into
        :param number: Number to insert into the board
        :return: None
        """
        if not isinstance(number, str):
            raise ValueError("number must be a string")

        row = self.get_board_rows(row_number)
        row[column_number] = number

    def remove_number_from_board(self, row_number: int, column_number: int) -> None:
        """
        Remove the number from the class board variable at the given coordinates
        :param row_number: Row to remove number from
        :param column_number: Column to remove number from
        :return: None
        """
        row = self.get_board_rows(row_number)
        row[column_number] = "-"

    def get_board_rows(self, row_start: int, row_end: int = None) -> Union[List[str], TwoDBoard]:
        """
        Return a range of rows from the class board variable. If no ending row is specified, return a singular row
        :param row_start: Starting row to include in range. If no ending row given, only row to include in return
        :param row_end: Ending row to include in range (exclusive). Optional
        :return: Singular row if no ending row provided, otherwise range of rows
        """
        if row_end is None:
            rows = self.board[row_start]
        else:
            rows = self.board[row_start:row_end]

        return rows

    def get_board_columns(self, column_start: int, column_end: int = None) -> Union[List[str], TwoDBoard]:
        """
        Return a range of columns from the class board variable. If no ending column is specified, return a
        singular column
        :param column_start: Starting column to include in range. If no ending column given, only column to
         include in return
        :param column_end: Ending column to include in range (exclusive). Optional
        :return: Singular column if no ending column provided, otherwise range of columns
        """

        if column_end is None:
            columns = self._extract_column_from_board(column_start)
        else:
            columns = []
            for column_index in range(column_start, column_end):
                columns.append(self._extract_column_from_board(column_index))

        return columns

    def _extract_column_from_board(self, column_index: int) -> List[str]:
        """
        Helper function used to extract one column out of the board
        :param column_index: Index of the column to extract
        :return: Column data at the index specified
        """
        column_data = []

        for row in self.board:
            column_data.append(row[column_index])

        return column_data

    def extract_box_from_box_number(self, box_number: int) -> Box:
        """
        Extract the box 2D array data from the class board variable using a box number.
        General logic is to identify the top-left coordinate of each box and return the box starting at that coordinate.
        Boxes are identified by number using the following pattern:
        0,1,2
        3,4,5
        6,7,8
        :param box_number: Number used to identify what box to check
        :return: Box data corresponding to the number given
        """
        starting_row = math.floor(box_number / 3) * 3
        starting_column = box_number % 3 * 3

        return self.get_box_array(starting_row, starting_column)

    def extract_box_from_cell_coordinates(self, row_index: int, column_index: int) -> Box:
        """
        Extract the box 2D array data from the class board variable using a coordinate of any cell in the board.
        General logic is to calculate what the top-left corner of the box would be and return the box starting at
        that coordinate
        :param row_index: Row of the cell to extract the box from
        :param column_index: Column of the cell to extract the box from
        :return: Box data corresponding to the cell coordinates given
        """
        if column_index % 3 != 0:
            column_index = column_index - (column_index % 3)

        if row_index % 3 != 0:
            row_index = row_index - (row_index % 3)

        return self.get_box_array(row_index, column_index)

    def get_box_array(self, starting_row: int, starting_column: int) -> Box:
        """
        Get the box 2D array given the coordinate of the top-left cell of the box
        :param starting_row: Row of the cell representing the top-left cell of the box
        :param starting_column: Column of the cell representing the top-left cell of the box
        :return: Box data corresponding to the top-left cell coordinates given
        """
        box = []

        relevant_rows = self.get_board_rows(starting_row, starting_row + 3)
        for row in relevant_rows:
            columns = row[starting_column:starting_column + 3]
            box.append(columns)

        return box

    @staticmethod
    def flatten_box(box: Box) -> List[str]:
        """
        Take in a 2D array and flatten it to a 1D array
        :param box: Box data to flatten
        :return: Flattened box
        """
        return sum(box, [])

    def get_board(self) -> TwoDBoard:
        """
        Return the 2D board array
        :return: 2D array representing the board
        """
        return self.board

    def print_board(self) -> None:
        """
        Print the 2D board object
        :return: None
        """
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
    def print_box(box: Box) -> None:
        """
        Print the given box
        :param box: Box to print
        :return: None
        """
        print("+-------+")
        for line in box:
            print("| ", end="")
            for element in line:
                element = element.replace("-", " ")
                print(f"{element} ", end="")
            print("|")
        print("+-------+")