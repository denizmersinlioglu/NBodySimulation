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
    def is_external(self, tree):
        return tree.NW is None \
            and tree.NE is None \
            and tree.SW is None \
            and tree.SE is None

    # We have to populate the tree with bodies. We start at the current tree and recursively travel through the branches
    def insert(self, body):
        # If there's not a body there already, put the body there.
        if self.body is None:
            self.body = body

        # If there's already a body there, but it's not an external node
        # combine the two bodies and figure out which quadrant of the
        # tree it should be located in. Then recursively update the nodes below it.
        elif not self.is_external(self):
            self.body = body.add(self.body)
            northwest = self.quad.NW()
            if body.inside(northwest):
                if self.NW is None:
                    self.NW = BHTree(northwest)
                self.NW.insert(body)
            else:
                northeast = self.quad.NE()
                if body.inside(northeast):
                    if self.NE is None:
                        self.NE = BHTree(northeast)
                    self.NE.insert(body)
                else:
                    southeast = self.quad.SE()
                    if body.inside(southeast):
                        if self.SE is None:
                            self.SE = BHTree(southeast)
                        self.SE.insert(body)
                    else:
                        southwest = self.quad.SW()
                        if(self.SW is None):
                            self.SW = BHTree(southwest)
                        self.SW.insert(body)

        # If the node is external and contains another body, create BHTrees
        # where the bodies should go, update the node, and end
        # (do not do anything recursively)
        elif self.is_external(self):
            c = self.body
            northwest = self.quad.NW()
            if c.inside(northwest):
                if self.NW is None:
                    self.NW = BHTree(northwest)
                self.NW.insert(c)
            else:
                northeast = self.quad.NE()
                if c.inside(northeast):
                    if self.NE is None:
                        self.NE = BHTree(northeast)
                    self.NE.insert(c)
                else:
                    southeast = self.quad.SE()
                    if c.inside(southeast):
                        if self.SE is None:
                            self.SE = BHTree(southeast)
                        self.SE.insert(c)
                    else:
                        southwest = self.quad.SW()
                        if self.SW is None:
                            self.SW = BHTree(southwest)
                        self.SW.insert(c)
            self.insert(body)

    # Start at the main node of the tree. Then, recursively go each branch
    # Until either we reach an external node or we reach a node that is sufficiently
    # far away that the external nodes would not matter much.
    def update_force(self, body):
        if self.is_external(self):
            if self.body != body:
                body.addForce(self.body)
        elif self.quad.get_length()/self.body.distanceTo(body) < 2:
            body.addForce(self.body)
        else:
            if self.NW is not None:
                self.NW.update_force(body)
            if self.SW is not None:
                self.SW.update_force(body)
            if self.SE is not None:
                self.SE.update_force(body)
            if self.NE is not None:
                self.NE.update_force(body)

    # convert to string representation for output
    def to_string(self):
        if self.NE is not None \
                or self.NW is not None \
                or self.SW is not None \
                or self.SE is not None:
            return "*" + self.body + "\n" + self.NW + self.NE + self.SW + self.SE

        return " " + self.body + "\n"
