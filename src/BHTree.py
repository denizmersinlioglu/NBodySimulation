class BHTree:
    # Create and initialize a new bhtree. Initially, all nodes are None and will be filled by recursion
    # Each BHTree represents a quadrant and a body that represents all bodies inside the quadrant
    def __init__(self, quad):
        self.quad = quad     # square region that the tree represents
        self.body = None     # body or aggregate body stored in self node
        self.NW = None       # tree representing northwest quadrant
        self.NE = None       # tree representing northeast quadrant
        self.SW = None       # tree representing southwest quadrant
        self.SE = None       # tree representing southeast quadrant

    # If all nodes of the BHTree are None, then the quadrant represents a single body and it is "external"
    def isExternal(self, tree):
        if tree.NW == None \
                and tree.NE == None \
                and tree.SW == None \
                and tree.SE == None:
            return True
        else:
            return False

    # We have to populate the tree with bodies. We start at the current tree and recursively travel through the branches
    def insert(self, body):
        # If there's not a body there already, put the body there.
        if self.body == None:
            self.body = body

        # If there's already a body there, but it's not an external node
        # combine the two bodies and figure out which quadrant of the
        # tree it should be located in. Then recursively update the nodes below it.
        elif (self.isExternal(self) == False):
            self.body = body.add(self.body)
            northwest = self.quad.NW()
            if (body.inside(northwest)):
                if (self.NW == None):
                    self.NW = BHTree(northwest)
                self.NW.insert(body)
            else:
                northeast = self.quad.NE()
                if (body.inside(northeast)):
                    if (self.NE == None):
                        self.NE = BHTree(northeast)
                    self.NE.insert(body)
                else:
                    southeast = self.quad.SE()
                    if (body.inside(southeast)):
                        if (self.SE == None):
                            self.SE = BHTree(southeast)
                        self.SE.insert(body)
                    else:
                        southwest = self.quad.SW()
                        if(self.SW == None):
                            self.SW = BHTree(southwest)
                        self.SW.insert(body)

        # If the node is external and contains another body, create BHTrees
        # where the bodies should go, update the node, and end
        # (do not do anything recursively)
        elif (self.isExternal(self) == True):
            c = self.body
            northwest = self.quad.NW()
            if (c.inside(northwest)):
                if (self.NW == None):
                    self.NW = BHTree(northwest)
                self.NW.insert(c)
            else:
                northeast = self.quad.NE()
                if (c.inside(northeast)):
                    if (self.NE == None):
                        self.NE = BHTree(northeast)
                    self.NE.insert(c)
                else:
                    southeast = self.quad.SE()
                    if (c.inside(southeast)):
                        if (self.SE == None):
                            self.SE = BHTree(southeast)
                        self.SE.insert(c)
                    else:
                        southwest = self.quad.SW()
                        if(self.SW == None):
                            self.SW = BHTree(southwest)
                        self.SW.insert(c)
            self.insert(body)

    # Start at the main node of the tree. Then, recursively go each branch
    # Until either we reach an external node or we reach a node that is sufficiently
    # far away that the external nodes would not matter much.
    def updateForce(self, body):
        if (self.isExternal(self)):
            if (self.body != body):
                body.addForce(self.body)
        elif self.quad.get_length()/self.body.distanceTo(body) < 2:
            body.addForce(self.body)
        else:
            if (self.NW != None):
                self.NW.updateForce(body)
            if (self.SW != None):
                self.SW.updateForce(body)
            if (self.SE != None):
                self.SE.updateForce(body)
            if (self.NE != None):
                self.NE.updateForce(body)

    # convert to string representation for output
    def toString(self):
        if self.NE != None \
                or self.NW != None \
                or self.SW != None \
                or self.SE != None:
            return "*" + self.body + "\n" + self.NW + self.NE + self.SW + self.SE
        else:
            return " " + self.body + "\n"
