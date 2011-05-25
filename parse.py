import pickle
import re
from chess import *

INITIALELO = 1800;
ME = 'spintheblack';
WHITE = 0;
BLACK = 1;
NOTMYMOVE, MYMOVE = (0,1);

class maxvisitor:
    def __init__(self):
        self.lowest = 0
        self.lowestv = ''

    def visit(self,node):
        if(self.lowest < node.all):
            self.lowest = node.all;
            self.lowestv = node;


class chessvisitor:
    def __init__(self):
        self.game = None

    def visit(self,node,tree):
        """ general visiting method, should be
        called by any subclasses' visitXXX method to initialize state
        """
        if not self.game:
            self.game = Game( node.board )
        self.generaltraverse(node,tree);

    def generaltraverse(self,node,tree):
        """ general DFS traversal, can be
        called after visit method to visit all children """
        for mv in node.children:
            self.game.move( mv )
            tree.nodes[self.game].invite(self,tree)
            self.game.takeback();
    
        
class Node:
    def __init__(self, board, props):
        self.board = board
        self.children = set()


        self.all = int(props["MyRating"])
        self.gamesplayed = 0
        self.gameswon   = 0

    def __hash__(self):
        return self.__str__(self)

    def __str__(self):
        return self.board

    def invelo(self,opp):
        """
        get the probability of winning given
        the opponents rating """
        return 1/(1.0 + pow(10,((opp-self.all)/400.0)))
        
    def updateelo(self,toupdate, win, oppelo):
        """ Update the ELO of the current node.
        TODO: make K dynamic based on the games played ala USCF ratings """
        
        K = 32
        e_me =  1/(1.0 + pow(10,((int(oppelo)-toupdate)/400.0)))
        toupdate = toupdate + K*(win-e_me)
        return toupdate

    def invite(self, visitor, tree):
        visitor.visit(self,tree)
        
    def update(self, updateprop):
        self.gamesplayed += 1
        self.gameswon += updateprop["Result"]

        opponentelo = int( updateprop["OppRating"] )
        self.all = self.updateelo(self.all, updateprop["Result"], opponentelo)

#        for k,v in updateprop.iteritems():
#            if k in self.props:
#                self.props[k].update(v,updateprop["Result"], opponentelo,myelo)
#            else:
#                self.props[k] = Property(k,v)

class ChessTree:
    DEFAULTMAXNEWPILES = 20

    def __init__(self):
        self.nodes = {}

        self.maxnewpiles = ChessTree.DEFAULTMAXNEWPILES

    def getwhiteroot(self):
        return self.nodes["rnbqkbnr pppppppp ........ ........ ........ ........ PPPPPPPP RNBQKBNR01"]

    def getblackroot(self):
        return self.nodes["rnbqkbnr pppppppp ........ ........ ........ ........ PPPPPPPP RNBQKBNR00"]

    def getnode(self, hash):
        return self.nodes[hash]

    def board2state(self,pos, props, whitetomove):
        """ Change board representation pos to the state representation
            eg. switching the color bit if it is the user's move and we are black """
        newpos = "%s%d"%pos
        if props["MyColor"] == WHITE:
            newpos += "%d"%whitetomove
        if props["MyColor"] == BLACK:
            blacktomove = (whitetomove+1)%2
            newpos += "%d"%blacktomove

        return newpos


    def walk(self, game,props):
        i = 0;
        for pos in game.boardstate:
            newpos = self.board2state(pos,props,i%2)
            print newpos
            if newpos in self.nodes:
                cur = self.nodes[newpos]
                print cur.all
            i+=1


    def addGame(self, game, props):
        prev = None

        seen = set()
        numnew = 0;

        i = 0;
        # boardstate is a tuple of (board representation, turn to move)
        print props["MyColor"]
        for pos in game.boardstate:

            statekey = self.board2state(pos,props,i%2)
            print statekey
            # make sure we don't update the ELO of a repeated position 
            if statekey in seen:
                continue

            # if adding new nods, only go as deep as maxnewpiles
            if numnew==self.maxnewpiles:
                break
            
            numnew+=1;
            seen.add(statekey)

            cur = None

            if statekey in self.nodes:
                cur = self.nodes[statekey]
            else:
                cur = Node(statekey,props)
                self.nodes[statekey] = cur

            cur.update(props)                 

            if prev:
                movetup = game.moves[i-1]
                mv = Move("",movetup[0],movetup[1])
                prev.children.add( (str(statekey), "%s-%s" % game.moves[i-1]) )

            prev = cur

            i+=1

class Property:
    def __init__(self, name, p=None):
        self.name = name;
        self.values = dict();
        self.values[p] = INITIALELO;

    def __hash__(self):
        return self.__name__

    def init_val(self,v):
        self.values[v] = INITIALELO;

    def update(self, node, score, opp):
        if not self.values.has_key(node):
            self.init_val(node);
            
        self.values[node] = updateElo( self.values[node], score, opp)


#class ChildIter:
#    def __init__(self,board,moves):
#        self.game  = Board();
#        self.game.set(board);
#        mv = [];
#        for moves in moves:
#            mv.append((board,moves))
#        self.moves = mv;
#        self.movesi = 0;
#        
#    def next(self):
#        if not (len(self.moves) - self.movesi):
#            raise StopIteration
#
#        gamep = self.game.clone();
#        t = self.moves[self.movesi];
#        gamep.move(t[0],t[1]);
#
#        out = (self.moves(self.movesi),"%s" % gamep);
#        gamep.takeback();
#
#        self.movesi = self.movesi + 1;
#        
#        return out;


class PGNLoader:

    def __init__(self):
        self.__matcher__ = re.compile("([0-9]*)\\. ([^{} ]*) ([^{} ]*)");
        self.__nmatcher__ = re.compile("\\{.*\\}");

    def load(self, file):
        games = []
        lines = file.readlines()
        lines[-1] = '['
        thisprops = []
        thismoves = []

        inmoves = False;
        for line in lines:

            line = line.strip()
            # blank line, drop ...
            if not len(line):
                continue


            if line[0] == '[':
                if inmoves:
                    try:
                        games.append(self.process(thisprops, thismoves));
                    except KeyboardInterrupt:
                        print "Bailing...."
                        return None
                    except:
                        print "Skipping..."
                    inmoves = 0;
                    thisprops=[];
                    thismoves=[];

                thisprops.append(line);
            else:
                inmoves = 1;
                thismoves.append(line)

        return games

    def process(self, prop, moves):
        print "starting"
        game = self.processMoves(moves)
        mapping = self.processProp(prop)
        print "done"
        return (game,mapping)

    def processMoves(self, moves):
        ml = []
        bigline = reduce( lambda x,y: x+" "+y, moves ).strip()

        game = Game()

        for move in self.__matcher__.findall(bigline):
            game.move( move[1] );
            if move[2]:
                game.move( move[2] );

        return game


    def processProp(self, prop):
        pm = dict();
        for p in prop:
            p = p.strip("[]");
            t = p.split(" ");
            pm[t[0]] = t[1].strip("\"");

        try:

            if( pm["White"] == ME ):
                pm["MyColor"] = 0
                pm["OppRating"] = pm["BlackElo"]
                pm["MyRating"] = pm["WhiteElo"]
            elif( pm["Black"] == ME ):
                pm["MyColor"] = 1
                pm["OppRating"] = pm["WhiteElo"]
                pm["MyRating"] = pm["BlackElo"]

            res = pm["Result"]
            lr = res.split("-");
            if( lr[0] == "1/2" ):
                lr[0] = lr[1] = 0.5;
            pm["Result"] = ( (float(lr[0])- pm["MyColor"] + \
                              pm["MyColor"] - float(lr[1])) + 1)/2.0;

        except:
            raise Error, "Missing Property"

        return pm


    def parseElo(self, whiteElo, whiteName):
        pass

















