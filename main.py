from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
import time
from frogcheckers import CheckersEngine

class RoadkillFrogRoot(BoxLayout):
    def initialsetup(self):  # called at the beginning of the game
        """ initialize the game state.  Called on the first button press."""
        print "DAGWOOD10"        
        self.createcheckersengine()
        print "DAGWOOD11"
        self.rowspritenames = ['lilypad','lilypad','lilypad','street_bottom',
                               'street_top','lilypad','lilypad','lilypad']
        self.spritegraphics = {
                   'WC': '_white',
                   'WK': '_whiteking',
                   'BC': '_black',
                   'BK': '_blackking',
                   'CR': '_car',
                   '00': ''}
                           
        self.purewhite   = ( 1,   1,  1, 1)
        self.brightwhite = (0.9,0.9,0.9, 1)
        self.lightgray   = (0.6,0.6,0.6, 1)
        self.darkgray    = (0.4,0.4,0.4, 1)   
        self.darkblack   = (0.1,0.1,0.1, 1)     
        self.pureblack   = ( 0,   0,  0, 1)
        self.ids["messageW"].text = 'Your Move'
        self.ids["messageB"].text = 'Black Move'
        self.setcancelandmovebuttons('cancel','move')
        self.blind = 0    # 1 means blind.  0 means show the pieces  
        self.movelist = []   
        self.resetbothmistakecounts()
        self.updateboardui()
        #for x in range(0,8):
        #    for y in range(0,8):
        #       #self.resetsquarebackground(x,y)
        
        self.whosemove = 'W' # white moves first
        self.setwidgetbackgroundcolors()
        self.ids['clockW'].text = "10:00"
        self.ids['clockB'].text = "10:00"
        self.ids['messageW'].font_size = '30dp'
        self.ids['messageB'].font_size = '30dp'
        self.cancelcount = 0 # pressing cancel 3 times in a row toggles self.blind
        self.resetcount  = 0 # pressing any board square 5 times in a row
                             # resets the game
        self.resetx = 0
        self.resety = 0
        Clock.schedule_interval(self.updateclocks, 1)
        self.state = "looking for moves"        

    def createcheckersengine(self):
        """ Creates the checkers engine.  Maintains the game state and enforces move rules."""
        self.checkersengine = CheckersEngine() 
        
    def updateboardui(self): 
        """ Update the display to match the engine."""
        print "DAGWOOD70"
        if self.blind == 1: return
        for x in range(0,8):
            for y in range(0,8):
                print "DAGWOOD20",x,y
                stringid = "but"+str(x)+str(y)
                colorpiece = self.checkersengine.getpiece(x,y)
                buttonid = "but"+str(x)+str(y)
                print "DAGWOOD21"
                if colorpiece != '--':
                    print "DAGWOOD22a", colorpiece
                    buttongraphic = self.rowspritenames[y]+self.spritegraphics[colorpiece]+'.png'
                    print "DAGWOOD23a", buttongraphic 
                else:
                    buttongraphic = 'water.png'
                    if y == 3:
                        buttongraphic = 'street_bottom.png'
                    if y == 4:
                        buttongraphic = 'street_top.png'    
                self.ids[buttonid].background_normal = buttongraphic   
                self.ids[buttonid].background_color = [1, 1, 1, 1]                   

    def setallfontsonecolor(self, color):
        """ Sets the button and counts to a color to alert the player something has happened."""
        self.ids['clockW'].color = color
        self.ids['clockB'].color = color
        self.ids['mistakecountW'].color = color                
        self.ids['mistakecountB'].color = color                
        self.ids['moveW'].color = color
        self.ids['moveB'].color = color
        self.ids['cancelW'].color = color
        self.ids['cancelB'].color = color
        
    def restoreallfonts(self):
        """ Restores the button and counts to their original color."""
        almostblack = (0.2,0.2,0.2,1)
        almostwhite = (0.8,0.8,0.8,1)
        self.ids['clockW'].color = almostwhite
        self.ids['clockB'].color = almostblack
        self.ids['mistakecountW'].color = almostwhite                
        self.ids['mistakecountB'].color = almostblack              
        self.ids['moveW'].color = self.darkgray
        self.ids['moveB'].color = self.lightgray
        self.ids['cancelW'].color = self.darkgray
        self.ids['cancelB'].color = self.lightgray
        
                   
    def getboardcolor(self,x,y):
        """ Returns the background color of a board square."""
        if (y%2 == 0 and x%2 == 0) or (y%2 == 1 and x%2 == 1):
            return self.darkgray
        else:
            return self.lightgray  
            
    def updateclocks(self,dt):
        """ Adds one second to the active board clock."""
        if self.whosemove == 'W':
            timestring = self.ids['clockW'].text
        else:
            timestring = self.ids['clockB'].text
            
        if timestring != '00:00':
            if timestring[4] != '0':
                timestring = timestring[0:4]+str(int(timestring[4])-1)
            else:
                if timestring[3] != '0':
                    timestring = timestring[0:3]+str(int(timestring[3])-1)+'9'
                else:
                    if timestring[1] != '0':
                        timestring = timestring[0]+str(int(timestring[1])-1)+timestring[2]+'59'
                    else:
                        timestring = str(int(timestring[0])-1)+'9:59'
        if self.whosemove == 'W':
            self.ids['clockW'].text = timestring
        else:
            self.ids['clockB'].text = timestring            
            
    def setwidgetbackgroundcolors(self):
        """ Sets the background color of the move and cancel buttons."""
        if self.whosemove == 'W': 
            blackcolor = self.darkgray
            whitecolor = self.brightwhite
        else:
            blackcolor = self.darkblack
            whitecolor = self.lightgray
        self.ids["moveB"].background_color = blackcolor
        self.ids["cancelB"].background_color = blackcolor
        self.ids["moveW"].background_color = whitecolor
        self.ids["cancelW"].background_color = whitecolor
        
        
        
        
        
        
        
        

    def setcancelandmovebuttons(self,canceltext,movetext):
        self.ids["moveB"].text = movetext
        self.ids["cancelB"].text = canceltext
        self.ids["moveW"].text = movetext
        self.ids["cancelW"].text = canceltext
         
        
    def resetbothmistakecounts(self):    
        labelidblack = "mistakecountB"
        labelidwhite = "mistakecountW"
        self.ids[labelidblack].text = str(0)
        self.ids[labelidwhite].text = str(0)
        
    def increasemistakecount(self,color):
        """ Increment the mistake count of the active player."""
        # read the mistake count and convert to a number
        labelid = "mistakecount"+color 
        mistakecount = int(self.ids[labelid].text) 
        mistakecount += 1 # increment
        self.ids[labelid].text = str(mistakecount) # convert to a string and update
        
    def updatebothmessages(self, message, colortodraw):
        """" Update the on screen message to both players."""
        colorvalue = self.purewhite
        if colortodraw == 'B' : colorvalue = self.pureblack
        self.ids['messageW'].text = message
        self.ids['messageB'].text = message
        self.ids['messageW'].color = colorvalue
        self.ids['messageB'].color = colorvalue
        
    def updatemessage(self,message,colortoupdate,colortodraw):
        """ Update the on screen message of one of the players."""
        labelid = "message"+colortoupdate 
        self.ids[labelid].text = message
        if colortodraw == 'W':
            self.ids[labelid].color = self.purewhite
        else:
            self.ids[labelid].color = self.pureblack
 
    def resetaftermove(self):
        """ Reset the board after a move."""
        # reset both the cursors ui
        #if self.sourcex != -1:
        #    self.resetsquarebackground(self.sourcex,self.sourcey)
        #if self.destx != -1:    
        #    self.resetsquarebackground(self.destx,self.desty)
        # reset the source and destination
        self.movelist = []
        # redraw the board
        self.updateboardui()
        # reset the message colors
        self.restoreallfonts()
        # set the state
        self.state = "looking for moves"

            
    def buttonpress(self, x, y):
        """ Process a button press on the game board.  Each board square is a button."""
        print "DAGWOOD40"
        message = self.ids["messageB"].text
        if message == 'Select Number of Players':
            return 
        self.cancelcount = 0
        if self.resetcount == 0:  # pressing the same square five times in a row
            self.resetcount = 1   # resets the game
            self.resetx = x
            self.resety = y
        elif self.resetx == x and self.resety == y:
            self.resetcount += 1
        else:
            self.resetcount = 0
     
        if self.resetcount == 5:
            del self.checkersengine
            self.initialsetup()   
            return
     
        if self.state == "looking for moves":
            buttonid = "but"+str(x)+str(y)  
            # add the press to the move list  
            print "DAGWOOD41" 
            self.movelist.append([x,y])
            if self.whosemove == 'W':
                self.ids[buttonid].background_color = self.purewhite
            else:
                self.ids[buttonid].background_color = self.pureblack
            self.ids[buttonid].background_normal = ''
            return
                    
        
    def movebuttonpress(self, color):
        """ Process a press on the move button."""
        message = self.ids["messageB"].text
        if message == 'Select Number of Players':
            self.numberplayers = 2
            self.blackplayer = 'human'
            self.whiteplayer = 'human'    
            self.initialsetup()
            return
        self.cancelcount = 0    
        self.resetcount = 0        
        if self.whosemove == color:
  
            if self.state == "looking for moves" and len(self.movelist) > 1:
                # check if the move is legal
                print "DAGWOOD60", self.whosemove, self.movelist
                validmove = self.checkersengine.checkifvalidmove(self.whosemove, self.movelist)
                print "DAGWOOD61", validmove
                if validmove:  
                    #self.movestring = self.chessengine.getmovenotation(self.sourcex, self.sourcey, 
                    #                self.destx, self.desty) # get the move notation
                    print "DAGWOOD62"
                    self.checkersengine.makevalidmove(self.movelist)
                    print self.checkersengine.printboard(self.checkersengine.board)
                    print "DAGWOOD63"
                    #self.updatebothmessages(self.movestring,self.whosemove)
                    print "DAGWOOD64"
                    if self.whosemove == 'B': # switch the players turn
                        self.whosemove = 'W'
                    else:
                        self.whosemove = 'B'
                    print "DAGWOOD65"
                    self.setwidgetbackgroundcolors()
                    print "DAGWOOD66"
                    self.resetaftermove()
                    print "DAGWOOD67"
                else:
                    self.increasemistakecount(self.whosemove)
                    self.resetaftermove()
                    self.setallfontsonecolor((1,0,0,1)) # turn the fonts red
                return
        
    def cancelbuttonpress(self, color):
        """ Process a press on the cancel button."""
        message = self.ids["messageB"].text
        if message == 'Select Number of Players':
            self.numberplayers = 1
            if color == 'B': 
                self.whiteplayer = 'cpu'
                self.blackplayer = 'human'
            else:
                self.whiteplayer = 'human'
                self.blackplayer = 'cpu'                 
            self.initialsetup()
            return
        self.cancelcount += 1
        self.resetcount = 0
        if self.cancelcount == 3:
            self.blind = 1-self.blind
            self.cancelcount = 0            
        if self.whosemove == color:            
            self.resetaftermove()


class RoadKillFrogApp(App):
    """ The kivy game app."""
    pass


if __name__ == '__main__':
    RoadKillFrogApp().run()
