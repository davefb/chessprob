import sys;
from parse import *

b = PGNLoader();
t = b.load(sys.__stdin__);

tree = ChessTree();
f=file('out', 'w')

for k,v in t:
    tree.addGame(k,v)

pickle.dump(tree,f)






