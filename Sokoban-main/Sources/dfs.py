import support_function as spf
import time

def DFS_search(board, list_check_point):
    start_time = time.time()
    spf.spfInit(board,list_check_point)
    board_ = spf.format(board)
    start_state = spf.state(board_, None)
    list_state = [start_state]
    list_visit = [start_state]
    while len(list_visit) != 0:
        now_state = list_visit.pop()
        now_board = now_state.board
        list_next_board = spf.get_next_boards(now_board)
        for next_board in list_next_board:
            new_board = next_board
            if spf.is_board_can_not_win(new_board):
                continue
            if spf.is_board_exist(new_board, list_state):
                continue
            new_state = spf.state(new_board, now_state)
            if spf.check_win(new_board):
                print("Found win")
                end_time = time.time()
                print(end_time - start_time)
                print(len(list_state))
                return (new_state.get_line_(), len(list_state))
            list_state.append(new_state)
            list_visit.append(new_state)
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    print("Not Found")
    return []
