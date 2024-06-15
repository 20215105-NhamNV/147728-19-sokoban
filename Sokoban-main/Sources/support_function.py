from copy import deepcopy

TIME_OUT = 1800
list_check_point = []
list_death_point = []
class state:
    def __init__(self,board, state_parent):
        self.board = board
        self.state_parent = state_parent
        self.cost = 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)
    def get_line(self):
        if self.state_parent is None:
            return [re_format(self.board)]
        return (self.state_parent).get_line() +[re_format(self.board)]
    def get_line_(self):
        if self.state_parent is None:
            return [self.board]
        stage_parent = self.state_parent
        board = self.state_parent.board
        return (self.state_parent).get_line_()+ getLine(board , self.board)
    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic
    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        else:
            return False
    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        else :
            return False

def spfInit(board, list_check_point_):
    global list_check_point
    list_check_point = list_check_point_
    global list_death_point 
    list_death_point = find_death_points(board)   
    
def check_win(board):
    for p in list_check_point:
        if board[p[0]][p[1]] != '$':
            return False
    return True

def is_board_can_not_win(board):
    boxes = find_boxes_position(board)
    for b in boxes:
        if is_box_on_death_point(b): 
            return True
    if have_box_can_not_move(board, boxes):
        return True
    return False

def have_box_can_not_move(board,boxes):
    for b in boxes:
        if (is_box_on_check_point(b)):
            continue 
        x, y = b[0], b[1]
        u = board[x+1][y]
        d = board[x-1][y]
        l = board[x][y-1]
        r = board[x][y+1]
        ur = board[x+1][y+1]
        ul = board[x+1][y-1]
        dr = board[x-1][y+1]
        dl = board[x-1][y-1]
        if u == '#':
            if l == '$' and dl in ['#', '$']: return True
            if r == '$' and dr in ['#', '$']: return True
        if d == '#':
            if l == '$' and ul in ['#', '$']: return True
            if r == '$' and ur in ['#', '$']: return True
        if l == '#':
            if u == '$' and ur in ['#', '$']: return True
            if d == '$' and dr in ['#', '$']: return True
        if r == '#':
            if u == '$' and ul in ['#', '$']: return True
            if d == '$' and dl in ['#', '$']: return True
        if u in ['#', '$']:
            if l in ['#', '$'] and ul in ['#', '$']: return True
            if r in ['#', '$'] and ur in ['#', '$']: return True
        if d in ['#', '$']:
            if l in ['#', '$'] and dl in ['#', '$']: return True
            if r in ['#', '$'] and dr in ['#', '$']: return True
        if l in ['#', '$']:
            if u in ['#', '$'] and ul in ['#', '$']: return True
            if d in ['#', '$'] and dl in ['#', '$']: return True
        if r in ['#', '$']:
            if u in ['#', '$'] and ur in ['#', '$']: return True
            if d in ['#', '$'] and ul in ['#', '$']: return True
    return False

def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

def find_position_player(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '@':
                return (x,y)
    return (-1,-1)

def compare_matrix(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] == '@':
                if board_B[i][j] == '$':
                    return False
            if board_B[i][j] == '@':
                if board_A[i][j] == '$':
                    return False
            if board_A[i][j] != '@' and board_B[i][j] != '@':
                if board_A[i][j] != board_B[i][j]:
                    return False
    return True

def compare_matrix_(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True

def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False
def is_board_exist_(board, list_state):
    for state in list_state:
        if compare_matrix_(state.board, board):
            return True
    return False

def is_box_on_check_point(box):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False

def is_point_in_corner(board, x, y):
    if board[x-1][y] == '#' and board[x][y-1] == '#':
        if not is_box_on_check_point((x,y)):
            return True
    if board[x+1][y] == '#' and board[x][y-1] == '#':
        if not is_box_on_check_point((x,y)):
            return True
    if board[x-1][y] == '#' and board[x][y+1] == '#':
        if not is_box_on_check_point((x,y)):
            return True
    if board[x+1][y] == '#' and board[x][y+1] == '#':
        if not is_box_on_check_point((x,y)):
            return True
    return False

def is_death_point(board, x, y):
    if is_point_in_corner(board,x,y):
        return True
    check = True
    for z in range (len(board)):
        if is_box_on_check_point((z,y)):
            check = False
            break
    if check:
        for z in range (len(board)):
            if board[z][y-1] != '#':
                check = False
                break
        if check: return True
        check = True
        for z in range (len(board)):
            if board[z][y+1] != '#':
                check = False
                break
        if check: return True
    check = True
    for z in range (len(board[0])):
        if is_box_on_check_point((x,z)):
            check = False
            break
    if check:
        for z in range (len(board[0])):
            if board[x-1][z] != '#':
                check = False
                break
        if check: return True
        check = True
        for z in range (len(board[0])):
            if board[x+1][z] != '#':
                check = False
                break
        if check: return True
    return False

def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result.append((i,j))
    return result

def is_box_on_death_point(box):
    for p in list_death_point:
        if box[0] == p[0] and box[1] == p[1]:
            return True
    return False

def get_next_pos(board):
    cur_pos = find_position_player(board)
    x,y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # MOVE UP (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    # MOVE DOWN (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move

def move(board, next_pos, cur_pos):
    new_board = assign_matrix(board) 
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2*next_pos[0] - cur_pos[0]
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
        new_board[next_pos[0]][next_pos[1]] = '@'
        new_board[cur_pos[0]][cur_pos[1]] = '+'
        new_board = format(new_board)
        return new_board
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = '+'
    return new_board

def move_(board, i):
    new_board = assign_matrix(board)
    cur_pos = find_position_player(board)
    x, y = cur_pos[0], cur_pos[1]
    if i == 'w':
        if board[x-1][y] in [' ', '%']:
            new_board[x][y] = ' '
            new_board[x-1][y] = '@'
        if board[x-1][y] == '$':
            if not board[x-2][y] in ['#', "$"]:
                new_board[x][y] = ' '
                new_board[x-1][y] = '@'
                new_board[x-2][y] = '$'
    if i == 's':
        if board[x+1][y] in [' ', '%']:
            new_board[x][y] = ' '
            new_board[x+1][y] = '@'
        if board[x+1][y] == '$':
            if not board[x+2][y] in ['#', "$"]:
                new_board[x][y] = ' '
                new_board[x+1][y] = '@'
                new_board[x+2][y] = '$'
    if i == 'a':
        if board[x][y-1] in [' ', '%']:
            new_board[x][y] = ' '
            new_board[x][y-1] = '@'
        if board[x][y-1] == '$':
            if not board[x][y-2] in ['#', "$"]:
                new_board[x][y] = ' '
                new_board[x][y-1] = '@'
                new_board[x][y-2] = '$'
    if i == 'd':
        if board[x][y+1] in [' ', '%']:
            new_board[x][y] = ' '
            new_board[x][y+1] = '@'
        if board[x][y+1] == '$':
            if not board[x][y+2] in ['#', "$"]:
                new_board[x][y] = ' '
                new_board[x][y+1] = '@'
                new_board[x][y+2] = '$'
    return re_format(new_board)
def find_death_points(board):
    death_points = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] != '#':
                if is_death_point(board,x,y,):
                    death_points.append((x,y))
    return death_points

def format(board_) :
    board = assign_matrix(board_)
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '%' or board[x][y] == '+' or board[x][y] == ' ':
                board[x][y] = '-'
    cur_pos = find_position_player(board)
    list_can_move = [cur_pos]
    while len(list_can_move) != 0:
        cur_pos = list_can_move.pop(0)
        x ,y = cur_pos[0], cur_pos[1]
        if 0 <= x - 1 < len(board):
            if board[x - 1][y] == '-':
                board[x - 1][y] = ' '
                list_can_move.append((x - 1, y))
        if 0 <= x + 1 < len(board):
            if board[x + 1][y] == '-':
                board[x + 1][y] = ' '
                list_can_move.append((x + 1, y))
        if 0 <= y - 1 < len(board[0]):
            if board[x][y - 1] == '-':
                board[x][y - 1] = ' '
                list_can_move.append((x, y - 1))
        if 0 <= y + 1 < len(board[0]):
            if board[x][y + 1] == '-':
                board[x][y + 1] = ' '
                list_can_move.append((x, y + 1))
    return board

def re_format(board):
    for p in list_check_point:
        if board[p[0]][p[1]] != '$' and board[p[0]][p[1]] != '@' :
            board[p[0]][p[1]] = '%'
    return board

def get_next_boards(board):
    list_next_board = []
    boxes = find_boxes_position(board)
    cur_pos = find_position_player(board)
    for b in boxes:
        x ,y = b[0], b[1]
        # MOVE UP (x - 1, y)
        if 0 <= x + 1 < len(board) and 0 <= x - 1 < len(board):
            if board[x + 1][y] in [' ', '-', '@'] and board[x - 1][y] in [' ', '@']:
                new_board = assign_matrix(board)
                new_board[cur_pos[0]][cur_pos[1]] = ' '
                new_board = move(new_board, (x, y), (x-1, y))
                list_next_board.append(new_board)
        
        # MOVE DOWN (x + 1, y)
        if 0 <= x - 1 < len(board) and 0 <= x + 1 < len(board):
            if board[x - 1][y] in [' ', '-', '@'] and board[x + 1][y] in [' ', '@']:
                new_board = assign_matrix(board)
                new_board[cur_pos[0]][cur_pos[1]] = ' '
                new_board = move(new_board, (x, y), (x+1, y))
                list_next_board.append(new_board)
        
        # MOVE LEFT (x, y - 1)
        if 0 <= y + 1 < len(board[0]) and 0 <= y - 1 < len(board[0]):
            if board[x][y + 1] in [' ', '-', '@'] and board[x][y - 1] in [' ', '@']:
                new_board = assign_matrix(board)
                new_board[cur_pos[0]][cur_pos[1]] = ' '
                new_board = move(new_board, (x, y), (x, y-1))
                list_next_board.append(new_board)
        
        # MOVE RIGHT (x, y + 1)
        if 0 <= y - 1 < len(board[0]) and 0 <= y + 1 < len(board[0]):
            if board[x][y - 1] in [' ', '-', '@'] and board[x][y + 1] in [' ', '@']:
                new_board = assign_matrix(board)
                new_board[cur_pos[0]][cur_pos[1]] = ' '
                new_board = move(new_board, (x, y), (x, y+1))
                list_next_board.append(new_board)
                
    return list_next_board

def getLine(board_A , board_B):
    start_state = state(board_A,None)
    list_state = [start_state]
    list_visit = [start_state]
    
    while len(list_visit) != 0:
        now_state = list_visit.pop(0)
        now_board = now_state.board
        cur_pos = find_position_player(now_board)
        list_can_move = get_next_pos(now_board)
        for next_pos in list_can_move:
            if now_board[next_pos[0]][next_pos[1]] == '$':
                new_board = move(now_state.board, next_pos,cur_pos)
                new_state = state(new_board, now_state)
                if compare_matrix(new_board, board_B):
                    line = new_state.get_line()
                    line.pop(0)
                    return line
                continue
            new_board_ = move(now_board, next_pos,cur_pos)
            new_board = format(new_board_)
            if is_board_exist_(new_board, list_state):
                continue
            new_state_ = state(new_board_, now_state)
            new_state = state(new_board, now_state)
            list_state.append(new_state)
            list_visit.append(new_state_)
    return[]
        