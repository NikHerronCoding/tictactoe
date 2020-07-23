#  Hyperskill Python Developer Track
#  Project: Tic Tac Toe w/ AI
#  Stage: 5 (An undefeated champion)

import random
import copy
import operator


import pdb


class Board:
    player_commands = [ 'easy', 'medium','hard','user']
    actions = ['start', 'exit']
    two_in_a_row = {('X', 'X', ' '):2, ('X', ' ', 'X'):1, (' ', 'X', 'X'):0,
                    ('O', 'O', ' '):2, ('O', ' ', 'O'):1, (' ', 'O', 'O'):0}


    def __init__(self, input_board='_________'):
        self.board = self.generate_board(input_board)

    def __input_coordinates__(self, user_input, ele):
        if self.__is_occupied__(user_input):
            raise ValueError('Space is occupied already')
        else:
            self.board[user_input[0]][user_input[1]] = ele

    def __is_occupied__(self, user_input):
        # user_input = self.convert_coordinates(user_input)
        if self.board[user_input[0]][user_input[1]] in ['X', 'O']:
            return True
        else:
            return False

    def get_initial_state(self):
        user_input = input('Enter cells:')
        return user_input

    def generate_board(self, items):
        board = [[], [], []]
        for counter, symbol in enumerate(items):
            row = counter // 3
            if symbol == '_':
                board[row].append(' ')
            elif symbol == 'X':
                board[row].append('X')
            elif symbol == 'O':
                board[row].append('O')
        return board

    def print_board(self):
        print('---------')
        for row in self.board:
            print('| ', end='')
            for square in row:
                print(square + ' ', end='')
            print('|')
        print('---------')

    def whos_turn(self):
        x_counter = 0
        o_counter = 0
        for row in self.board:
            for square in row:
                if square == 'X':
                    x_counter += 1
                elif square == 'O':
                    o_counter += 1
        if x_counter == o_counter:
            return 'X'
        else:
            return 'O'

    def whos_not_turn(self):
        x_counter = 0
        o_counter = 0
        for row in self.board:
            for square in row:
                if square == 'X':
                    x_counter += 1
                elif square == 'O':
                    o_counter += 1
        if x_counter == o_counter:
            return 'O'
        else:
            return 'X'

    def enter_coordinates(self):
        while True:
            try:
                user_input = [int(num) for num in input('Enter the coordinates:').split(' ')]
                break
            except ValueError:
                print('You should enter numbers!')

        if len(user_input) != 2:
            raise ValueError('Only 2 numbers can be entered at a time')

        try:
            symbol = self.whos_turn()
            coordinates = self.convert_coordinates(user_input)
            for coordinate in coordinates:
                if coordinate not in [0, 1, 2]:
                    raise IndexError
            self.__input_coordinates__(coordinates, symbol)
            return True
        except IndexError:
            print('Coordinates should be from 1 to 3!')
        except ValueError:
            print('This cell is occupied! Choose another one!')
            self.enter_coordinates()
        return False

    def game_state(self):
        game_state_condition = [self.vertical_win(), self.horizontal_win(), self.diagonal_win()]

        if any(game_state_condition) and 'X' in game_state_condition:
            print('X wins')
        elif any(game_state_condition) and 'O' in game_state_condition:
            print('O wins')
        elif self.board_full():
            print('Draw')
        else:
            print('Game not finished')
    def return_game_state(self):
        game_state_condition = [self.vertical_win(), self.horizontal_win(), self.diagonal_win()]

        if any(game_state_condition) and 'X' in game_state_condition:
            return 'X'
        elif any(game_state_condition) and 'O' in game_state_condition:
            return 'O'
        elif self.board_full():
            return 'Draw'
        else:
            return False

    def game_over(self):
        game_state_condition = [self.vertical_win(), self.horizontal_win(), self.diagonal_win()]
        if game_state_condition == ['', '', ''] and not self.board_full():
            return False
        return True

    def board_full(self):
        for num in range(9):
            row = num // 3
            column = num % 3
            if self.board[row][column] == ' ':
                return False
        return True

    def board_empty(self):
        for num in range(9):
            row = num // 3
            column = num % 3
            if self.board[row][column] != ' ':
                return False
        return True


    def vertical_win(self):
        for num in range(3):
            column = []
            for col_num in range(3):
                column.append(self.board[col_num][num])
            if column == ['X', 'X', 'X']:
                return 'X'
            elif column == ['O', 'O', 'O']:
                return 'O'
        return ''

    def horizontal_win(self):
        for row in self.board:
            if row == ['X', 'X', 'X']:
                return 'X'
            elif row == ['O', 'O', 'O']:
                return 'O'
        return ''

    def diagonal_win(self):
        diagonal_1 = []
        diagonal_2 = []
        for num in range(3):
            diagonal_1.append(self.board[num][num])
            diagonal_2.append(self.board[num][2 - num])
        if diagonal_1 == ['X', 'X', 'X'] or diagonal_2 == ['X', 'X', 'X']:
            return 'X'
        elif diagonal_1 == ['O', 'O', 'O'] or diagonal_2 == ['O', 'O', 'O']:
            return 'O'
        else:
            return ''

    def convert_coordinates(self, input):
        return [3 - input[1], input[0] - 1]


    def coord_ok(self, value_1, value_2):
        convert_values = self.convert_coordinates([value_1, value_2])

        if self.board[convert_values[0]][convert_values[1]] != ' ':
            return False
        return True

    def valid_command(self, user_input):
        if user_input[0] == 'exit':
            exit()
        elif user_input == [] or user_input == '' or len(user_input) != 3:
            return []
        else:
            if user_input[0] not in Board.actions or user_input[1] not in Board.player_commands or user_input[2] not in Board.player_commands:
                    return []
            else:
                return user_input

    def ai_easy_choose(self):
        print('Making move level "easy"')
        self.ai_easy_random_choose()

    def ai_easy_random_choose(self):
        while True:
            value_1 = random.randint(1, 3)
            value_2 = random.randint(1, 3)
            if self.coord_ok(value_1, value_2):
                value_1, value_2 = self.convert_coordinates([value_1, value_2])[0], \
                                   self.convert_coordinates([value_1, value_2])[1]
                symbol = self.whos_turn()
                self.__input_coordinates__([value_1, value_2], symbol)
                break

    def ai_medium_choose(self):
        symbol = self.whos_turn()
        print('Making move level "medium"')
        if self.ai_medium_check_vertical():
            coordinates = self.ai_medium_check_vertical()
            self.board[coordinates[0]][coordinates[1]] = symbol
        elif self.ai_medium_check_horizontal():
            coordinates = self.ai_medium_check_horizontal()
            self.board[coordinates[0]][coordinates[1]] = symbol
        elif self.ai_medium_check_diagonal():
            coordinates = self.ai_medium_check_diagonal()
            self.board[coordinates[0]][coordinates[1]] = symbol
        else:
            self.ai_easy_random_choose()

    def ai_medium_check_column(self, col_num):
        column = []
        for num in range(3):
            column.append(self.board[num][col_num])
        if tuple(column) in Board.two_in_a_row:
            return Board.two_in_a_row[tuple(column)]
        else:
            return False

    def ai_medium_check_vertical(self):
        for num in range(3):
            if self.ai_medium_check_column(num):
                col_num = num
                row_num = self.ai_medium_check_column(num)
                return [row_num, col_num]
        return False

    def ai_medium_check_row(self, num):
        row = self.board[num]
        if tuple(row) in Board.two_in_a_row:
            return Board.two_in_a_row[tuple(row)]
        else:
            return False

    def ai_medium_check_horizontal(self):
        for num in range(3):
            if self.ai_medium_check_column(num):
                col_num = self.ai_medium_check_column(num)
                row_num = num
                return [row_num, col_num]
        return False

    def ai_medium_check_diagonal(self):
        diagonal_1 = []
        diagonal_2 = []
        for num in range(3):
            diagonal_1.append(self.board[num][num])
            diagonal_2.append(self.board[2 - num][num])

        if tuple(diagonal_1) in Board.two_in_a_row:
            row = Board.two_in_a_row[tuple(diagonal_1)]
            column = Board.two_in_a_row[tuple(diagonal_1)]
            return [row, column]
        elif tuple(diagonal_2) in Board.two_in_a_row:
            row = 2 - Board.two_in_a_row[tuple(diagonal_2)]
            column = Board.two_in_a_row[tuple(diagonal_2)]
            return [row, column]
        else:
            return False


class MiniMax(Board):

    def __init__(self, board, parent,maximum, minimum ):
        self.score = 0
        self.board = board
        self.parent = parent
        self.max = maximum
        self.min = minimum
        self.util = ''
        self.make_children()


    def make_children(self):
        self.children = []

        symbol = self.whos_turn()
        open_spaces = self.open_spaces()
        if not self.game_over():

            for open_space in open_spaces:
                child_board = copy.deepcopy(self.board)
                child_board[open_space[0]][open_space[1]] = symbol
                self.children.append(MiniMax(child_board.copy(), self, self.max, self.min))

    def minimax_algorithm(self):
        if self.terminal_state():
            self.util = self.utility()
            return self.utility()
        elif self.whos_turn() == self.max:
            points_dict = {}
            for child in self.children:
                points_dict[child] = child.minimax_algorithm()
            return max(points_dict.items(), key=operator.itemgetter(1))[1]
        else:
            points_dict = {}
            for child in self.children:
                points_dict[child] = child.minimax_algorithm()
            return min(points_dict.items(), key=operator.itemgetter(1))[1]

    def minimax_children(self):
        minimax_scores = []
        for child in self.children:
            minimax_scores.append(child.minimax_algorithm())
        return minimax_scores


    def utility(self):
        if self.return_game_state() == self.max:
            return 1
        elif self.return_game_state() == self.min:
            return -1
        elif self.return_game_state() == 'Draw':
            return 0



    def terminal_state(self):
        if self.return_game_state():
            return True
        else:
            return False

    def ai_hard_choose(self, board_object):
        max_value = max(self.minimax_children())
        for child in self.children:
            if child.minimax_algorithm() == max_value:
                chosen_child = child
                break
        coordinates = self.find_difference(chosen_child)
        board_object.board[coordinates[0]][coordinates[1]] = self.max

    def find_difference(self, comparator):
        for row_num in range(3):
            for col_num in range(3):
                if self.board[row_num][col_num] != comparator.board[row_num][col_num]:
                    return [row_num, col_num]

    def open_spaces(self):
        open_spaces_list = []
        for row in range(3):
            for column in range(3):
                if self.board[row][column] == ' ':
                    open_spaces_list.append([row, column])
        return open_spaces_list

    def whos_not_turn(self):
        x_counter = 0
        o_counter = 0
        for row in self.board:
            for square in row:
                if square == 'X':
                    x_counter += 1
                elif square == 'O':
                    o_counter += 1
        if x_counter == o_counter:
            return 'O'
        else:
            return 'X'


if __name__ == '__main__':
    board = Board()
    while True:
        user_input = input('Input command:').split(' ')
        commands = board.valid_command(user_input)
        if commands == []:
            print('Bad parameters!')
        else:
            player_matrix = commands[1:]
            round_counter = 0
            board = Board()
            board.print_board()
            while not board.game_over():
                if player_matrix[round_counter % 2] == 'easy':
                    board.ai_easy_choose()
                elif player_matrix[round_counter % 2] == 'medium':
                    board.ai_medium_choose()
                elif player_matrix[round_counter % 2] == 'hard':
                    if board.board_empty():
                        print('Making move level "hard"')
                        board.ai_easy_random_choose()
                    else:
                        minimax = MiniMax(board.board, 'root', board.whos_turn(), board.whos_not_turn())
                        print('Making move level "hard"')
                        minimax.ai_hard_choose(board)

                elif player_matrix[round_counter % 2] == 'user':
                    board.enter_coordinates()

                round_counter += 1
                board.print_board()
            board.game_state()
