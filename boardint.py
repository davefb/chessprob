import sys
import os
import pickle
import time
from chess import *
from parse import *

class boardint:

    def __init__(self):
        self.treeFile = open('/home/dfb/chessprob/out','r');
        self.tree = [];

        self.out = sys.__stdout__
        self.debug = file('/home/dfb/test', 'w')
        self.setup_stream()

        self.stop = False
        self.postmode = False
        self.bookmode = True

        self.internalState = Game();


    def __sayfilter__(self,x):
        if x[-1] == '\n':
            return x
        return (x+'\n')


    def setup_stream(self):
        self.pipe    = os.popen("java -cp /home/dfb/chessprob/lamewindow/ Console",'w');
        
    def say(self,tosay):
        if type(tosay) == str:
            tosay = [tosay]
            
        tosay = map( self.__sayfilter__ , tosay )
        self.out.writelines( tosay );
        self.out.flush();
    
    def toconsole(self, tosay):
        if type(tosay) == str:
            tosay = [tosay]

        self.pipe.writelines(map( lambda x: "%s\n" % x , tosay));
        self.pipe.flush();
        
    def init(self):
        self.say("feature analyze=1 sigint=0 usermove=1 colors=0");
        self.me = self.internalState.whose();
        self.tree = pickle.load(self.treeFile);

    def boardtohash(self, str):
        if self.me == self.internalState.whose():
            return "%s1" % str[:-1]
        else:
            return "%s0" % str[:-1]

    def gettreeinfo(self):

        self.toconsole("\t");
        
        state = self.internalState.__str__()
        try:
            node = self.tree.getnode(state)
        except:
            self.toconsole("Not in book");
            return
        
        firstline = "CURRENT POSITION - %d"
        
        self.toconsole(firstline % node.all);
        self.toconsole( "%d items" % len(node.children));

        cloneboard = self.internalState.clone();
        for move in node.children:
            mv = cloneboard.move( move );
            self.toconsole( "%s %s" % (mv.shortAlgebraic() , self.tree.getnode(self.boardtohash("%s"%cloneboard)).all) )
            cloneboard.takeback();

    def makemove(self,move):
        self.internalState.move(move);
        
    def processCommand(self,cmd, args):
        if cmd == "xboard":
            self.init()
        elif cmd == "new":
            self.internalState = Game();
        elif cmd == "undo":
            self.internalState.takeback();
        elif cmd == "analyze":
            pass
        elif cmd == "post":
            self.postflag = True;
        elif cmd == "nopost":
            self.postflag = False;
        elif cmd == "bk":
            self.bookmode  = True;
        elif cmd == "go":
            pass
        elif cmd == 'usermove':
            self.tree.nodes["%s"%self.internalState].invite( chessvisitor(), self.tree)
            self.makemove(args[0]);
        elif cmd == 'quit':
            self.stop = True;

        self.gettreeinfo()

    def loopforever(self):
        while not self.stop:
            #time.sleep(0.100);

            t = sys.__stdin__.readline();
            self.debug.writelines([t]);
            self.debug.flush();

            t = t.strip();
            tsplit = t.split(" ");

            if t:
                self.processCommand( tsplit[0], tsplit[1:] );


        self.pipe.close();
        self.debug.close();

    def main(self):
        self.loopforever()

boardint().main()
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
