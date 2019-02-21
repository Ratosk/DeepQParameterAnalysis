'''
Created on Jul 9, 2018

@author: Alen
'''
from selenium import webdriver
from time import sleep, strftime, localtime, time
from string import Template
from NNGraphics import NNGraphicPlotter
import pyperclip, pickle, os, pyautogui, threading
from copy import copy

class SimulationHandler():
    '''
    classdocs
    '''
    
    def __init__(self, OpenWebInstance = True):
        '''
        Constructor
        '''
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        prefs = {'download.default_directory' : '/path/to/dir'}
        options.add_experimental_option('prefs', prefs)
                
        # Using Chrome to access web
        if OpenWebInstance:
            self.browser = webdriver.Chrome(chrome_options=options)
            self.browser.get('https://selfdrivingcars.mit.edu/deeptraffic/')
        else:
            self.browser = None
        self.Statistics = {'speed':[],'cars passed':[]}
        self.SetParameters = False
        self.FileName = ""
        self.WorkSpacePath = "Results\\"
        self.WorkSpacePath = os.path.abspath(self.WorkSpacePath)+'\\'
        self.PrepareWorkSpace()
        self.Plotter = NNGraphicPlotter()
        self.AvgSpeed=0.0    
        self.timeString = 'NoTimeStamp'
        self.NetTopologyDictionary ={ 
            'Pyramid':"Pyramid.NNet",
            'InvPyramid':"InvPyramid.NNet",
            'Quadrants':"Quadrants.NNet",
            'Cardinal':"Cardinal.NNet"#,
            #'Control':"Control.NNet",
            }
        self.NetInputTypes={ 
            'Box':[3,10,12], #lanesSide, patchesAhead, patchesBehind
            'Behind':[3,2,18], #lanesSide, patchesAhead, patchesBehind
            'Front':[1,40,10], #lanesSide, patchesAhead, patchesBehind
            'Sides':[6,5,7], #lanesSide, patchesAhead, patchesBehind
            'Control':[3,50,10] #lanesSide, patchesAhead, patchesBehind
            }
        
    def __del__(self):
        try:
            #self.SaveModel()
            pass
        except:
            pass
        try:
            #self.SaveStatistics()
            pass
        except:
            pass
        pass
    
    def PrepareWorkSpace(self):
        try:
            os.makedirs(self.WorkSpacePath)  
        except:
            #print("INFO > Working directory already exists!")  
            pass
    
    def SaveModel(self): #TODO save the info on a specific file path and name
        self.browser.minimize_window()
        self.browser.maximize_window()
        sleep(1.5)
        if self.FileName != "":
            webButton = self.browser.find_element_by_id("downloadCodeButton")
            webButton.click()
            sleep(1)
            #webButton.send_keys(self.WorkSpacePath+self.FileName + ".netInfo")
            pyautogui.typewrite(self.WorkSpacePath+self.FileName + ".netInfo")
            pyautogui.hotkey('enter')
            pyautogui.hotkey('y')
            
        else:
            print("ERROR > Execute a training first, before of save the model.")
    
    def LoadCode(self):
        
        str_code = self.GenerateCode()
        
        code = self.browser.find_element_by_class_name('view-lines')
        
        pyautogui.moveTo(code.location['x']*2, code.location['y']*2)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'x')
        #spam = pyperclip.paste()
        pyperclip.copy(str_code)
        #print(spam)
        pyautogui.hotkey('ctrl', 'v')
        
    def SetExperimentParameters(self, NetName, NetInputType , learning_rate=0.001, batch_size=64, iterations=10000, otherAgents = 0, experience_size = 3000, temporalWindow = 0):
        self.iterations = iterations
        self.LoadNetInput(NetInputType)
        self.otherAgents = otherAgents
        self.experience_size = experience_size
        self.NetName = NetName
        self.NetInputType = NetInputType
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.Temporal_Window = temporalWindow
        
        self.SetParameters = True
        
    def LoadNetInput(self,NetInputType):
        self.lanesSide = self.NetInputTypes[NetInputType][0]
        self.patchesAhead = self.NetInputTypes[NetInputType][1]
        self.patchesBehind = self.NetInputTypes[NetInputType][2]
        
    def GenerateCode(self):
        
        if not self.SetParameters:
            raise("The parameters for the experiment should be set before of generate the code")
        
        d={ 'trainIterations':str(self.iterations),
            'experience_size':str(self.experience_size),
            'hiddenlayers':str(self.LoadNetCode()),
            'otherAgents':str(self.otherAgents),
            'lanesSide':str(self.lanesSide),
            'patchesAhead':str(self.patchesAhead),
            'patchesBehind':str(self.patchesBehind),
            'learning_rate':str(self.learning_rate),
            'batch_size':str(self.batch_size),
            'TemporalWindow':str(self.Temporal_Window)
            }

        #open the file
        filein = open( 'Code.tmpl' )
        #read it
        src = Template( filein.read() )
        #do the substitution
        string = src.substitute(d)
        
        filein.close()
        
        return string
    
    def LoadNetCode(self):
        fileName = self.NetTopologyDictionary[self.NetName]
        
        p_file = open(fileName, 'r')
        lines = p_file.readlines()
        p_file.close()
        
        return "".join(lines)
    
    def GetStatistics(self, SampleDelay = 5): #TODO add the reward info to the graphics create individual graphics and store the graphics for each execution.
        TrainingFinished = False
        print('Starting data recollection...')
        mphSamples = []
        passedSamples = []
        while not (TrainingFinished):
            try:
                mphSamples.append(float(self.browser.find_element_by_id('mph').text))
                passedSamples.append(int(self.browser.find_element_by_id('passed').text))
            except:
                print('ERROR > During sample recollection.')
                pass
            
            try:
                TrainingOK = self.browser.find_element_by_class_name("confirm")
                TrainingFinished = True
            except:
                pass
            
            sleep(SampleDelay)
        print('Training Finished!')
        TrainingOK.click()
        
        self.Statistics = {'Velocidad MpH':mphSamples,'Coches Pasados':passedSamples}
        
        self.CalculateAverages()
                        
    def SaveStatistics(self): 
        self.FileName = str(self.AvgSpeed)+'_'+self.NetName + "_" + self.NetInputType + "_" + self.timeString + "_" + str(self.iterations)
        with open(self.WorkSpacePath+self.FileName + ".Stats", 'wb') as outputFile:
            pickle.dump(self.Statistics, outputFile, pickle.HIGHEST_PROTOCOL)
            
    def CalculateAverages(self):
        Temp = []
        for Category in self.Statistics:
            Avg = 0
            Count = 0
            SampleList = []            
            for sample in self.Statistics[Category]:
                Avg += sample
                Count +=1
                SampleList.append(Avg/Count)
            Temp.append(copy(SampleList))
        
        self.Statistics['Promedio - Velocidad MpH'] = copy(Temp[1])
        self.Statistics['Promedio - Coches Pasados'] = copy(Temp[0])
            
    def LoadStatistics(self, filename = None): 
        if not filename:
            filename = self.WorkSpacePath + self.FileName + ".Stats"
        with open(filename, 'rb') as inputFile:
            data = pickle.load(inputFile)
            #print(data)
            del self.Statistics
            self.Statistics = data
    
    def GenerateGraphics(self):

        filename = self.WorkSpacePath + self.FileName
        plotTitle = 'Red:'+ self.NetName + '- Entrada:'+self.NetInputType+" - Velocidad Promedio:"+str(self.AvgSpeed)
        self.Plotter.Plot(plotTitle, self.Statistics, xlabel='Iteraciones('+str(self.iterations)+')', ylabel='Valores', SaveFileOn = filename, Iterations = self.iterations)
        for Category in self.Statistics:
            d = {Category:self.Statistics[Category]}
            try:
                self.Plotter.Plot(plotTitle, d, xlabel='Iteraciones', ylabel=Category, SaveFileOn = (filename+"_"+Category), Iterations = self.iterations)
            except:
                print("ERROR > Exception detected at plotting of data experiment:", self.FileName)
                pass
        pass
    
    def ReportStatistics(self): #TODO
        pass #Store the statistics of the experiment on a center file.
    
    def RunTraining(self): #TODO Decide a better filename to arrange better the files for future analysis
        TrainingOK = self.browser.find_element_by_id("trainButton")
        TrainingOK.click()
        self.timeString  = strftime("%Y%m%d_%H%M%S", localtime())
                
    def EvalModel(self,SampleDelay = 2):
        sleep(1)
        StartEvaluation = self.browser.find_element_by_id("evalButton")
        StartEvaluation.click()
        print('Evaluation Started!')
        EvaluationFinished = False
        while not (EvaluationFinished):
            try:
                p_elements = self.browser.find_elements_by_css_selector("p")
                for element in p_elements:
                    if element.text.find("Average speed") != -1:
                        TextBox = element.text
                        EvaluationFinished = True
                        break
            except:
                pass
            
            sleep(SampleDelay)
        print('Evaluation Finished!')#TODO get average info
        
        self.AvgSpeed = float(TextBox.split(": ")[-1].split("m")[0].strip())
        EvaluationOK = self.browser.find_element_by_class_name("confirm")
        EvaluationOK.click()
        pass
    
    def ApplyCodeAndResetNet(self):
        webButton = self.browser.find_element_by_css_selector("button.button-small")
        webButton.click()
        pass
        
    def Close(self):
        if self.browser:
            self.browser.close()
        
    def RunExperiment(self):
        print('Running Experiment for Net:', self.NetName , ', InputType:',self.NetInputType)
    
        self.ApplyCodeAndResetNet()
        
        TrainingTime = time()
        self.RunTraining()
        TrainingTime = time()-TrainingTime
        print("Training completed in:",int(TrainingTime/60)+1,"Minutes")
        
        self.GetStatistics()
        
        self.EvalModel()
        
        self.SaveStatistics()
        
    def FinishExperiment(self):
        
        self.SaveModel()
        
        self.GenerateGraphics()
        
        #self.LoadStatistics()
        
        self.Close()

Sim = SimulationHandler(OpenWebInstance = False)

NetTopologyDictionary = copy(Sim.NetTopologyDictionary)
NetInputTypes = copy(Sim.NetInputTypes)

Sim.Close()

Simulations = {}

SimThreads = []

Trainings = 3

for index in range(Trainings):
    print("Starting Training for all nets:",index+1,"/",Trainings)
    
    for Net in NetTopologyDictionary:
        Simulations[Net] = {}
        for InputType in Sim.NetInputTypes:
            Simulations[Net][InputType] = SimulationHandler()
            
            Simulations[Net][InputType].SetExperimentParameters(Net,InputType,iterations=100000,experience_size = 3000)
            
            Simulations[Net][InputType].LoadCode()
            
        for InputType in NetInputTypes:
            
            while(len(SimThreads)>4):
                #print("Waiting") 
                sleep(1)
                for thread in SimThreads:
                    if not thread.isAlive():
                        break
                if not thread.isAlive():
                        SimThreads.remove(thread)  
            
            t = threading.Thread(target=Simulations[Net][InputType].RunExperiment, name=Simulations[Net][InputType].FileName)
            SimThreads.append(t)
            t.setDaemon(True)
            t.start()
            
        while(len(SimThreads)>0):
                #print("Waiting") 
                sleep(1)
                for thread in SimThreads:
                    if not thread.isAlive():
                        break
                if not thread.isAlive():
                        SimThreads.remove(thread)
            
        for InputType in NetInputTypes:
            
            Simulations[Net][InputType].FinishExperiment()
    
    print("Finishing Training for all nets:",index+1,"/",Trainings)
    


#Turn Off the computer when finish!
print("The machine will be turned off in 1 minute")
#os.system('shutdown -s')


