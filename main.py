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
        """
        self.purewhite   = ( 1,   1,  1, 1)
        self.brightwhite = (0.9,0.9,0.9, 1)
        self.lightgray   = (0.6,0.6,0.6, 1)
        self.darkgray    = (0.4,0.4,0.4, 1)   
        self.darkblack   = (0.1,0.1,0.1, 1)     
        self.pureblack   = ( 0,   0,  0, 1)
        self.ids["messageW"].text = 'Your Move'
        self.ids["messageB"].text = 'Black Move'
        #self.setcancelandmovebuttons('cancel','move')
        self.blind = 1    # 1 means blind.  0 means show the pieces  
        self.sourcex = -1  # set the source and destination to none
        self.sourcey = -1 
        self.destx = -1
        self.desty = -1     
        #self.resetbothmistakecounts()
        #self.updateboardui()
        for x in range(0,8):
            for y in range(0,8):
               #self.resetsquarebackground(x,y)
        self.whosemove = 'W' # white moves first
        #self.setwidgetbackgroundcolors()
        self.ids['clockW'].text = "10:00"
        self.ids['clockB'].text = "10:00"
        self.ids['messageW'].font_size = '30dp'
        self.ids['messageB'].font_size = '30dp'
        self.cancelcount = 0 # pressing cancel 3 times in a row toggles self.blind
        self.resetcount  = 0 # pressing any board square 5 times in a row
                             # resets the game
        self.resetx = 0
        self.resety = 0
        #Clock.schedule_interval(self.updateclocks, 1)
        if self.whiteplayer == 'human':
            self.state = "looking for source"        
        else:
            self.state = "cpu turn to move"
            #self.cpumove(0)
        """


    def createcheckersengine(self):
        """ Creates the checkers engine.  Maintains the game state and enforces move rules."""
        self.checkersengine = CheckersEngine() 
        
        
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
        

class RoadKillFrogApp(App):
    """ The kivy game app."""
    pass


if __name__ == '__main__':
    RoadKillFrogApp().run()
