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
        rows = None
        if finish is None:
            rows = self.board[start]
        else:
            rows = self.board[start:finish]

        return rows

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

    def print_box(self, box):
        print("+-------+")
        for line in box:
            print("| ", end="")
            for element in line:
                element = element.replace("-", " ")
                print(f"{element} ", end="")
            print("|")
        print("+-------+")