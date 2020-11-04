import copy
piece_vals = {
    'Pawn': 1,
    'Knight': 3,
    'Bishop': 3,
    'Rook': 5,
    'Queen': 9,
    'King': 1000
}

#  for now at least, the AI is just always going to be black.
#  board state looks like BEFORE the player makes it's turn

def ai_move(board, depth):
    best_move = None
    best_move_piece = None
    best_score = -1000000
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != 0 and board[y][x].team == 'Black':
                moves = board[y][x].possible_moves(board, find_king(board, 'Black'))
                for move in moves:
                    temp_board = copy.deepcopy(board)
                    piece = temp_board[y][x]
                    piece.move(temp_board, move)
                    score = minimax(temp_board, depth, -100000, 100000, False)
                    if score > best_score:
                        best_score = score
                        best_move = move
                        best_move_piece = board[y][x]
    best_move_piece.move(board, best_move)


def minimax(board, depth, alpha, beta, max_player):
    if depth == 0 or checkamte(board):
        return evaluate_pos(board)

    if max_player:
        val = -100000
        children = get_children(board, 'Black')
        for child in children:
            val = max(val, minimax(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, val)
            if alpha >= beta:
                pass
        return val

    else:
        val = 100000
        children = get_children(board, 'White')
        for child in children:
            val = min(val, minimax(child, depth - 1, alpha, beta, True))
            beta = min(beta, val)
            if beta <= alpha:
                pass
        return val

def get_children(parent, team):
    print(team)
    children = []
    for y in range(len(parent)):
        for x in range(len(parent[0])):
            if parent[y][x] != 0 and parent[y][x].team == team:
                moves = parent[y][x].possible_moves(parent, find_king(parent, team))
                for move in moves:
                    new_board = copy.deepcopy(parent)
                    new_board[y][x].move(new_board, move)
                    children.append(new_board)
    return children

def evaluate_pos(board):
    score = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != 0:
                if board[y][x].team == 'Black':
                    score += piece_vals[board[y][x].name]
                else:
                    score -= piece_vals[board[y][x].name]
    return score

def find_king(board, team):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != 0 and board[y][x].name == 'King' and board[y][x].team == team:
                return board[y][x]

def checkamte(board):
    flags = {
        'White': False,
        'Black': False
    }
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != 0:
                if len(board[y][x].possible_moves(board, find_king(board, board[y][x].team))) > 0:
                    flags[board[y][x].team] = True
                    if flags['White'] == True and flags['Black'] == True:
                        return False
    return True


