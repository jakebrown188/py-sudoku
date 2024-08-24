import math


def print_board(board):
    print("+-------+-------+-------+")
    line_count = 1

    for line in board:
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


def print_box(box):
    print("+-------+")
    for line in box:
        print("| ", end="")
        for element in line:
            element = element.replace("-", " ")
            print(f"{element} ", end="")
        print("|")
    print("+-------+")


def read_board(file_path):
    board = []
    with open(file_path, 'r') as puzzle:
        for line in puzzle:
            line = line.strip()
            board.append(line.split(","))

    return board


def extract_box(box_number, board):
    starting_row = math.floor(box_number / 3) * 3
    starting_column = box_number % 3 * 3

    box = []
    relevant_rows = board[starting_row:starting_row + 3]
    for row in relevant_rows:
        box.append(row[starting_column:starting_column + 3])

    return box


def test_box(box_number, board):
    """
    Boxes identified by number using the following pattern:
    0,1,2
    3,4,5
    6,7,8
    :param box_number: number used to identify what box to check
    :param board: board to use
    :return: True if box contains no errors, false otherwise
    """
    box = extract_box(box_number, board)

    flattened_box = sum(box, [])
    dupes = set()

    for element in flattened_box:
        if element != "-" and flattened_box.count(element) > 1:
                dupes.add(element)

    return dupes


# def test_horizontal_line():
#     pass
#
#
# def test_vertical_line():
#     pass

def main():
    board = read_board("puzzles/puzzle1-beginner-dupes.txt")
    print_board(board)
    print()
    dupes = test_box(1, board)

    if len(dupes) > 0:
        print("Found dupes:")
        for dupe in dupes:
            print(f" - {dupe}")
    else:
        print("Zero dupes found")


if __name__ == '__main__':
    main()


# for num in range(0,9):
#     print(f"Box {num}:")
#     test_box(num, board)
#     print()