# modules
import sys # quits app
import copy
import random
import pygame
import numpy as np

width = 600
height = 600
bg_color = (28, 170, 156)

ROWS = 3
COLS = 3
SQSIZE = width // COLS # or height // rows

line_color = (23,135, 145) 
line_width = 15 

circ_color = (239, 123, 126)
circ_width = 15
radius = SQSIZE // 4 

offset = 50


# pygame set up; always the same lines for set-up
pygame.init() # 1. initialize
screen = pygame.display.set_mode((width, height)) # 2. screen
pygame.display.set_caption(' TIC TAC TOE ') # 3. caption
screen.fill(bg_color) # 4. color of bg

class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) ) # creates a 3 x 3 array filled with 0s
        self.empty_sqrs = self.squares # list of empty squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 is player 1 wins
            @return 2 if player 2 wins
        '''
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0: 
                if show:
                    color = circ_color if self.squares[0][col] == 2 else "yellow"
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[0][col] # return any column input; a 1 ; if player 1 wins

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circ_color if self.squares[row][0] == 2 else "yellow"
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (width - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[row][0] 
            
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = circ_color if self.squares[1][1] == 2 else "yellow"
                    iPos = (20, 20)
                    fPos = (width - 20, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
            return self.squares[1][1] 
        
        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    color = circ_color if self.squares[1][1] == 2 else "yellow"
                    iPos = (20, height - 20)
                    fPos = (width - 20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
            return self.squares[1][1]
        
        return 0 # if no win

    def mark_sqr(self, row, col, player): # player inputs mark of a square
        self.squares[row][col] = player
        self.marked_sqrs += 1 

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0 
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs == 9 # if board is full
    
    def isempty(self):
        return self.marked_sqrs == 0 # if board is empty
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board): 
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs)) # place mark somewhere random

        return empty_sqrs[idx] # return a row, col
    
    def minimax(self, board, maximizing):

        # terminal cases
        case = board.final_state() # returns 0-2

        # player 1 wins
        if case == 1:
            return 1, None
        
        # player 2 wins
        if case == 2:
            return -1, None # minimizing 
        
        # if draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board) # copy board temporarily
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0] # eval; 1,-1, 0
                if eval > max_eval:
                    max_eval = eval 
                    best_move = (row, col) # best move is row, col that lead to minimum eval

            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board) # copy board temporarily
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0] # eval; 1,-1, 0
                if eval < min_eval:
                    min_eval = eval 
                    best_move = (row, col) # best move is row, col that lead to minimum eval

            return min_eval, best_move
        
    def eval_board(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algorithm
            eval, move = self.minimax(main_board, False) # minimizing

        print(f'AI has selected to mark the square in pos {move} with an eval of: {eval}')
        return move # row, col 
    
class Game:

    def __init__(self):
        self.board = Board() 
        self.ai = AI() 
        self.player = random.randint(1, 2) # 1 is X, 2 is O
        self.gamemode = 'ai' # or ai 
        self.running = True # game is not over
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player) # marks what we click for player 
        self.draw_fig(row, col)
        self.next_turn()


    def show_lines(self):
        screen.fill(bg_color)
        # vertical
        pygame.draw.line(screen, line_color, (SQSIZE, 0), (SQSIZE, height), line_width) # start at sq size on x axis and 0 on y axis, finish at sq.size and 0 on height of y axis
        pygame.draw.line(screen, line_color, (width - SQSIZE, 0), (width - SQSIZE, height), line_width) # move over more on the x axis (600-200) 

        # horizontal
        pygame.draw.line(screen, line_color, (0, SQSIZE), (width, SQSIZE), line_width) # start at 0 on x axis, and sq size on y axis, and finish at max width, and sq size  
        pygame.draw.line(screen, line_color, (0, width - SQSIZE), (width, height-SQSIZE), line_width)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw a cross
            # desc line
            start_desc = (col * SQSIZE + offset, row * SQSIZE + offset)
            end_desc = (col * SQSIZE + SQSIZE - offset, row * SQSIZE + SQSIZE - offset)
            pygame.draw.line(screen, "red", start_desc, end_desc, 15)
            # asc line
            start_asc = (col * SQSIZE + offset, row * SQSIZE + SQSIZE - offset)
            end_asc = (col * SQSIZE + SQSIZE - offset, row * SQSIZE + offset)
            pygame.draw.line(screen, "red", start_asc, end_asc, 15)

        elif self.player == 2:
            # draw a circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, "black", center, radius, 15)

    def next_turn(self):
        self.player = self.player % 2 + 1 # 2 modulo 2 no remainder + 1 = player 1 turn; 1 modulo 2 remainder 1 + 1 = player 2 turn
    
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
    
    def isover(self):
        return self.board.final_state(show = True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__() # restarting all our attributes to default values

# main
def main():
    
    # game object to call class
    game = Game()
    board = game.board
    ai = game.ai 

    while True:

        for event in pygame.event.get(): # always same lines in pygame to make sure we quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g key to change game mode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                
                # restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai 

                # 0 is random AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 is AI level 1
                if event.key == pygame.K_1:
                    ai.level = 1 

            if event.type == pygame.MOUSEBUTTONDOWN: # if we are clicking screen
                pos = event.pos # returns coordinates based on what we click
                row = pos[1] // SQSIZE # makes values into 0,0 ; 0,1 if we click on an area...
                col = pos[0] // SQSIZE 

                if board.empty_sqr(row, col) and game.running: # if sq is empty
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update screen
            pygame.display.update()

            # ai methods
            row, col = ai.eval_board(board)
            game.make_move(row,col)

            if game.isover():
                game.running = False

        pygame.display.update()

main()