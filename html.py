import sys;
from parse import *

template = None;
white = None;
black = None;
tree = None;
count = 0;
span_html = "<span class=\"%s\">%s</span>"
span_str = ["white_sq","black_sq"]
unicode_pieces=dict(
    zip("KQRBNPkqrbnp",
        ("&#x%x;" % uc for uc in range(0x2654, 0x2660))))

def init():
    f=file('out', 'r')

    tree=pickle.load(f)
    f.close()

    white = tree.getwhiteroot()
    black = tree.getblackroot()

    templatefi = open("template.html",'r')
    template = templatefi.read();
    templatefi.close()

def node_str(node):
    posasstring = str(node).replace(" ","");
    return posasstring[:-2];

def node_filename(node):
    filename = "/home/dfb/.www/chess/%s.html"%str(node).replace(" ","");
    return filename

def node_url(node):
    filename = "%s.html"%str(node).replace(" ","");
    return filename



def increment_count():
    if count %100:
        print "Done with %d positions" % count;
    count += 1;    


def go(node,parenthtml,depth=0):

    increment_count();

    posasstring = node_str(node)

    blob = ''
    for i in range(len(posasstring)):
        span_color = span_str[(((i/8)%2)+i)%2]
        
        char_v =  posasstring[i];
        piece_v = ''

        if char_v == '.':
            piece_v = ' '
        else:
            piece_v = unicode_pieces[char_v]
        span = span_html % (span_color,piece_v)

        if i%8 == 7:
            span = "%s%s" % (span,"\n<br>")

            
        blob="%s%s"%(blob,span);

    linkblob = ''

    children = list(node.children)
    children = map(  lambda x: (tree.getnode(x[0]),x[1]),node.children )

    children.sort( lambda x,y: int(x[0].all-y[0].all) )

    for childnode,cm in children:
        childfiname = node_url(childnode)
        link = '<a href="%s">%s</a>%s, %s/%s<br>' % (childfiname, cm ,childnode.all, childnode.gameswon, childnode.gamesplayed)
        linkblob += link

    filename =  node_filename(node);
    fi = open(filename,'w')
    fi.write(template % (blob,linkblob))
    fi.close()

    for mv,cm in node.children:
        childnode = tree.getnode(str(mv))
        go(childnode,filename,depth+1);

go(white,None)
go(black,None)
