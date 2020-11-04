from abc import ABC, abstractmethod
import copy

TEAM_WHITE = 'White'
TEAM_BLACK = 'Black'


# Abstract Piece template for all pieces
class Piece(ABC):
    def __init__(self, y_pos, x_pos, team, name):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.team = team
        self.name = name  # type of piece

    # returns a 2D array with 1's = possible move/capture, 2 = current spot
    # direct_call: boolean representing if it was called by the main module or by the eliminate moves function
    @abstractmethod
    def possible_moves(self, board, king):
        pass

    # it's illegal to make a move that puts your king in danger. We must check if any piece on the opposing team
    # could capture the king if the move were made. Putting this inside of possible_moves causes infinite recursion.
    def eliminate_moves(self, board, moves_array, king):
        all_moves_array = copy.copy(moves_array)
        for move in all_moves_array:
            board2 = copy.deepcopy(board)  # we don't want to alter the real board so we make a copy
            piece = board2[self.y_pos][self.x_pos]
            piece.move(board2, move)
            for y2 in range(len(board2)):
                for x2 in range(len(board2[0])):
                    if board2[y2][x2] != 0 and board2[y2][x2].team != self.team:
                        if self.name == king.name:
                            if (piece.y_pos, piece.x_pos) in board2[y2][x2].possible_moves(board2, None):
                                moves_array.remove(move)
                        elif (king.y_pos, king.x_pos) in board2[y2][x2].possible_moves(board2, None):
                            moves_array.remove(move)
        return moves_array

    def move(self, board, move):
        new_y = move[0]
        new_x = move[1]
        board[self.y_pos][self.x_pos] = 0
        board[new_y][new_x] = self
        self.y_pos, self.x_pos = new_y, new_x

    # returns first letter of the piece name. Uppercase for white, lowercase for black
    def __repr__(self):
        if self.team == TEAM_WHITE:
            return self.name[0].upper()
        return self.name[0].lower()


class Pawn(Piece):
    def __init__(self, y_pos, x_pos, team):
        super().__init__(y_pos, x_pos, team, 'Pawn')
        self.first_move = True  # Needed variable since pawns can move two spaces on their first move.

    def possible_moves(self, board, king):
        moves_array = []
        if self.team == TEAM_WHITE and self.y_pos > 0:
            for x in range(len(board[0])):
                if board[self.y_pos-1][x] != 0 and x - self.x_pos in [-1, 1]:
                    if board[self.y_pos-1][x].team != self.team:
                        moves_array.append((self.y_pos-1, x))
            if board[self.y_pos-1][self.x_pos] == 0:
                moves_array.append((self.y_pos-1, self.x_pos))
                if self.y_pos > 1 and board[self.y_pos-2][self.x_pos] == 0 and self.first_move:
                    moves_array.append((self.y_pos-2, self.x_pos))
        elif self.team == TEAM_BLACK and self.y_pos < len(board):
            for x in range(len(board[0])):
                if board[self.y_pos+1][x] != 0 and x - self.x_pos in [-1, 1]:
                    if board[self.y_pos+1][x].team != self.team:
                        moves_array.append((self.y_pos+1, x))
            if board[self.y_pos+1][self.x_pos] == 0:
                moves_array.append((self.y_pos+1, self.x_pos))
                if self.y_pos < len(board) - 1 and board[self.y_pos+2][self.x_pos] == 0 and self.first_move:
                    moves_array.append((self.y_pos+2, self.x_pos))
        if king is not None:
            return self.eliminate_moves(board, moves_array, king)
        return moves_array

    # method overridden to set first_move to false.
    def move(self, board, move):
        super().move(board, move)
        self.first_move = False


class Rook(Piece):
    def __init__(self, y_pos, x_pos, team):
        super().__init__(y_pos, x_pos, team, 'Rook')

    def possible_moves(self, board, king):
        moves_array = []
        x = self.x_pos - 1
        while x >= 0 and board[self.y_pos][x] == 0:  # from self to left
            moves_array.append((self.y_pos, x))
            x -= 1
        if x >= 0 and board[self.y_pos][x].team != self.team:
            moves_array.insert(0, (self.y_pos, x))
        x = self.x_pos + 1
        while x < len(board[0]) and board[self.y_pos][x] == 0:  # from self to right
            moves_array.append((self.y_pos, x))
            x += 1
        if x < len(board[0]) and board[self.y_pos][x].team != self.team:
            moves_array.insert(0, (self.y_pos, x))
        y = self.y_pos - 1
        while y >= 0 and board[y][self.x_pos] == 0:  # from self to top
            moves_array.append((y, self.x_pos))
            y -= 1
        if y >= 0 and board[y][self.x_pos].team != self.team:
            moves_array.insert(0, (y, self.x_pos))
        y = self.y_pos + 1
        while y < len(board) and board[y][self.x_pos] == 0:  # from self to bottom
            moves_array.append((y, self.x_pos))
            y += 1
        if y < len(board) and board[y][self.x_pos].team != self.team:
            moves_array.insert(0, (y, self.x_pos))
        if king is not None:
            return self.eliminate_moves(board, moves_array, king)
        return moves_array


class Knight(Piece):
    def __init__(self, y_pos, x_pos, team):
        super().__init__(y_pos, x_pos, team, 'Knight')

    def possible_moves(self, board, king):
        moves_array = []
        offsets = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2)]
        for y in range(len(board)):
            for x in range(len(board[y])):
                if (self.y_pos - y, self.x_pos - x) in offsets:
                    if board[y][x] == 0:
                        moves_array.append((y, x))
                    elif board[y][x].team != self.team:
                        moves_array.insert(0, (y, x))
        if king is not None:
            return self.eliminate_moves(board, moves_array, king)
        return moves_array

    # method overridden to use 'n' instead of 'k', to not be confused with king.
    def __repr__(self):
        if self.team == TEAM_WHITE:
            return self.name[1].upper()
        return self.name[1]


class Bishop(Piece):
    def __init__(self, y_pos, x_pos, team):
        super().__init__(y_pos, x_pos, team, 'Bishop')

    def possible_moves(self, board, king):
        moves_array = []
        y, x = self.y_pos - 1, self.x_pos - 1
        while y >= 0 and x >= 0 and board[y][x] == 0:  # from self to top left
            moves_array.append((y, x))
            y, x = y - 1, x - 1
        if y >= 0 and x >= 0 and board[y][x].team != self.team:
            moves_array.insert(0, (y, x))
        y, x = self.y_pos - 1, self.x_pos + 1
        while y >= 0 and x < len(board[0]) and board[y][x] == 0:  # from self to top right
            moves_array.append((y, x))
            y, x = y - 1, x + 1
        if y >= 0 and x < len(board[0]) and board[y][x].team != self.team:
            moves_array.insert(0, (y, x))
        y, x = self.y_pos + 1, self.x_pos - 1
        while y < len(board) and x >= 0 and board[y][x] == 0:  # from self to bottom left
            moves_array.append((y, x))
            y, x = y + 1, x - 1
        if y < len(board) and x >= 0 and board[y][x].team != self.team:
            moves_array.insert(0, (y, x))
        y, x = self.y_pos + 1, self.x_pos + 1
        while y < len(board) and x < len(board[0]) and board[y][x] == 0:  # from self to bottom right
            moves_array.append((y, x))
            y, x = y + 1, x + 1
        if y < len(board) and x < len(board[0]) and board[y][x].team != self.team:
            moves_array.insert(0, (y, x))
        if king is not None:
            return self.eliminate_moves(board, moves_array, king)
        return moves_array


class Queen(Piece):
    def __init__(self, y_pos, x_pos, team):
        super().__init__(y_pos, x_pos, team, 'Queen')

    def possible_moves(self, board, king):
        moves_array = []
        rook_moves = Rook(self.y_pos, self.x_pos, self.team).possible_moves(board, None)
        bishop_moves = Bishop(self.y_pos, self.x_pos, self.team).possible_moves(board, None)
        length = max(len(rook_moves), len(bishop_moves))
        for move_index in range(length):
            if move_index < len(rook_moves):
                moves_array.append(rook_moves[move_index])
            if move_index < len(bishop_moves):
                moves_array.append(bishop_moves[move_index])
        if king is not None:
            return self.eliminate_moves(board, moves_array, king)
        return moves_array


class King(Piece):
    def __init__(self, y_pos, x_pos, team):
        super().__init__(y_pos, x_pos, team, 'King')

    def possible_moves(self, board, king):
        moves_array = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if y - self.y_pos in [-1, 0, 1] and x - self.x_pos in [-1, 0, 1]:
                    if board[y][x] == 0:
                        moves_array.append((y, x))
                    elif board[y][x].team != self.team:
                        moves_array.insert(0, (y, x))
        if king is not None:
            return self.eliminate_moves(board, moves_array, king)
        return moves_array
