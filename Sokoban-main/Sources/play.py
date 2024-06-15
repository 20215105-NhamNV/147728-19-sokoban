import support_function as spf

def Play(board, list_check_point):
    spf.spfInit(board,list_check_point)
    return (board,spf.check_win(board))
def move(board, i):
    board = spf.move_(board, i)
    return (board,spf.check_win(board))