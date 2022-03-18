class fixture(object):
    def __init__(self, startChannel, channelsNeeded, RGBA, name):
        self.rgba = RGBA
        self.name = name
        self.channelsneeded = channelsNeeded
        self.occupiedChannels = [startChannel]
        for channels in range(channelsNeeded):
            self.occupiedChannels.append(channels+1)
        self.color = (255,255,255,255)
    
    def updateColor(self, newColor):
        self.color = newColor
    
    def updatePatch(self, startChannel, channelsNeeded, RGBA):
        self.occupiedChannels = [startChannel]
        self.rgba = RGBA
        for channels in range(channelsNeeded):
            self.occupiedChannels.append(channels+1)
    
    def getChans(self):
        return self.occupiedChannels()

    def rename(self, newName):
        self.name = newName
