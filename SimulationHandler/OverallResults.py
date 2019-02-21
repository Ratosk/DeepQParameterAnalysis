'''
Created on Jul 27, 2018

@author: Alen
'''
from os import listdir
from os.path import isfile, join, abspath
from NNGraphics import NNGraphicPlotter

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
    

def GenerateOverallGraphic( folder = 'Results'):
        files = ls(folder)
        filteredfiles = [ file.split('_')[0:3] for file in files if file.split(".")[-1] == "Stats"]
        
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
                NetDictionary[translate(file[2])] = []
                MaxSpeed[file[1]][translate(file[2])] = 0

                
            Speed = float(file[0])
            
            if Speed > MaxSpeed[file[1]][translate(file[2])]:
                MaxSpeed[file[1]][translate(file[2])] = Speed
            
            if Speed > 55: 
                NetDictionary[file[2]].append( Speed )
            else:
                NetDictionary['Discarted'] += 1
            
        Plotter = NNGraphicPlotter()
            
        for Net in OverallResults:
            
            NetDictionary = OverallResults[Net]

            Plotter.CategoricalPlot(Net,NetDictionary, xlabel='Tipo de entrada', ylabel='Velocidad Millas/h', SaveFileOn = 'Resultados Generales ' + Net, CategoryOrder = ["Posterior","Lateral","Balanceada","Frontal","Control"])
            
            print("Discarted trainings in ", Net,":",NetDictionary['Discarted'])
            
        print(MaxSpeed)


GenerateOverallGraphic()
    