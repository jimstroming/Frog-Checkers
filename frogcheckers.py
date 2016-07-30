import pdb
import random

class CheckersEngine(object):
    # white on bottom, black on top
   
    def __init__(self):
        firstrow = ['RC','00','RC','00','RC','00','RC','00'] # RC is a red checker
        wpawnrow = ['00','RC','00','RC','00','RC','00','RC'] # RK is a red king
        blnkrow2 = ['RC','00','RC','00','RC','00','RC','00']
        blnkrow3 = ['00','00','00','00','00','00','00','00']
        blnkrow4 = ['00','00','00','00','00','00','00','00']
        blnkrow5 = ['00','BC','00','BC','00','BC','00','BC']
        bpawnrow = ['BC','00','BC','00','BC','00','BC','00'] # BK is a black king
        lastrow  = ['00','BC','00','BC','00','BC','00','BC'] # BC is a black checker
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

    pdb.set_trace()