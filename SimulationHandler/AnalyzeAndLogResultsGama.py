'''
Created on Jul 27, 2018

@author: Alen
'''
from os import listdir
from os.path import isfile, join, abspath, isdir
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

def PrintLatexTable(Data,Labels,FileName,SubLabels):
    #|c|c|c|c|
    #\textbf{AlexNet} & \textbf{ResNet} & \textbf{VGG16} & \textbf{VGG19} \\ \hline
    row = Bold('\\#') +' & ' + Bold('Gamma (\\gamma)')
    Structure = '|c|c'
    for label in Labels:
        row += ' & '+Bold(label)
        Structure += '|c'
    row += ' \\\\ \\hline'
    Headers = row
    Structure += '|'
    
    DataLen = len(Data[0])
    Body = ''
    count = 0
    for index in range(DataLen):
        for elem in range(len(Data[0][0])):
            count += 1
            row = Bold(str(count))  +' & ' + str(SubLabels[index])
            for catIndex in range(len(Labels)):
                row += ' & '+str(Data[catIndex][index][elem])
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
    
def lsdirs( ruta = '.'):
    return [arch for arch in listdir(abspath(ruta)) if isdir(join(ruta, arch))]

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

def GenerateOverallGraphic( folder = 'GamaResults', Legend = True, ShowPlot = False):
        gammas = lsdirs(folder)
        filteredfiles = []
        for gamma in gammas:
            files = ls(folder+'/'+gamma)
            filteredfiles += [ file.split(".St")[0].split('_')[0:7] +[gamma] for file in files if file.split(".")[-1] == "Stats"]
        
        OverallResults = {}
        MaxSpeed = {}
        for file in filteredfiles:
            file = [translate(term) for term in file]
            if not file[1] in OverallResults.keys():
                OverallResults[file[1]] = {}
                MaxSpeed[file[1]] = {}
                
            NetDictionary = OverallResults[file[1]]
            
            if not file[7] in NetDictionary.keys():
                NetDictionary[translate(file[7])] = []
                MaxSpeed[file[1]][translate(file[7])] = 0

                
            Speed = float(file[0])
            
            if Speed > MaxSpeed[file[1]][translate(file[7])]:
                MaxSpeed[file[1]][translate(file[7])] = Speed
            
            if Speed > 45 and int(file[5]) > 100000: 
                NetDictionary[file[7]].append( Speed )
                
        Longest = 1000
        #Labels = ['Piramidal', 'Piramidal Invertida', 'Cardinal', 'Cuadrantes']
        Labels = gammas
        Labels = [str(x) for x in Labels]
        for Topology in OverallResults:
            for category in Labels:
                LenCat = len(OverallResults[Topology][category])
                if LenCat < Longest:
                    Longest = LenCat
        
        AllData = []
        OverallLabels = []
        for Topology in OverallResults:
            TempData = []
            OverallLabels.append(Topology)
            
            for category in Labels:
                TempData.append(TrimArrays(OverallResults[Topology][category],Longest))
            pl.rcParams["figure.figsize"] = [16,9]
            pl.boxplot(TempData,labels=Labels)
            index = 0
            for category in Labels:
                Temp = max(OverallResults[Topology][category])
                index += 1
                pl.annotate('Max: ' + str(Temp),
                    xy=(index-0.32, Temp+0.4), xycoords='data')
            pl.ylim(pl.ylim()[0],76)
            pl.xlabel('Valor de Gamma - Número de muestras analizadas por categoría: '+str( Longest))
            pl.ylabel('Velocidad Km/h')
            
            pl.grid(True)
            pl.savefig('ResGamma_'+Topology+'.png')
            
            pl.close()
            AllData.append(TempData)

        PrintLatexTable(AllData,OverallLabels,'Gamma', gammas)
        NetSpeeds = {}
        for gamma in Labels:
            NetSpeeds[gamma] = []
        for elem in AllData:
            count = 0 
            for gamma in Labels:
                NetSpeeds[gamma] = NetSpeeds[gamma] + elem[count]
                count += 1

        Longest = 1000
        TempData = []
        Labels = gammas
        OverallLen = 0
        for category in Labels:
            if len(NetSpeeds[category]) < Longest:
                Longest = len(NetSpeeds[category])
            
        for category in Labels:
            TempData.append(TrimArrays(NetSpeeds[category],Longest))
            OverallLen = Longest
        
        pl.boxplot(TempData,labels=Labels)
        index = 0
        for category in Labels:
            Temp = max(NetSpeeds[category])
            index += 1
            pl.annotate('Max: ' + str(Temp),
                xy=(index-0.32, Temp+0.4), xycoords='data')
        pl.ylim(pl.ylim()[0],76)
        #pl.xlabel('Numero de registros (estado-accion-recompensa) almacenados:'+str( Longest))
        pl.xlabel('Valor de Gamma - Número de muestras analizadas por categoría: '+str(OverallLen))
        pl.ylabel('Velocidad Km/h')
        pl.grid(True)
        
        #pl.title(title+" (Muestras: "+str(len(Alldata))+", Promedio: " +format(sum(Alldata)/len(Alldata), '.2f')+" mph)" )

        #if Legend: pl.legend()

        pl.savefig('ResGammaOverall.png')

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
        pl.ylim(pl.ylim()[0],76)
        pl.xlabel('Estadísticas de los entrenamientos para las diferentes categorías')
        pl.ylabel('Velocidad Km/h')
        pl.grid(True)
        pl.savefig('StatGammaOverall.png')
    
        if ShowPlot: pl.show()
            
        pl.close()
                
                
            


GenerateOverallGraphic()
    