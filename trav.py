import sys;
from parse import *

b = PGNLoader();
t = b.load(sys.__stdin__);

print "HI"
f=file('out', 'r')
tree=pickle.load(f)


for k,v in t:
    tree.walk(k,v)








