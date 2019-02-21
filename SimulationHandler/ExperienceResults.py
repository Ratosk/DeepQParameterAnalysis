'''
Created on Jul 27, 2018

@author: Alen
'''
from os import listdir
from os.path import isfile, join, abspath
from NNGraphics import NNGraphicPlotter
from copy import deepcopy

def ls( ruta = '.'):
    return [arch for arch in listdir(abspath(ruta)) if isfile(join(ruta, arch))]

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

def F_SortedExperience(data):
    print(data[0])
    return data[0]+data[1]
    

def GenerateOverallGraphic( folder = 'Results'):
        files = ls(folder)
        filteredfiles = [ (file.split(".Sta")[0]).split('_')[0:7] for file in files if file.split(".")[-1] == "Stats"]
        
        OverallResults = {}
        MaxSpeed = {}
        for file in filteredfiles:
            file = [translate(term) for term in file]
            if not file[1] in OverallResults.keys():
                OverallResults[file[1]] = {}
                OverallResults[file[1]]['Discarted'] = 0
                MaxSpeed[file[1]] = {}
                
            NetDictionary = OverallResults[file[1]]
            
            if not file[2] in NetDictionary.keys():
                #NetDictionary[translate(file[2])] = {'Speed':[],'Experience':[]}
                NetDictionary[translate(file[2])] = []
                MaxSpeed[file[1]][translate(file[2])] = 0

                
            Speed = float(file[0])
            Experience = int(file[-1])
            
            if Speed > MaxSpeed[file[1]][translate(file[2])]:
                MaxSpeed[file[1]][translate(file[2])] = Speed
            
            if Speed > 60: 
                #NetDictionary[file[2]]['Speed'].append( Speed )
                #NetDictionary[file[2]]['Experience'].append( Experience )
                NetDictionary[file[2]].append([Experience, Speed])
                
            else:
                NetDictionary['Discarted'] += 1
                
        for Net in OverallResults: 
            NetDictionary = OverallResults[Net]
            
            for Category in NetDictionary:
                if Category != 'Discarted': 

                    Data = sorted(NetDictionary[Category], key=F_SortedExperience)
                    print(NetDictionary[Category])
                    NetDictionary[Category] = {'Speed':[],'Experience':[]}
                    
                    for elem in Data:
                        NetDictionary[Category]['Speed'].append(elem[1])
                        NetDictionary[Category]['Experience'].append(elem[0])
            
        Plotter = NNGraphicPlotter()
            
        for Net in OverallResults:
            
            NetDictionary = OverallResults[Net]

            Plotter.CategoricalPlotXY(Net,NetDictionary, xlabel='Tamaño de la Experiencia', ylabel='Velocidad Millas/h', SaveFileOn = 'Resultados Generales ' + Net, CategoryOrder = ["Posterior","Lateral","Balanceada","Frontal","Control"])
            
            print("Discarted trainings in ", Net,":",NetDictionary['Discarted'])
            
        print(MaxSpeed)
        
        for Net in OverallResults: 
            NetDictionary = OverallResults[Net]
            
            for Category in NetDictionary:
                if Category != 'Discarted': 

                    Data = sorted(NetDictionary[Category], key=F_SortedExperience)
                    print(NetDictionary[Category])
                    NetDictionary[Category] = {'Speed':[],'Experience':[]}
                    
                    for elem in Data:
                        NetDictionary[Category]['Speed'].append(elem[1])
                        NetDictionary[Category]['Experience'].append(elem[0])
            
        Plotter = NNGraphicPlotter()
        
        
        '''-------------------------------------------------------------'''
            
        for Net in OverallResults:
            
            NetDictionary = OverallResults[Net]

            Plotter.CategoricalPlotXY(Net,NetDictionary, xlabel='Tamaño de la Experiencia', ylabel='Velocidad Millas/h', SaveFileOn = 'Resultados Generales ' + Net, CategoryOrder = ["Posterior","Lateral","Balanceada","Frontal","Control"])
            
            print("Discarted trainings in ", Net,":",NetDictionary['Discarted'])
            
        print(MaxSpeed)


GenerateOverallGraphic()
    