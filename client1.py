import pygame
import sys
import numpy as np
import socket
import time
import ssl

pygame.init()

# global variables
row_size = 6
column_size = 7
board = np.zeros((row_size, column_size))
np.flip(board, 0)
game = "True"
turn = 0
row_count = [0, 0, 0, 0, 0, 0, 0]
win = 0
size = 100
height = int((row_size + 1) * size)
width = int(column_size * size)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# creating the screen of the game
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Client")
pygame.draw.rect(screen, blue, (0, size, width, (row_size * size)))
for i in range(row_size):
    for j in range(column_size):
        pygame.draw.circle(screen, black, (int((j * size) + size / 2), int(size + size / 2 + (i * size))), int(size / 2 - 5))
pygame.display.update()


# checking for the validity of the move
def validity(col):
    row = row_count[col]
    if (row < row_size):
        if (board[row][col] == 0):
            return True
    return False


# putting the repective player's pieces in their positions
def put_turn_client1(col):
    plr = (turn % 2) + 1
    board[row_count[col], col] = plr
    pygame.draw.circle(screen, red, (int((col) * size + size / 2), int((5 - row_count[col]) * size + size + size / 2)), int(size / 2 - 5))
    pygame.display.update()
    row_count[col] += 1


def put_turn_client2(col):
    plr = (turn % 2) + 1
    board[row_count[col], col] = plr
    pygame.draw.circle(screen, yellow, (int((col) * size + size / 2), int((5 - row_count[col]) * size + size + size / 2)), int(size / 2 - 5))
    pygame.display.update()
    row_count[col] += 1


# checking win condition
def win_cond():
    plr = (turn % 2) + 1
    # horizontal check
    for i in range(row_size):
        for j in range(column_size - 3):
            if (board[i][j] == plr and board[i][j + 1] == plr and board[i][j + 2] == plr and board[i][j + 3] == plr):
                return 1

    # vertical check
    for i in range(row_size - 3):
        for j in range(column_size):
            if (board[i][j] == plr and board[i + 1][j] == plr and board[i + 2][j] == plr and board[i + 3][j] == plr):
                return 1

    # positive diagonal(slope) check
    for i in range(row_size - 3):
        for j in range(column_size - 3):
            if (board[i][j] == plr and board[i + 1][j + 1] == plr and board[i + 2][j + 2] == plr and board[i + 3][j + 3] == plr):
                return 1

    # negative diagonal(slope) check
    for i in range(row_size - 3):
        for j in range(3, column_size):
            if (board[i][j] == plr and board[i + 1][j - 1] == plr and board[i + 2][j - 2] == plr and board[i + 3][j - 3] == plr):
                return 1

    return 0


def create_socket_thread():
    global s1
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('./server_cert.pem')
    Host = "192.168.0.108"
    Port = 12321
    ssl_client = ssl_context.wrap_socket(s1, server_hostname=Host)
    ssl_client.connect((Host, Port))

    return ssl_client


ssl_client1 = create_socket_thread()

# the game
while (game == "True" or game == "true"):
    if (turn % 2 == 1):
        data = int(ssl_client1.recv(2048).decode())
        put_turn_client2(data)
        win = win_cond()
        if (win == 1):
            print("Opponent Won!")
            time.sleep(2)
            ssl_client1.close()
            sys.exit()
        turn += 1
    else:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                ssl_client1.close()
                sys.exit()
            if (event.type == pygame.MOUSEMOTION):
                poss = event.pos[0]
                pygame.draw.rect(screen, black, (0, 0, width, size))
                pygame.draw.circle(screen, red, (poss, int(size / 2)), int(size / 2 - 5))
                pygame.display.update()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                col = event.pos[0]
                col = int(np.floor(col / size))
                if (validity(col)):
                    data = str(col)
                    ssl_client1.sendall(data.encode())
                    put_turn_client1(col)
                    win = win_cond()
                else:
                    col = event.pos[0]
                    col = int(np.floor(col / size))
                    put_turn_client1(col)
                    win = win_cond()
                if (win == 1):
                    print("You Won!")
                    time.sleep(2)
                    ssl_client1.close()
                    sys.exit()

                turn += 1
