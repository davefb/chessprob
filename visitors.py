class visitor:
    """ generalization of the visitor pattern to
    chain several visitors """
    
    def __init__(self, visitorlist = None):
        self.nextvisitors = visitorlist;

    def addvisitor(self, visitor):
        self.nextvisitors.append(visitor)

    def visit(self, visiting, payload = None):
        throw Exception("This method must be overridden");

    def finalize(self, visiting, payload):
        """ called after the dispatch """
        pass
    
    def dispatch(self, visiting, payload):
        """ dispatches the visitor to the children """
        payload.append( self )
        for nv in self.nextvisitors:
            nv.visit( visiting, payload )
        self.finalize( visiting, payload )
        

class depthvisitor(visitor):
    def __init__(self):
        visitor.__init__(self)
        self.depth = 0;
        
    def visit(self, visiting, payload = None):
        dispatch(visiting, payload);






