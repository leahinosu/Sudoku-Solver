# Author: Leah In
# Last Updated: 10/6/24
# Description: an implementation of a 9x9 Sudoku puzzle.
#              The program prompts users to initiate auto solve a given sudoku puzzle
#              by using the backtracking algorithm. Or, users can select option to
#              solve the puzzle manually.


class Sudoku:
    """
    A class represents 9x9 Sudoku puzzle.

    Attributes:
        board: list. a 9x9 sudoku board
        board_init: list. a 9x9 sudoku board for marking hint numbers
        board_sub: list. contains 3x3 sub-board number.
        empty_cell: int. the number of empty cells on the board.
        sub: dict. containing the number of integers between 1 and 9 in each 3x3 sub-board.
        row: dict. containing the number of integers between 1 and 9 in each row.
        col: dict. containing the number of integers between 1 and 9 in each column.
        empty_cell_list: list. a list of tuples containing the coordinate and the sub-board number of empty cells.
            Used for solver.

    Methods:
        get_sub_board_num(row: int, col: int) -> int:
            Return the sub-board number of the given coordinate.
        add_to_dictionaries(row: int, col: int, num: int, sub: int) -> None:
            Add 1 to sub/row/col dictionaries.
        remove_from_dictionaries(row: int, col: int, num: int, sub: int) -> None:
            Subtract 1 from sub/row/col dictionaries.
        initialize_board(sudoku_board: list) -> None:
            Initialize the board with the given list.
        place_on_board(row: int, col: int, num: int) -> bool:
            Place the given number on the given coordinate.
            Return False, if one of the inputs is not valid. Otherwise, update the board and return True.
        is_valid(row: int, col: int, num: int) -> bool:
            Check if the number on the given coordinate does not violate any rules.
            Return True, if not. Otherwise, return False.
        verify_solution() -> bool:
            Check the solution of the sudoku.
            If solved, return True. Otherwise, return False.
        get_num_empty_cell() -> int:
            Return the number of empty cells on the board.
        draw_board() -> None:
            Print the board.
        solver_is_valid(row: int, col: int, num: int, sub: int) -> bool:
            Check if the given number on the given coordinate is valid.
            Return True, if so. Otherwise, return False.
        solver(index: int = 0) -> None:
            Solve Sudoku by using the backtracking method.
    """

    def __init__(self, sudoku_board: list):
        """
        Initialized Sudoku object.
        :param sudoku_board: a 9x9 sudoku board
        """
        self.board = [[''] * 9 for _ in range(9)]
        self.board_init = [[''] * 9 for _ in range(9)]
        self.board_sub = [[0, 1, 2],
                          [3, 4, 5],
                          [6, 7, 8]]
        self.empty_cell = 81
        self.sub = [{1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0} for _ in range(9)]
        self.row = [{1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0} for _ in range(9)]
        self.col = [{1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0} for _ in range(9)]

        self.empty_cell_list = []

        self.initialize_board(sudoku_board)

    def get_sub_board_num(self, row: int, col: int) -> int:
        """
        Return the sub-board number of the given coordinate.
        :param row: row number
        :param col: column number
        :return sub_num: 3x3 sub-board number
        """
        sub_row = int(row / 3)
        sub_col = int(col / 3)
        sub_num = self.board_sub[sub_row][sub_col]

        return sub_num

    def add_to_dictionaries(self, row: int, col: int, num: int, sub: int) -> None:
        """
        Add 1 to row/col/sub dictionaries.
        :param row: row number
        :param col: column number
        :param num: an integer between 1 and 9
        :param sub: sub-board number
        :return:
        """
        self.sub[sub][num] += 1
        self.row[row][num] += 1
        self.col[col][num] += 1

    def remove_from_dictionaries(self, row: int, col: int, num: int, sub: int) -> None:
        """
        Subtract 1 from row/col/sub dictionaries
        :param row: row number
        :param col: column number
        :param num: an integer between 1 and 9
        :param sub: sub-board number
        :return:
        """
        self.sub[sub][num] -= 1
        self.row[row][num] -= 1
        self.col[col][num] -= 1

    def initialize_board(self, sudoku_board: list) -> None:
        """
        Initialize Sudoku board with the given list.
        Update board_init, sub/row/col dictionaries, and empty_cell.
        Update empty_cell_list for solver.
        :param sudoku_board: a 9x9 sudoku board
        :return:
        """
        self.board = sudoku_board

        for row in range(9):
            for col in range(9):
                sub = self.get_sub_board_num(row, col)
                if self.board[row][col] != '':
                    num = int(self.board[row][col])
                    self.add_to_dictionaries(row, col, num, sub)
                    self.board_init[row][col] = 'i'
                    self.empty_cell -= 1
                else:
                    self.empty_cell_list.append((row, col, sub))

    def place_on_board(self, row: int, col: int, num: int) -> bool:
        """
        Place an integer between 1 and 9 on the given coordinate.
        Return True, if board has been updated successfully.
        Return False, if one of the inputs is not valid.
        :param row: row number
        :param col: column number
        :param num: an integer between 1 and 9
        :return: bool
        """
        # verify user's inputs
        if num < 1 or num > 9:
            print("Please enter an integer between 1 and 9.")
            return False

        row -= 1
        if row < 0 or row > 8:
            print("Please enter a valid row number between 1 and 9.")
            return False

        col -= 1
        if col < 0 or col > 8:
            print("Please enter a valid column number between 1 and 9.")
            return False

        if self.board_init[row][col] == 'i':
            print("You cannot replace a hint number.")
            return False

        # place the num
        sub = self.get_sub_board_num(row, col)

        if self.board[row][col] != '':
            # replace
            old_num = int(self.board[row][col])
            self.remove_from_dictionaries(row, col, old_num, sub)
        else:
            # fill an empty cell
            self.empty_cell -= 1

        self.add_to_dictionaries(row, col, num, sub)
        self.board[row][col] = str(num)

        return True

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Check if the number on the given coordinate does not violate any rules.
        Return True, if not. Otherwise, return False.e.
        :param row: row number
        :param col: column number
        :param num: an integer between 1 and 9
        :return: bool
        """
        # check sub-board
        sub = self.get_sub_board_num(row, col)
        if self.sub[sub][num] > 1:
            return False
        # check row
        if self.row[row][num] > 1:
            return False
        # check col
        if self.col[col][num] > 1:
            return False

        return True

    def verify_solution(self) -> bool:
        """
        Verify the user's solution.
        Return True, if the user solved the sudoku. Otherwise, return False.
        :return: bool
        """
        for row in range(9):
            for col in range(9):
                num = int(self.board[row][col])
                if not self.is_valid(row, col, num):
                    print("Not Solved. Try Again.")
                    return False
        print("Congratulation. You've solved the puzzle!")
        return True

    def get_num_empty_cell(self) -> int:
        """
        Return the number of empty cells on the board.
        :return: int
        """
        return self.empty_cell

    def draw_board(self) -> None:
        """
        Print the board.
        :return:
        """
        print(" " + "--" * 12 + "-")
        for row in range(9):
            text = " | "
            for col in range(9):
                if self.board[row][col] == "":
                    text += "  "
                else:
                    text += self.board[row][col] + " "
                if (col + 1) % 3 == 0:
                    text += "| "
            print(text)
            if (row + 1) % 3 == 0:
                print(" " + "--" * 12 + "-")

    # ====================
    # Solver
    # ====================

    def solver_is_valid(self, row: int, col: int, num: int, sub: int) -> bool:
        """
        Checking validation for solver.
        Return true, if valid. Otherwise, return False.
        :param row: row number
        :param col: column number
        :param num: an integer between 1 and 9
        :param sub: 3x3 sub-board number
        :return: bool
        """
        # check sub-board
        if self.sub[sub][num] == 1:
            return False
        # check row
        if self.row[row][num] == 1:
            return False
        # check col
        if self.col[col][num] == 1:
            return False

        return True

    def solver(self, index: int = 0) -> None:
        """
        Solve sudoku by using the backtracking method.
        :param index: index of the empty_cell_list. Default is 0.
        :return:
        """

        # base case
        if self.get_num_empty_cell() == 0:
            return

        # get an empty cell
        row, col, sub = self.empty_cell_list[index]

        # get a valid number
        for num in range(1, 10):
            if self.solver_is_valid(row, col, num, sub):
                self.board[row][col] = str(num)
                self.add_to_dictionaries(row, col, num, sub)
                self.empty_cell -= 1

                # checking the next empty spot. The for loop holds the last number tried.
                self.solver(index + 1)

                # check if the board is filled.
                if self.get_num_empty_cell() == 0:
                    return

                # backtracking
                self.board[row][col] = ''
                self.remove_from_dictionaries(row, col, num, sub)
                self.empty_cell += 1


if __name__ == '__main__':

    puzzle1 = [['', '9', '', '', '', '', '', '', ''],
              ['2', '1', '', '', '', '', '', '5', '7'],
              ['7', '5', '3', '2', '', '', '', '6', '1'],
              ['', '', '7', '', '9', '', '1', '3', '6'],
              ['', '', '', '8', '1', '', '', '7', ''],
              ['5', '', '', '', '2', '', '', '', '9'],
              ['', '', '', '4', '', '', '7', '', '3'],
              ['', '', '', '7', '', '6', '', '', ''],
              ['', '', '4', '', '8', '', '', '1', '']]

    solution1 = [['4', '9', '6', '1', '7', '5', '3', '2', '8'],
                ['2', '1', '8', '3', '6', '9', '4', '5', '7'],
                ['7', '5', '3', '2', '4', '8', '9', '6', '1'],
                ['8', '2', '7', '5', '9', '4', '1', '3', '6'],
                ['6', '4', '9', '8', '1', '3', '5', '7', '2'],
                ['5', '3', '1', '6', '2', '7', '8', '4', '9'],
                ['9', '6', '2', '4', '5', '1', '7', '8', '3'],
                ['1', '8', '5', '7', '3', '6', '2', '9', '4'],
                ['3', '7', '4', '9', '8', '2', '6', '1', '5']]  # solution to preset_1

    unsolvable1 = [['4', '3', '5', '2', '6', '9', '7', '8', '1'],
                ['6', '8', '2', '5', '7', '1', '4', '9', '3'],
                ['1', '9', '7', '8', '3', '4', '5', '6', '2'],
                ['8', '2', '6', '1', '9', '5', '3', '4', '7'],
                ['3', '7', '1', '6', '8', '2', '9', '1', '5'],
                ['9', '5', '1', '7', '4', '3', '6', '2', '8'],
                ['5', '1', '9', '3', '2', '6', '8', '7', '4'],
                ['2', '4', '8', '9', '5', '7', '1', '3', '6'],
                ['7', '6', '3', '4', '1', '8', '2', '5', '9']]  # not solved. column/row check failed

    unsolvable2 = [['4', '3', '5', '2', '6', '9', '7', '8', '1'],
                ['9', '5', '1', '7', '4', '3', '6', '2', '8'],
                ['6', '8', '2', '5', '7', '1', '4', '9', '3'],
                ['1', '9', '7', '8', '3', '4', '5', '6', '2'],
                ['8', '2', '6', '1', '9', '5', '3', '4', '7'],
                ['3', '7', '4', '6', '8', '2', '9', '1', '5'],
                ['5', '1', '9', '3', '2', '6', '8', '7', '4'],
                ['2', '4', '8', '9', '5', '7', '1', '3', '6'],
                ['7', '6', '3', '4', '1', '8', '2', '5', '9']]  # not solved. section check failed

    puzzle2 = [['4', '', '', '', '', '', '', '1', ''],
                ['', '1', '5', '', '4', '', '6', '', ''],
                ['', '', '', '', '', '7', '', '', ''],
                ['', '', '', '2', '1', '', '', '', '8'],
                ['', '', '', '7', '3', '4', '', '', '2'],
                ['', '3', '', '', '8', '', '', '', ''],
                ['8', '', '1', '9', '', '', '', '4', '5'],
                ['', '4', '', '', '', '', '7', '', ''],
                ['2', '', '', '', '', '3', '', '', '']]  # test for solver

    empty_list = [['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', '']]

    # add more presets below.

    # select the set
    print("There are 5 samples of sudoku presets.")
    print("1. puzzle 1")
    print("2. puzzle 2")
    print("3. unsolvable1 - a complete set")
    print("4. unsolvable2 - a complete set")
    print("5. solution1 - a complete set")
    preset = -1
    while not(0 < int(preset) < 6):
        preset = int(input("Please select a set from the list above: "))
        if not(0 < preset< 6):
            print("Please enter a number between 1 and 5.")
    
    preset_map = {
        1: puzzle1,
        2: puzzle2,
        3: unsolvable1,
        4: unsolvable2,
        5: solution1
    }
    puzzle = Sudoku(preset_map[preset])

    # start sudoku
    print("=" * 20)
    print("Puzzle #23: Sudoku")
    print("=" * 20)
    puzzle.draw_board()
    confirm = input("Run solver? (y/n): ")
    if confirm.lower() in ['y', 'yes']:
        puzzle.solver()
        puzzle.draw_board()
        puzzle.verify_solution()
    elif confirm.lower() in ['n', 'no']:
        while puzzle.get_num_empty_cell() != 0:
            user_input_is_valid = False
            while not user_input_is_valid:
                row = int(input("Enter row (1-9): "))
                col = int(input("Enter column (1-9): "))
                num = int(input("Enter number (1-9): "))
                user_input_is_valid = puzzle.place_on_board(row, col, num)
            puzzle.draw_board()
        puzzle.verify_solution()
    else:
        print("Good Bye.")
