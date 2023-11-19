from sys import argv
import random


def heuristic(board, pos, ai_player, player):
    if pos == (1, 1):
        return 5

    x, y = pos

    test_board = [row.copy() for row in board]  # Create a copy of the board
    test_board[x][y] = ai_player 
    if check_win(test_board, ai_player) == "win":
        return 99


    test_board = [row.copy() for row in board]  # Create a copy of the board
    test_board[x][y] = player 
    if check_win(test_board, ai_player) == "loss":
        return 99 

    return 0

def check_win(test_board, ai_player):
    for i in range(3):
        if test_board[i][0] == test_board[i][1] == test_board[i][2] != "+":
            if test_board[i][0] == ai_player:
                return "win"
            else:
                return "loss"
        if test_board[0][i] == test_board[1][i] == test_board[2][i] != "+":
            if test_board[0][i] == ai_player:
                return "win"
            else:
                return "loss"

    # Check diagonals
        if test_board[0][0] == test_board[1][1] == test_board[2][2] != "+":
            if test_board[0][0] == ai_player:
                return "win"
            else:
                return "loss"
        if test_board[0][2] == test_board[1][1] == test_board[2][0] != "+":
            if test_board[0][0] == ai_player:
                return "win"
            else:
                return "loss"

    return 



class Node:
    def __init__(self, pos, heuristic):
        self.pos = pos
        self.heuristic = heuristic


class Fronteir():
    def __init__(self):
        self.fronteir = []


    def add(self, node):
        self.fronteir.append(node)
        self.fronteir = sorted(self.fronteir, key=lambda x: (x.heuristic, random.random()))


    def empty(self):
        return len(self.fronteir) == 0


    def move(self):
        if self.empty():
            raise Exception("empty fronteir")
        else:
            node = self.fronteir.pop(-1)
            return node

    def remove(self, xcoord, ycoord):
        if self.empty():
            raise Exception("empty fronteir")
        else:
            for node in self.fronteir:
                if node.pos == (xcoord-1, ycoord-1):
                    self.fronteir.remove(node)


class Board:
    def __init__(self, player):
        self.moves_made = 0
        self.board = [["+", "+", "+",],
                      ["+", "+", "+",],
                      ["+", "+", "+",]]
        self.fronteir = Fronteir()
        if player == "X":
            self.ai_player = "O"
        elif player == "O":
            self.ai_player = "X"
        else:
            raise Exception("You must enter if you are X or O")

        self.player = player


    def game_over(self):
        if self.moves_made == 9:
            print("Draw")
            return True

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "+":
                print(f"{self.board[i][0]} is the winner")
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "+":
                print(f"{self.board[0][i]} is the winner")
                return True

        # Check diagonals
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != "+":
                print(f"{self.board[0][0]} is the winner")
                return True
            if self.board[0][2] == self.board[1][1] == self.board[2][0] != "+":
                print(f"{self.board[0][2]} is the winner")
                return True

        return False 
        

    def print_board(self):
        for row in self.board:
            for space in row:
                print(space, end="")
            print()


    def play_move(self):
        if self.game_over():
            return
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "+":
                    heuristic_value = heuristic(self.board, (i, j), self.ai_player, self.player)
                    self.fronteir.add(Node(pos=(i, j), heuristic=heuristic_value))
        node = self.fronteir.move()
        x, y = node.pos
        self.board[x][y] = self.ai_player 

    
    def play(self):
        last_move = "O" 
        while not self.game_over():
            if last_move != self.ai_player:
                last_move = self.ai_player 
                self.play_move()
                self.print_board()
            else:
                last_move = self.player 
                while True:
                    try:
                        xcoord = int(input("\nEnter x coord: "))
                        ycoord = int(input("Enter y coord: "))
                    except:
                        print("NaN") 
                        continue
                    if xcoord not in range(1, 4):
                        print("xcoord not between 1 and 3")
                        continue
                    if ycoord not in range(1, 4):
                        print("ycoord not between 1 and 3")
                        continue
                    if self.board[ycoord-1][xcoord-1] == "+":
                        self.board[ycoord-1][xcoord-1] = self.player 
                        if self.moves_made != 0:
                            self.fronteir.remove(ycoord, xcoord)
                        break
            self.moves_made += 1


    
if __name__ == "__main__":
    board = Board(argv[1])
    board.play()
