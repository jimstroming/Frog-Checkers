import pdb
import random
from copy import deepcopy

class CheckersEngine(object):
    # white on bottom, black on top
   
    def __init__(self):

        firstrow = ['WC','--','WC','--','WC','--','WC','--'] # WC is a white checker
        wpawnrow = ['--','WC','--','WC','--','WC','--','WC'] # WK is a white king
        blnkrow2 = ['WC','--','WC','--','WC','--','WC','--']
        blnkrow3 = ['--','00','--','00','--','00','--','00']
        blnkrow4 = ['00','--','00','--','00','--','00','--']
        blnkrow5 = ['--','BC','--','BC','--','BC','--','BC']
        bpawnrow = ['BC','--','BC','--','BC','--','BC','--'] # BK is a black king       
        lastrow  = ['--','BC','--','BC','--','BC','--','BC'] # BC is a black checker

        self.board = [firstrow, wpawnrow, blnkrow2, blnkrow3,
                     blnkrow4, blnkrow5, bpawnrow, lastrow]
                      
        self.kingjumpoffsetlist          = [[-2,-2],[-2,2],[2,-2],[2,2]]
        self.kingcaptureoffsetlist       = [[-1,-1],[-1,1],[1,-1],[1,1]]
        self.whitejumpoffsetlist           = [[-2,2], [2,2]]
        self.whitecaptureoffsetlist        = [[-1,1], [1,1]]
        self.newkingjumpoffsetlist       = [] # newly promoted king can not move
        self.newkingcaptureoffsetlist    = [] # until the next turn
        self.blackjumpoffsetlist         = [[-2,-2],[2,-2]]
        self.blackcaptureoffsetlist      = [[-1,-1],[1,-1]]

        # define the car variables.   
        # I will write the game first without the car, then add the car.
        self.topcarx    = random.randint(0,7)
        self.topcary    = 4 
        self.board[self.topcary][self.topcarx] = 'CR'
        self.bottomcarx = random.randint(0,7)
        self.bottomcary = 3
        self.board[self.bottomcary][self.bottomcarx] = 'CR'
        self.carcolortomove = 'B'        

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
                           
    def updateboardinplace(self,movelist, board):  
        # the first entry in the movelist is the starting position 
        currentpos = movelist[0]      
        currentx = currentpos[0]
        currenty = currentpos[1]
                
        # for each move in the rest of movelist
        for move in movelist[1:]: 
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
        if currenty == 7 and piece[0] == 'W':
            piece = 'Wk'  # lower case is a newly promoted king
        if currenty == 0 and piece[0] == 'B':
            piece = 'Bk'  # newly promoted kings has to quit jumping this turn
        board[currenty][currentx] = piece    
        
        
    def checkifvalidmove(self, color, move):
        # create the jumplist
        jumplist = self.createjumplist(color, self.board)
        if len(jumplist) != 0:
            if move in jumplist: return True
            else:  return False
            
        # if there is no jumplist, then the move is not a jump
        # we just need to check if the source is the correct color
        # and the destination is legal and empty. 
        
        currentpos = move[0]
        destpos    = move[1]
        #pdb.set_trace()
        piece = self.board[currentpos[1]][currentpos[0]]
        if piece[0] != color: return False
        jumpoffsetlist = self.blackcaptureoffsetlist
        if piece[0] == 'W':
            jumpoffsetlist = self.whitecaptureoffsetlist
        if piece[1] == 'K':
            jumpoffsetlist = self.kingcaptureoffsetlist
        if piece[1] == 'k':
            jumpoffsetlist = []
        actualoffset = [destpos[0]-currentpos[0],destpos[1]-currentpos[1]]
        if not actualoffset in jumpoffsetlist:  return False
        if self.board[destpos[1]][destpos[0]] == '00':  return True
        return False    
        
    def makevalidmove(self,move):
        self.updateboardinplace(move,self.board)  
        # need to change any newly promoted kings from 'k' to 'K'
        for y in range (0,8):
            for x in range (0,8):
                piece = self.board[y][x]
                if piece[1] == 'k':
                    piece = piece[0]+'K'
                    self.board[y][x] = piece
        # move the car
        self.movethecar(self.board)
        
    def movethecar(self,board):
        """ Moves all the cars in the street on one side of the board.
            White side cars move right.
            Black side cars move left.
            Each call it alternates which color moves
        """    
        if self.carcolortomove == 'W':
            y = 3
            increment = 1
            self.carcolortomove = 'B'
        else:
            y = 4
            increment = -1
            self.carcolortomove = 'W'

        newcars = []
        for x in range(0,8):
            if board[y][x] == 'CR':
                board[y][x] = '00'
                newx = x+increment
                if newx == -1: newx = 7
                if newx == 8: newx = 0
                newcars.append(newx)
        for x in newcars:            
            board[y][x] = 'CR'
              
        
    def createjumplist(self,color,board):
        """ Function to create all the legal jumps
            If there are any legal jumps, then 
            the only legal move is one of these jumps. 
        """
        outputjumplist = []
        # loop through all the checkers of the given color
        for y in range(0,8):
            for x in range(0,8):
                currentpiece = board[y][x]
                if currentpiece[0] == color:
                    #print x,y
                    # find the possible jumps from this piece
                    jumplist = self.addtojumplist([[x,y]],color,board)
                    #print jumplist
                    #print len(jumplist[0])
                    if len(jumplist[0]) != 1:
                        outputjumplist += jumplist
                        #print outputjumplist
         
        return outputjumplist     
        
    def addtojumplist(self,jumplist,color,board):
        """ Recursive routine to take the current jump list
            and follow it through to multiple jumps 
            This can only be used on a single checker.
        """
        
        resultjumplist = []  # this is the list we are going to return
        
        # get the current jump position
        currentpos = jumplist[-1]
        #pdb.set_trace()
        currentpiece = board[currentpos[1]][currentpos[0]]
        
        loopsize = 2
        if currentpiece[0] == 'W':
            #pdb.set_trace()
            jumpoffsetlist    = self.whitejumpoffsetlist
            captureoffsetlist = self.whitecaptureoffsetlist
        else:
            jumpoffsetlist    = self.blackjumpoffsetlist
            captureoffsetlist = self.blackcaptureoffsetlist
        
        if currentpiece[1] == 'K':
            loopsize = 4
            jumpoffsetlist    = self.kingjumpoffsetlist
            captureoffsetlist = self.kingcaptureoffsetlist
            
        if currentpiece[1] == 'k':
            loopsize = 0
            jumpoffsetlist = []
            captureoffsetlist = []
        
        # loop through all the possible jumps from the current position
        for i in range(0,loopsize):
            # check if the jump destination is open
            #print i
            #print jumpoffsetlist
            jumpoffset = jumpoffsetlist[i]
            jumpx = currentpos[0]+jumpoffset[0]
            jumpy = currentpos[1]+jumpoffset[1]
            if jumpx < 0 or jumpx > 7: continue
            if jumpy < 0 or jumpy > 7: continue     
            if board[jumpy][jumpx] != '00': continue   
            # check if there is an opposing checker to capture
            captureoffset = captureoffsetlist[i]
            capturex = currentpos[0]+captureoffset[0]
            capturey = currentpos[1]+captureoffset[1]
            capturepiece = board[capturey][capturex] 
            if capturepiece == '00': continue
            if capturepiece[0] == color: continue
            if capturepiece[0] == 'C': continue
        
            # we have found a legal jump
    
            # create a board to account for the jump
            newboard = self.fastcopy(board)
            # create the current move
            movelist = [currentpos]
            movelist.append([jumpx,jumpy])
            # update the board to account for the jump
            self.updateboardinplace(movelist, newboard)
            # create a copy of the jump list
            newjumplist = deepcopy(jumplist)
            # append the new jump to the list
            newjumplist.append([jumpx,jumpy])
            # check if the piece was promoted to king
            currentpiece = newboard[jumpy][jumpx]
            if currentpiece[1] == 'k':
                resultjumplist.append(newjumplist)
            else:
                # if not, recursively call addtojumplist
                outputjumplist = self.addtojumplist(newjumplist,color,newboard)
                # append each list in the output to the resultjumplist
                resultjumplist += outputjumplist
        # return the resultjumplist
        if resultjumplist == []:
            resultjumplist.append(jumplist)
        return resultjumplist          
                         
                         
if __name__ == '__main__':
    import time
    import cProfile
    cb = CheckersEngine()  
    cb.printboard(cb.board)
    #jumplist = [[1,1]]
    #newjumplist = cb.addtojumplist(jumplist,'W',cb.board)
    #print newjumplist
    print "move"
    print cb.checkifvalidmove('B', [[3,3],[4,4]])
    pdb.set_trace()
    cb.makevalidmove([[4,2],[5,3]])
    cb.printboard(cb.board)
    print "move"
    print cb.checkifvalidmove('B', [[7,5],[6,4]])    
    cb.makevalidmove([[7,5],[6,4]])
    cb.printboard(cb.board)
    print "move"
    print cb.checkifvalidmove('W', [[0,2],[1,3]])
    cb.makevalidmove([[0,2],[1,3]])
    cb.printboard(cb.board)
    
    """print "move"
    cb.makevalidmove([[5,5],[4,4]])
    print "move"
    cb.makevalidmove([[7,5],[6,4]])
    print "move"
    cb.makevalidmove([[6,4],[5,3]])
    cb.printboard(cb.board)
    #jumplist = [[3,3]]
    #newjumplist = cb.addtojumplist(jumplist,'W',cb.board)
    #print newjumplist
    totaljumplist = cb.createjumplist('W',cb.board)
    print totaljumplist"""
    #pdb.set_trace()