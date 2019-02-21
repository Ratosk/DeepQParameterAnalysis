from NNGraphics import NNGraphicPlotter

inputFile = open("Log.txt","r")

timeArray = []
lossArray = []
valLossArray = []


for line in inputFile:

    if " - loss: " in line :

        line = line.strip()
        line = line.replace("-","")
        line = line.replace(" ","")

        firstSplit = line.split("s",1)

        time = int(firstSplit[0])

        secondSplit = firstSplit[1].split(":")
        loss = float(secondSplit[1].split("v")[0])
        val_loss = float(secondSplit[2])

        timeArray.append(time)
        lossArray.append(loss)
        valLossArray.append(val_loss)


inputFile.close()

Plotter = NNGraphicPlotter()

dict = {"Error in Test Set":lossArray, "Error in Validation set":valLossArray}

Plotter.Plot(dict, xlabel='Number of Epochs', ylabel='Mean Square Error', SaveFileOn = "Test")

