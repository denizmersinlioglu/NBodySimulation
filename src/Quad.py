class Quad:

    def __init__(self, xmid, ymid, length):
        self.xmid = xmid
        self.ymid = ymid
        self.length = length

    def get_length(self):
        return self.length

    def NW(self):
        return Quad(self.xmid-self.length/4.0, self.ymid+self.length/4.0, self.length/2.0)

    def NE(self):
        return Quad(self.xmid+self.length/4.0, self.ymid+self.length/4.0, self.length/2.0)

    def SW(self):
        return Quad(self.xmid-self.length/4.0, self.ymid-self.length/4.0, self.length/2.0)

    def SE(self):
        return Quad(self.xmid+self.length/4.0, self.ymid-self.length/4.0, self.length/2.0)

    def contains(self, xmid, ymid):
        return xmid <= self.xmid+self.length/2.0 \
            and xmid >= self.xmid-self.length/2.0 \
            and ymid <= self.ymid+self.length/2.0  \
            and ymid >= self.ymid-self.length/2.0
