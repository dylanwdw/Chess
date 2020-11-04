from timeit import default_timer as timer
from pieces import *
from minimax import ai_move, minimax
import pygame

running = True

turn = TEAM_WHITE

BOARD_HEIGHT = 8
BOARD_WIDTH = 8
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
BOX_HEIGHT = 8
BOX_WIDTH = 8
BOX_SIZE = int(SCREEN_WIDTH / BOX_WIDTH)

LIGHT = (232, 235, 239)
DARK = (125, 135, 150)
GREEN = (144, 238, 144)
image_offset = 13
screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])
icons = {
    'P': pygame.image.load('Images/whitePawn.png'),
    'R': pygame.image.load('Images/whiteRook.png'),
    'N': pygame.image.load('Images/whiteKnight.png'),
    'B': pygame.image.load('Images/whiteBishop.png'),
    'Q': pygame.image.load('Images/whiteQueen.png'),
    'K': pygame.image.load('Images/whiteKing.png'),
    'p': pygame.image.load('Images/blackPawn.png'),
    'r': pygame.image.load('Images/blackRook.png'),
    'n': pygame.image.load('Images/blackKnight.png'),
    'b': pygame.image.load('Images/blackBishop.png'),
    'q': pygame.image.load('Images/blackQueen.png'),
    'k': pygame.image.load('Images/blackKing.png'),
}

title = "White's turn"

board = [[0 for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
white_pieces = [Rook(7, 0, TEAM_WHITE), Knight(7, 1, TEAM_WHITE), Bishop(7, 2, TEAM_WHITE),
                King(7, 4, TEAM_WHITE), Queen(7, 3, TEAM_WHITE), Bishop(7, 5, TEAM_WHITE),
                Knight(7, 6, TEAM_WHITE), Rook(7, 7, TEAM_WHITE)]
black_pieces = [Rook(0, 0, TEAM_BLACK), Knight(0, 1, TEAM_BLACK), Bishop(0, 2, TEAM_BLACK),
                King(0, 4, TEAM_BLACK), Queen(0, 3, TEAM_BLACK), Bishop(0, 5, TEAM_BLACK),
                Knight(0, 6, TEAM_BLACK), Rook(0, 7, TEAM_BLACK)]

for i in range(BOARD_WIDTH):  # Adding the pawns
    white_pieces.append(Pawn(6, i, TEAM_WHITE))
    black_pieces.append(Pawn(1, i, TEAM_BLACK))

# Adding the pieces to the board
for i in range(len(white_pieces)):
    board[white_pieces[i].y_pos][white_pieces[i].x_pos] = white_pieces[i]
    board[black_pieces[i].y_pos][black_pieces[i].x_pos] = black_pieces[i]


def get_king():  # returns the king from the array of pieces. Used to find possible moves of a piece.
    if turn == TEAM_WHITE:
        return white_pieces[3]
    return black_pieces[3]


def switch_turn():
    global turn
    global title
    if turn == TEAM_WHITE:
        turn = TEAM_BLACK
        title = "Black's turn"
    else:
        turn = TEAM_WHITE
        title = "White's turn"


def draw_background():
    for x_pos in range(BOX_HEIGHT):
        for y_pos in range(BOX_WIDTH):
            if (x_pos % 2 == 0 and y_pos % 2 == 0) or (x_pos % 2 != 0 and y_pos % 2 != 0):
                pygame.draw.rect(screen, LIGHT, (x_pos * BOX_SIZE, y_pos * BOX_SIZE, BOX_SIZE, BOX_SIZE))
            else:
                pygame.draw.rect(screen, DARK, (x_pos * BOX_SIZE, y_pos * BOX_SIZE, BOX_SIZE, BOX_SIZE))
    pygame.display.update()


def update_graphics(moves):
    draw_background()
    for y_pos in range(len(board)):
        for x_pos in range(len(board[0])):
            if board[y_pos][x_pos] != 0:
                screen.blit(icons[str(board[y_pos][x_pos])],
                            (x_pos * BOX_SIZE + image_offset, y_pos * BOX_SIZE + image_offset))
    # prints the green dots representing legal moves
    if moves is not None:
        for move in moves:
            if len(move) > 1:
                y_pos = move[0]
                x_pos = move[1]
                pygame.draw.circle(screen, GREEN, (int(x_pos * BOX_SIZE) + 45, int(y_pos * BOX_SIZE) + 45), 20)
    pygame.display.set_caption(title)
    pygame.display.update()


def checkmate():
    global title
    for y_pos in range(len(board)):
        for x_pos in range(len(board[0])):
            if board[y_pos][x_pos] != 0 and board[y_pos][x_pos].team == turn:
                legal_moves = board[y_pos][x_pos].possible_moves(board, get_king())
                if len(legal_moves) > 0:
                    return False
    title = "Checkmate,", turn, "wins"
    return True


update_graphics(None)  # board with pieces are initially shown with their starting positions
selected_piece = None
possible_moves = None
while running:
    if turn == TEAM_WHITE:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                x, y = int(x / BOX_SIZE), int(y / BOX_SIZE)
                if board[y][x] != 0 and board[y][x].team == turn:
                    selected_piece = board[y][x]
                    possible_moves = selected_piece.possible_moves(board, get_king())
                    update_graphics(possible_moves)
                elif selected_piece is not None and (y, x) in possible_moves:
                    selected_piece.move(board, (y, x))
                    switch_turn()
                    selected_piece = None
                    possible_moves = None
                    checkmate()
                    update_graphics([[0], [0]])
    elif turn == TEAM_BLACK:
        start_time = timer()
        ai_move(board, 1)
        #print(timer()-start_time)
        switch_turn()
        checkmate()
        update_graphics([[0], [0]])



