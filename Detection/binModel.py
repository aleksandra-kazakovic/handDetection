import Configurations.helper as helper

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Compartment:
    def __init__(self, upperLeft, downRight):
        self.upperLeft = upperLeft
        self.downRight = downRight

class Bin:
    def __init__(self, typeOfBin):
        config = helper.read_bin_config()
        self.typeOfBin = typeOfBin
        self.nRows = int(config[str(typeOfBin)]['nRows'])
        self.nCols = int(config[str(typeOfBin)]['nCols'])
        self.height = int(config['BinConfig']['binHeight'])
        self.width = int(config['BinConfig']['binWidth'])
        self.startX = int(config['BinConfig']['binStartX'])
        self.startY = int(config['BinConfig']['binStartY'])

        self.compartments = []

        deltaX = self.width / self.nCols
        deltaY = self.height / self.nRows

        for i in range(self.nRows):
            for j in range(self.nCols):
                upperLeft = Dot(int(j*deltaX)+self.startX , int(i*deltaY)+self.startY)
                downRight = Dot(int((j+1)*deltaX)+self.startX, int((i+1)*deltaY)+self.startY)
                compartment = Compartment(upperLeft, downRight)
                self.compartments.append(compartment)

    def getRequestedCompartment(self, requestedCompartment):
        return self.compartments[requestedCompartment-1]
    
    def getCompartmentNumberUsingTheCoordinates(self, x, y):
        for index, compartment in enumerate(self.compartments):
            if x > compartment.upperLeft.x and x < compartment.downRight.x and y > compartment.upperLeft.y and y < compartment.downRight.y:
                return index+1
        return -1
