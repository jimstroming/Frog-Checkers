import pdb
import random

class CheckersEngine(object):
    # white on bottom, black on top
   
    def __init__(self):
        firstrow = ['RC','--','RC','--','RC','--','RC','--'] # RC is a red checker
        wpawnrow = ['--','RC','--','RC','--','RC','--','RC'] # RK is a red king
        blnkrow2 = ['RC','--','RC','--','RC','--','RC','--']
        blnkrow3 = ['--','00','--','00','--','00','--','00']
        blnkrow4 = ['00','--','00','--','00','--','00','--']
        blnkrow5 = ['--','BC','--','BC','--','BC','--','BC']
        bpawnrow = ['BC','--','BC','--','BC','--','BC','--'] # BK is a black king
        lastrow  = ['--','BC','--','BC','--','BC','--','BC'] # BC is a black checker
        self.board = [firstrow, wpawnrow, blnkrow2, blnkrow3,
                     blnkrow4, blnkrow5, bpawnrow, lastrow]
        topcarx    = 0   # the top car starts on the left border
        topcary    = 4
        topcarwidth = 2
        bottomcarx = 6   # the bottom car stars on the right border
        bottomcary = 3
        bottomcarwidth = 2

    def printboard(self,board):
        for x in range(0,8):
            print board[7-x] 
            
    def getpiece(self, x, y):
        return self.board[y][x]        
            
    def fastcopy(self, b):
        return     [[b[0][0],b[0][1],b[0][2],b[0][3],b[0][4],b[0][5],b[0][6],b[0][7]],
                    [b[1][0],b[1][1],b[1][2],b[1][3],b[1][4],b[1][5],b[1][6],b[1][7]],
                    [b[2][0],b[2][1],b[2][2],b[2][3],b[2][4],b[2][5],b[2][6],b[2][7]],
                    [b[3][0],b[3][1],b[3][2],b[3][3],b[3][4],b[3][5],b[3][6],b[3][7]],
                    [b[4][0],b[4][1],b[4][2],b[4][3],b[4][4],b[4][5],b[4][6],b[4][7]],
                    [b[5][0],b[5][1],b[5][2],b[5][3],b[5][4],b[5][5],b[5][6],b[5][7]],
                    [b[6][0],b[6][1],b[6][2],b[6][3],b[6][4],b[6][5],b[6][6],b[6][7]],
                    [b[7][0],b[7][1],b[7][2],b[7][3],b[7][4],b[7][5],b[7][6],b[7][7]]]
                           
    def updateboardinplace(self,sourcex, sourcey, movelist, board):          
        currentx = sourcex
        currenty = sourcey
        # for each move in the movelist
        for move in movelist: 
            piece = board[currenty][currentx]  
            # check for capture
            if abs(move[0]-currentx) == 2:
                capturex = (move[0]+currentx)/2
                capturey = (move[1]+currenty)/2     
                board[capturey][capturex] = '00' 
            # make the move
            board[currenty][currentx] = '00'
            board[move[1]][move[0]] = piece
            currentx = move[0]
            currenty = move[1]
        
        # after the last move, see if we need to promote the checker to a king
        if currenty == 7 and piece[0] == 'R':
            piece = 'RK'
        if currenty == 0 and piece[0] == 'B':
            pice = 'BK'
        board[currenty][currentx] = piece                     
                         
                         
if __name__ == '__main__':
    import time
    import cProfile
    cb = CheckersEngine()  
    cb.printboard(cb.board)
    print "move"
    cb.updateboardinplace(2,2,[[3,3]],cb.board)
    cb.printboard(cb.board)
    print "move"
    cb.updateboardinplace(1,5,[[2,4]],cb.board)
    cb.printboard(cb.board)
    print "move"
    cb.updateboardinplace(3,3,[[1,5]],cb.board)
    cb.printboard(cb.board)    
    #pdb.set_trace()