import pdb
import random

class CheckersEngine(object):
    # white on bottom, black on top
   
    def __init__(self):
        firstrow = ['Wr','WN','WB','WQ','Wk','WB','WN','Wr'] # r is a R that hasn't moved
        wpawnrow = ['Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wp'] # p is a P that hasn't moved
        blnkrow2 = ['00','00','00','00','00','00','00','00']
        blnkrow3 = ['00','00','00','00','00','00','00','00']
        blnkrow4 = ['00','00','00','00','00','00','00','00']
        blnkrow5 = ['00','00','00','00','00','00','00','00']
        bpawnrow = ['Bp','Bp','Bp','Bp','Bp','Bp','Bp','Bp']
        lastrow  = ['Br','BN','BB','BQ','Bk','BB','BN','Br'] # k is a K that hasn't moved
        self.board = [firstrow, wpawnrow, blnkrow2, blnkrow3,
                     blnkrow4, blnkrow5, bpawnrow, lastrow]
                     

    def printboard(self,board):
        for x in range(0,8):
            print board[7-x] 
            
    def getpiece(self, x, y):
        return self.board[y][x]        
            
 
        
                         
if __name__ == '__main__':
    import time
    import cProfile
    cb = CheckersEngine()  
