import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import bfs
import astar


TIME_OUT = 1800

path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'

def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}\{file}"
            board = get_board(file_path)
            # print(file)
            list_boards.append(board)
    return list_boards


def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}\{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point

def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'


def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result


def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result


maps = get_boards()
check_points = get_check_points()



pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)

assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
found_background = pygame.image.load(os.getcwd() + '\\found_background.png')
'''
RENDER THE MAP FOR GAMEPLAY
'''
def renderMap(board):
	width = len(board[0])
	height = len(board)
	indent = (640 - width * 32) / 2.0
	for i in range(height):
		for j in range(width):
			screen.blit(space, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '#':
				screen.blit(wall, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '$':
				screen.blit(box, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '%':
				screen.blit(point, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '@':
				screen.blit(player, (j * 32 + indent, i * 32 + 250))

