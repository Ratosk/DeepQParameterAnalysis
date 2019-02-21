'''
Created on Jul 27, 2018

@author: Alen
'''
from os import listdir
from os.path import isfile, join, abspath
import matplotlib.pyplot as pl
import numpy as np
import random
from string import Template

def ls( ruta = '.'):
    return [arch for arch in listdir(abspath(ruta)) if isfile(join(ruta, arch))]

def TrimArrays(x, MaxLength):
    x = sorted(x)
    while(len(x) > MaxLength):
        x.pop(random.randrange(len(x)-1))
    return x

def Bold(string):
    return '\\textbf{'+string+'}'

def PrintLatexTable(Data,Labels,FileName):
    #|c|c|c|c|
    #\textbf{AlexNet} & \textbf{ResNet} & \textbf{VGG16} & \textbf{VGG19} \\ \hline
    row = Bold('\\#')
    Structure = '|c'
    for label in Labels:
        row += ' & '+Bold(label)
        Structure += '|c'
    row += ' \\\\ \\hline'
    Headers = row
    Structure += '|'
    
    row = Bold('#')
    DataLen = len(Data[0])
    Body = ''
    for index in range(DataLen):
        row = Bold(str(index+1))
        for catIndex in range(len(Labels)):
            row += ' & '+str(Data[catIndex][index])
        row += ' \\\\ \\hline \n'
        Body += row
    
    p_file = open(FileName + '_Table.tex', 'w')
    
    d={'Headers':Headers,
        'Body':Body,
        'Structure':Structure,
        }

    #open the file
    filein = open( 'Table.tmpl' )
    #read it
    src = Template( filein.read() )
    #do the substitution
    string = src.substitute(d)
        
    filein.close()
    
    p_file.write(string)
    p_file.close()
    

def translate(term):
    dictionary = {
        'Sides':'Lateral',
        'Behind':'Posterior',
        'Front':'Frontal',
        'Box':'Balanceada',
        'InvPyramid':'Piramidal Invertida',
        'Pyramid':'Piramidal',
        'Quadrants':'Cuadrantes'}
    
    if not term in dictionary.keys():
        return term
    return dictionary[term]
    

def GenerateOverallGraphic( folder = 'TopologyInput', Legend = True, ShowPlot = False):
        files = ls(folder)
        filteredfiles = [ file.split('_')[0:3] for file in files if file.split(".")[-1] == "Stats"]
        
        OverallResults = {}
        MaxSpeed = {}
        for file in filteredfiles:
            file = [translate(term) for term in file]
            if not file[2] in OverallResults.keys():
                OverallResults[file[2]] = {}
                #OverallResults[file[1]]['Discarted'] = 0
                MaxSpeed[file[2]] = {}
                
            NetDictionary = OverallResults[file[2]]
            
            if not file[1] in NetDictionary.keys():
                NetDictionary[translate(file[1])] = []
                MaxSpeed[file[2]][translate(file[1])] = 0

                
            Speed = float(file[0])
            
            if Speed > MaxSpeed[file[2]][translate(file[1])]:
                MaxSpeed[file[2]][translate(file[1])] = Speed
            
            if Speed > 50: 
                NetDictionary[file[1]].append( Speed )
            #else:
                #NetDictionary['Discarted'] += 1
                
                
        Longest = 1000
        Labels = ['Piramidal', 'Piramidal Invertida', 'Cardinal', 'Cuadrantes']
        for Topology in OverallResults:
            for category in Labels:
                LenCat = len(OverallResults[Topology][category])
                if LenCat < Longest:
                    Longest = LenCat
        
        
        for Topology in OverallResults:
            TempData = []
            
            for category in Labels:
                TempData.append(TrimArrays(OverallResults[Topology][category],Longest))
            
            pl.boxplot(TempData,labels=Labels)
            index = 0
            for category in Labels:
                Temp = max(OverallResults[Topology][category])
                index += 1
                pl.annotate('Max:' + str(Temp),
                    xy=(index-0.32, Temp+0.4), xycoords='data')
            pl.ylim(pl.ylim()[0],73)
            pl.xlabel('Número de muestras analizadas por categoría:'+str( Longest))
            pl.ylabel('Velocidad Km/h')
            pl.grid(True)
            pl.savefig('ResInp_'+Topology+'.png')
            pl.close()
            PrintLatexTable(TempData,Labels,'Input_'+Topology)
        
        NetSpeeds = {}
        
        for Net in OverallResults:
            
            NetSpeeds[Net] = []
            
            for Input in OverallResults[Net]:
                
                a = OverallResults[Net][Input]
                
                if not isinstance(a, int):
                    NetSpeeds[Net] = NetSpeeds[Net] + a
        
        Longest = 1000
        TempData = []
        Labels = ['Lateral', 'Posterior', 'Balanceada','Frontal','Control']
        for category in Labels:
            if len(NetSpeeds[category]) < Longest:
                Longest = len(NetSpeeds[category])
            
        for category in Labels:
            TempData.append(TrimArrays(NetSpeeds[category],Longest))
        
        pl.boxplot(TempData,labels=Labels)
        index = 0
        for category in Labels:
            Temp = max(NetSpeeds[category])
            index += 1
            pl.annotate('Max:' + str(Temp),
                xy=(index-0.32, Temp+0.4), xycoords='data')
        pl.ylim(pl.ylim()[0],73)
        pl.xlabel('Numero de muestras analizadas por categoria:'+str( Longest))
        pl.ylabel('Velocidad Km/h')
        pl.grid(True)
        
        #pl.title(title+" (Muestras: "+str(len(Alldata))+", Promedio: " +format(sum(Alldata)/len(Alldata), '.2f')+" mph)" )

        #if Legend: pl.legend()

        pl.savefig('ResInpOverall.png')

        if ShowPlot: pl.show()
        
        pl.close()
        
        from statistics import median, mean
            
        ResultStatistics = []
        for data in TempData:

            ResultStatistics.append([round(mean(data),2),round(median(data),2),round(max(data),2)])
        
        pl.rcParams["figure.figsize"] = [9.6,5.4]
        pl.plot(ResultStatistics)
        pl.xticks(range(len(Labels)), Labels)
        pl.legend(['Promedio', 'Mediana', 'Maximo'],
           shadow=True, loc=(0.05, 0.05), fontsize=12)
        index = 0 
        for category in Labels:
            Xcoord = index -0.1
            Temp = ResultStatistics[index][2]
            pl.annotate(str(Temp),
                xy=(Xcoord, Temp+0.5), xycoords='data')
            Temp = ResultStatistics[index][0]
            pl.annotate(str(Temp),
                xy=(Xcoord, Temp+0.5), xycoords='data')
            Temp = ResultStatistics[index][1]
            pl.annotate(str(Temp),
                xy=(Xcoord, Temp+0.5), xycoords='data')
            index += 1
        pl.ylim(pl.ylim()[0],73)
        pl.xlabel('Estadísticas de los entrenamientos para las diferentes categorías')
        pl.ylabel('Velocidad Km/h')
        pl.grid(True)
        pl.savefig('StatInpOverall.png')
    
        if ShowPlot: pl.show()
            
        pl.close()
            
            
            
        
        
        
        
                
                
            

random.seed(9001)
GenerateOverallGraphic()
    