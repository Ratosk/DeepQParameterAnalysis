'''
Created on 10/07/2018

@author: uidv5488
'''
import matplotlib.pyplot as pl
import statistics

class NNGraphicPlotter():
    '''
    classdocs
    '''
    def __init__(self, backend = 'Qt5Agg'):
        '''
        Constructor
        '''
        #pl.switch_backend(backend)

    def Plot(self, title, DataDictionary, xlabel="", ylabel="", grid_visible = True, Legend = True, ShowPlot = False, Color = "", SaveFileOn = "", Iterations = 0):

        MaxLength = 0
        Colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w']
        for Category in DataDictionary:
            if len(DataDictionary[Category]) > MaxLength:
                MaxLength = len(DataDictionary[Category])
        
        if Iterations:
            Xfactor = int(Iterations/MaxLength)
        else:
            Xfactor = 1
        x_axis = list(range(0, Xfactor*MaxLength, Xfactor))
        if len(x_axis) < MaxLength:
            x_axis.append(Iterations)
        Index = 0
        for Category in DataDictionary:
            Data = DataDictionary[Category]
            if Color == "":
                PlotColor = Colors[Index % len(Colors)]
            else:
                PlotColor = Color
            pl.plot(x_axis, Data, PlotColor + "-",label = Category)
            Index+=1

        pl.xlim([0,Iterations])
        pl.xlabel(xlabel)
        pl.ylabel(ylabel)
        pl.grid(grid_visible)
        
        pl.title(title)

        if Legend: pl.legend()

        if SaveFileOn != "":
            pl.savefig(SaveFileOn + ".png")

        if ShowPlot: pl.show()
        
        pl.close()

    def CategoricalPlot(self, title, DataDictionary, xlabel="", ylabel="", grid_visible = True, Legend = False, ShowPlot = False, Color = "", SaveFileOn = "", Iterations = 0, CategoryOrder = None):

        Colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w']

        Index = 0
        Alldata = []
        if not CategoryOrder:
            CategoryOrder = DataDictionary
        
        for Category in CategoryOrder:
            if isinstance(DataDictionary[Category],list):
                Data = DataDictionary[Category]
                Alldata = Alldata + Data
                #enable this with a lot of samples
                #Cat = [Category +'('+format(sum(Data)/len(Data), '.1f')+')' for i in range(len(Data))]
                Cat = [Category for i in range(len(Data))]
                if Color == "":
                    PlotColor = Colors[Index % len(Colors)]
                else:
                    PlotColor = Color
                pl.scatter(Cat, Data)

        pl.ylim(pl.ylim()[0],pl.ylim()[1])
        pl.xlabel(xlabel)
        pl.ylabel(ylabel)
        pl.grid(grid_visible)
        
        pl.title(title+" (Muestras: "+str(len(Alldata))+", Promedio: " +format(sum(Alldata)/len(Alldata), '.2f')+" mph)" )

        if Legend: pl.legend()

        if SaveFileOn != "":
            pl.savefig(SaveFileOn + ".png")

        if ShowPlot: pl.show()
        
        pl.close()
        


    def CategoricalPlotXY(self, title, DataDictionary, xlabel="", ylabel="", grid_visible = True, Legend = False, ShowPlot = False, Color = "", SaveFileOn = "", Iterations = 0, CategoryOrder = None):

        Colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w']

        Index = 0
        Alldata = []
        
        if not CategoryOrder:
            CategoryOrder = DataDictionary
        
        for Category in CategoryOrder:
            if isinstance(DataDictionary[Category],dict):
                
                Data = DataDictionary[Category]
                Alldata = Alldata + Data['Speed']
                #enable this with a lot of samples
                #Cat = [Category +'('+format(sum(Data)/len(Data), '.1f')+')' for i in range(len(Data))]
                pl.plot(Data['Experience'], Data['Speed'])

        pl.ylim(pl.ylim()[0],pl.ylim()[1])
        pl.xlabel(xlabel)
        pl.ylabel(ylabel)
        pl.grid(grid_visible)
        
        pl.title(title+" (Muestras: "+str(len(Alldata))+", Promedio: " +format(sum(Alldata)/len(Alldata), '.2f')+" mph)" )

        if Legend: pl.legend()

        if SaveFileOn != "":
            pl.savefig(SaveFileOn + ".png")

        if ShowPlot: pl.show()
        
        pl.close()
        
    def CategoricalPlotXYDots(self, title, DataDictionary, xlabel="", ylabel="", grid_visible = True, Legend = False, ShowPlot = False, Color = "", SaveFileOn = "", Iterations = 0, CategoryOrder = None):

        Colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w']

        Index = 0
        Alldata = []
        
        if not CategoryOrder:
            CategoryOrder = DataDictionary
        
        for Category in CategoryOrder:
            if isinstance(DataDictionary[Category],dict):
                
                Data = DataDictionary[Category]
                Alldata = Alldata + Data['Speed']
                #enable this with a lot of samples
                #Cat = [Category +'('+format(sum(Data)/len(Data), '.1f')+')' for i in range(len(Data))]
                pl.plot(Data['Experience'], Data['Speed'],'ro')

        pl.ylim(pl.ylim()[0],pl.ylim()[1])
        pl.xlabel(xlabel)
        pl.ylabel(ylabel)
        pl.grid(grid_visible)
        
        pl.title(title+" (Muestras: "+str(len(Alldata))+", Promedio: " +format(sum(Alldata)/len(Alldata), '.2f')+" mph)" )

        if Legend: pl.legend()

        if SaveFileOn != "":
            pl.savefig(SaveFileOn + ".png")

        if ShowPlot: pl.show()
        
        pl.close()

