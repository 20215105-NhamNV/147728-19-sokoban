import support_function as spf
import time

def BFS_search(board, list_check_point):
    start_time = time.time()
    
    if spf.check_win(board,list_check_point):
        print("Found win")
        return [board]
    start_state = spf.state(board, None, list_check_point)
    list_state = [start_state]
    list_visit = [start_state]
    while len(list_visit) != 0:
        
        now_state = list_visit.pop(0)
        cur_pos = spf.find_position_player(now_state.board)
       
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        print_matrix(now_state.board)
        print("State visited : {}".format(len(list_state)))
        print("State in queue : {}".format(len(list_visit)))
        '''