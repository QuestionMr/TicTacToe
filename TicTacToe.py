import pygame
import sys
import pickle
import random

pygame.init()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
dx = [-1, 0, 1, 1]
dy = [1, 1, 1, 0]
turn = 1
status = ["", "X turn", "O turn", "Winner Found", "Draw"]
adjust_to_write_status = 50
search_depth = 3
oo = 1000000000000000000
with open("cell_xor.config", "rb") as rf:
    cell_xor = pickle.load(rf)
    rf.close()
with open("cal_data.config", "rb") as rf:
    cal_data = list(pickle.load(rf))
    rf.close()
start = False
count = 0

#================================================================#

class TicTacToeBoard:
    def __init__(self) -> None:
        global screen
        self.BOARD_SIZE = 10
        self.cell_size = 60
        self.board_length = self.BOARD_SIZE * self.cell_size + adjust_to_write_status
        self.board_width = self.BOARD_SIZE * self.cell_size
        self.screen = pygame.display.set_mode((self.board_width, self.board_length))
        self.cell_val = [[0 for j in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE)]
        self.board_xor = 0
        
    def display(self) -> None:
        self.screen.fill(WHITE)
        if turn == 1 or turn == 2:
            self.screen.blit(game_font.render(status[turn], True, BLACK, WHITE), (230, 0))
        elif turn == 3:
            self.screen.blit(game_font.render(status[turn], True, BLACK, WHITE), (125, 0))
        else :
            self.screen.blit(game_font.render(status[turn], True, BLACK, WHITE), (250, 0))
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                cell_posX = j * self.cell_size
                cell_posY = i * self.cell_size + adjust_to_write_status
                pygame.draw.rect(surface=self.screen, rect = pygame.Rect(cell_posX, cell_posY, self.cell_size, self.cell_size), color=LIGHTBLUE)
                pygame.draw.rect(surface=self.screen, rect = pygame.Rect(cell_posX + 2, cell_posY + 2, self.cell_size - 4, self.cell_size - 4), color=WHITE)
                if self.cell_val[i][j] == 1:
                    self.screen.blit(game_font.render("X", True, RED, WHITE), (cell_posX + 13, cell_posY + 8))
                elif self.cell_val[i][j] == 2:
                    self.screen.blit(game_font.render("O", True, GREEN, WHITE), (cell_posX + 10, cell_posY + 8))
        pygame.display.flip()

#================================================================#

class System:
    def winner_check(self, board: TicTacToeBoard) -> bool:
        for i in range(board.BOARD_SIZE):
            for j in range(board.BOARD_SIZE):
                if board.cell_val[i][j] == 0:
                    continue
                for dir in range(4):
                    check = True
                    for k in range(1, 5):
                        ni = i + k * dx[dir]
                        nj = j + k * dy[dir]
                        if ni < 0 or ni >= board.BOARD_SIZE or nj < 0 or nj >= board.BOARD_SIZE or board.cell_val[ni][nj] != board.cell_val[i][j]:
                            check = False
                            break
                    if check:
                        return True
        return False
    def draw_check(self, board: TicTacToeBoard) -> bool:
        for i in range(board.BOARD_SIZE):
            for j in range(board.BOARD_SIZE):
                if board.cell_val[i][j] == 0:
                    return False
        return True

#================================================================#

shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]

class AI:
    def __init__(self, _turn, _style) -> None:
        self.turn = _turn
        self.style = _style
        self.sys = System()
        pass

    def minimax(self, depth, board: TicTacToeBoard, alpha, beta, maximize):
        global count
        count = count + 1
        id = str(board.board_xor) + str(depth)
        for data in cal_data:
            if data[0] == id:
                return data[1]

        if depth == 0 or self.sys.winner_check(board) or self.sys.draw_check(board):
            return (self.eval(board), [0, 0])

        avail_cell = []
        for i in range(board.BOARD_SIZE):
            for j in range(board.BOARD_SIZE):
                if board.cell_val[i][j] == 0:
                    check = False
                    for k1 in range(-1,2):
                        for k2 in range(-1,2):
                            if k1 == 0 and k2 == 0: continue
                            ni = i + k1
                            nj = j + k2
                            if ni < 0 or ni >= board.BOARD_SIZE or nj < 0 or nj >= board.BOARD_SIZE:continue
                            if board.cell_val[ni][nj]:
                                check = True
                    if check:
                        avail_cell.append((i, j))

        if maximize:
            value = -oo
            pos_move = []
            for pos in avail_cell:
                x = pos[0]
                y = pos[1]
                board.cell_val[x][y] = self.turn
                board.board_xor = board.board_xor ^ cell_xor[x][y][self.turn]
                rvalue = self.minimax(depth - 1, board, alpha, beta, False)[0]
                if rvalue > value:
                    value = rvalue
                    pos_move = []
                    pos_move.append(x)
                    pos_move.append(y)
                alpha = max(alpha, value)
                board.board_xor = board.board_xor ^ cell_xor[x][y][self.turn]
                board.cell_val[x][y] = 0
                if alpha >= beta:
                    break
            cal_data.append((id,(value, pos_move)))
            return (value, pos_move)
        else:
            value = oo
            pos_move = []
            for pos in avail_cell:
                x = pos[0]
                y = pos[1]
                board.cell_val[x][y] = 3 - self.turn
                board.board_xor = board.board_xor ^ cell_xor[x][y][3-self.turn]
                rvalue = self.minimax(depth - 1, board, alpha, beta, True)[0]
                if rvalue < value:
                    value = rvalue
                    pos_move = []
                    pos_move.append(x)
                    pos_move.append(y)
                beta = min(beta, value)
                board.board_xor = board.board_xor ^ cell_xor[x][y][3-self.turn]
                board.cell_val[x][y] = 0
                if alpha >= beta:
                    break
            cal_data.append((id,(value, pos_move)))
            return (value, pos_move)
    
    def minimaxNullmove(self, depth, board: TicTacToeBoard, alpha, beta, maximize):
        global count
        count = count + 1

        avail_cell = []
        for i in range(board.BOARD_SIZE):
            for j in range(board.BOARD_SIZE):
                if board.cell_val[i][j] == 0:
                    check = False
                    for k1 in range(-1,2):
                        for k2 in range(-1,2):
                            if k1 == 0 and k2 == 0: continue
                            ni = i + k1
                            nj = j + k2
                            if ni < 0 or ni >= board.BOARD_SIZE or nj < 0 or nj >= board.BOARD_SIZE:continue
                            if board.cell_val[ni][nj]:
                                check = True
                    if check:
                        avail_cell.append((i, j))
        value = oo
        n_move = []
        for pos in avail_cell:
            x = pos[0]
            y = pos[1]
            board.cell_val[x][y] = 3 - self.turn
            board.board_xor = board.board_xor ^ cell_xor[x][y][3-self.turn]
            rvalue = self.minimax(depth, board, alpha, beta, True)
            if rvalue[0] < value:
                value = rvalue[0]
                n_move = list(rvalue[1])
            beta = min(beta, value)
            board.board_xor = board.board_xor ^ cell_xor[x][y][3-self.turn]
            board.cell_val[x][y] = 0
        return (rvalue, n_move)

    def eval(self, board: TicTacToeBoard):
        ai_score = 0
        for i in range(board.BOARD_SIZE):
            for j in range(board.BOARD_SIZE):
                for dir in range(4):
                    ai_score = ai_score + self.cal(i, j, board, dir, self.turn)

        enemy_score = 0
        for i in range(board.BOARD_SIZE):
            for j in range(board.BOARD_SIZE):
                for dir in range(4):
                    enemy_score = enemy_score + self.cal(i, j, board, dir, 3 - self.turn)

        return ai_score - enemy_score * self.style
    
    def cal(self, px, py, board: TicTacToeBoard, dir, turn):
        shape = []
        for k in range(6):
            nx = px + k * dx[dir]
            ny = py + k * dy[dir]
            if nx < 0 or nx >= board.BOARD_SIZE or ny < 0 or ny >= board.BOARD_SIZE:
                shape.append(-1)
            else:
                if board.cell_val[nx][ny] == turn:
                    shape.append(1)
                elif board.cell_val[nx][ny] == 0:
                    shape.append(0)
                else:
                    shape.append(2)
        shap5 = (shape[0], shape[1], shape[2], shape[3], shape[4])
        shap6 = (shape[0], shape[1], shape[2], shape[3], shape[4], shape[5])

        max_score = 0
        for (score, sh) in shape_score:
            if shap5 == sh or shap6 == sh:
                max_score = max(max_score, score)
        return max_score
    
    def get_next_move(self, board: TicTacToeBoard):
        global start
        global count
        if start == False:
            start = True
            n_move = [int(random.random()*4) + 4, int(random.random()*4)+4]
            return n_move
        '''
        val1 = self.minimaxNullmove(3, board, -oo, oo, True)
        print("With Nullmove:", count)
        count = 0
        return val1[1]'''
        val2 = self.minimax(3, board, -oo, oo, True)
        print("Without Nullmove:", count)
        count = 0
        return val2[1]

#============================Main================================#
board = TicTacToeBoard()
game_sys = System()

def restart_match():
    global start
    global board
    global cal_data
    global turn
    turn = 1
    start = False
    board = TicTacToeBoard()
    with open("cal_data.config", "rb") as rf:
        cal_data = pickle.load(rf)
        rf.close()

def run():
    global turn
    global count
    ai = [0, AI(1, 0.5), AI(2, 1.5)]
    vshuman = False
    playerturn = 2
    while True:
        mouseX = -1
        mouseY = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseY, mouseX = pygame.mouse.get_pos()
                break

        if game_sys.winner_check(board):
            turn = 3
            with open("cal_data.config", "wb") as wf:
                pickle.dump(cal_data, wf)
                wf.close()
            restart_match()
        elif game_sys.draw_check(board):
            turn = 4
            with open("cal_data.config", "wb") as wf:
                pickle.dump(cal_data, wf)
                wf.close()
            restart_match()

        if vshuman:
            if turn < 3:
                if turn == playerturn:
                    if mouseX != -1:
                        px = (mouseX - adjust_to_write_status) // board.cell_size
                        py = mouseY // board.cell_size
                        if board.cell_val[px][py] == 0:
                            board.cell_val[px][py] = turn
                            board.board_xor = board.board_xor ^ cell_xor[px][py][turn]
                            turn = 3 - turn
                else:
                    n_move = ai[turn].get_next_move(board)
                    board.cell_val[n_move[0]][n_move[1]] = turn
                    board.board_xor = board.board_xor ^ cell_xor[n_move[0]][n_move[1]][turn]
                    turn = 3 - turn
        else:
            n_move = ai[turn].get_next_move(board)
            board.cell_val[n_move[0]][n_move[1]] = turn
            board.board_xor = board.board_xor ^ cell_xor[n_move[0]][n_move[1]][turn]
            turn = 3 - turn
        board.display()

if __name__ == "__main__":
    run()