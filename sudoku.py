import copy


class SudokuSolver:

    def __init__(self, board_matrix):
        self.board_matrix = board_matrix
        self._possibilities_dictionary = {}
        self._current_guess_list = []

    def all_check(self, row_number, column_number):
        """Checks whether a given row/column position on the sudoku board is forced. If it is forced, it updates the
        board. If not, it updates the dictionary of possible values for that square."""
        possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for row_index in range(9):
            possibilities.discard(self.board_matrix[row_index][column_number])
        for column_index in range(9):
            possibilities.discard(self.board_matrix[row_number][column_index])
        for block_column_index in range(3 * (column_number // 3), 3 * (column_number//3) + 3):
            for block_row_index in range(3 * (row_number // 3), 3 * (row_number//3) + 3):
                possibilities.discard(self.board_matrix[block_row_index][block_column_index])
        if len(possibilities) == 1:
            self.board_matrix[row_number][column_number] = list(possibilities)[0]
            self._possibilities_dictionary.pop((row_number, column_number), None)
        else:
            self._possibilities_dictionary[(row_number, column_number)] = possibilities

    def row_check(self, row_number):
        """Checks to see if any values in a particular row have only one possible space. If so, updates the sudoku
        board. """
        for possible_value in range(1, 10):
            location_list = []
            for column_index in range(9):
                if self.board_matrix[row_number][column_index] == 0 \
                        and possible_value in self._possibilities_dictionary[(row_number, column_index)]:
                    location_list.append((row_number, column_index))
            if len(location_list) == 1:
                self.board_matrix[location_list[0][0]][location_list[0][1]] = possible_value
                self._possibilities_dictionary.pop((location_list[0][0], location_list[0][1]), None)

    def column_check(self, column_number):
        """Checks to see if any values in a particular row have only one possible space. If so, updates the sudoku
        board."""
        for possible_value in range(1, 10):
            location_list = []
            for row_index in range(9):
                if self.board_matrix[row_index][column_number] == 0 \
                        and possible_value in self._possibilities_dictionary[(row_index, column_number)]:
                    location_list.append((row_index, column_number))
            if len(location_list) == 1:
                self.board_matrix[location_list[0][0]][location_list[0][1]] = possible_value
                self._possibilities_dictionary.pop((location_list[0][0], location_list[0][1]), None)

    def block_check(self, block_row_number, block_column_number):
        """Checks to see if any values in a particular block can only be assigned to one space. If so, updatesthe sudoku
        board."""
        for possible_value in range(1, 10):
            location_list = []
            for row_index in range(3 * block_row_number, 3 * block_row_number + 3):
                for column_index in range(3 * block_column_number, 3 * block_column_number + 3):
                    if self.board_matrix[row_index][column_index] == 0 \
                            and possible_value in self._possibilities_dictionary[(row_index, column_index)]:
                        location_list.append((row_index, column_index))
            if len(location_list) == 1:
                self.board_matrix[location_list[0][0]][location_list[0][1]] = possible_value
                self._possibilities_dictionary.pop((location_list[0][0], location_list[0][1]), None)

    def guess(self):
        minimum_possibilities = 9
        minimum_index = (0, 0)
        for row_index in range(9):
            for column_index in range(9):
                if self.board_matrix[row_index][column_index] == 0:
                    if len(self._possibilities_dictionary[(row_index, column_index)]) < minimum_possibilities:
                        minimum_possibilities = len(self._possibilities_dictionary[(row_index, column_index)])
                        minimum_index = (row_index, column_index)
        guess = min(self._possibilities_dictionary[minimum_index])  # Choose the guess to be the lowest element in set
        self._possibilities_dictionary[minimum_index].remove(guess)  # Remove the guess from the set
        self._current_guess_list.append((minimum_index, self._possibilities_dictionary.pop(minimum_index),
                                        copy.deepcopy(self.board_matrix)))  # Move the set to the guess list.
        self.board_matrix[minimum_index[0]][minimum_index[1]] = guess

    def empty_set(self):
        if self._current_guess_list[-1][1] != set():
            return
        else:
            self._current_guess_list[-1:] = []
            self.empty_set()

    def back_step(self):
        for row_index in range(9):
            for column_index in range(9):
                if self.board_matrix[row_index][column_index] == 0:
                    if self._possibilities_dictionary[(row_index, column_index)] == set():  # catch an error
                        if self._current_guess_list[-1][1] == set():
                            self.empty_set()
                        self.board_matrix = self._current_guess_list[-1][2]  # rollback the board
                        self.board_matrix[self._current_guess_list[-1][0][0]][self._current_guess_list[-1][0][1]] \
                            = min(self._current_guess_list[-1][1])  # choose next highest value as new guess
                        self._current_guess_list[-1][1].remove(min(self._current_guess_list[-1][1]))
                        return

    def print_board(self):
        """Prints out the board state."""
        for i in range(len(self.board_matrix)):
            string = ""
            for j in range(len(self.board_matrix)):
                string += str(self.board_matrix[i][j])
            print(string)


def main(sudoku_board):
    sudoku = SudokuSolver(sudoku_board)
    not_done = [0 in row for row in sudoku.board_matrix]
    while True in not_done:
        current_board = copy.deepcopy(sudoku.board_matrix)
        for row_index in range(9):
            for column_index in range(9):
                if sudoku.board_matrix[row_index][column_index] == 0:
                    sudoku.all_check(row_index, column_index)
        if current_board == sudoku.board_matrix:
            for row_index in range(9):
                sudoku.row_check(row_index)
        if current_board == sudoku.board_matrix:
            for column_index in range(9):
                sudoku.column_check(column_index)
        if current_board == sudoku.board_matrix:
            for block_row_index in range(3):
                for block_column_index in range(3):
                    sudoku.block_check(block_row_index, block_column_index)
        not_done = [0 in row for row in sudoku.board_matrix]
        if current_board == sudoku.board_matrix and True in not_done:
            sudoku.back_step()
        if current_board == sudoku.board_matrix and True in not_done:
            sudoku.guess()
    sudoku.print_board()
