
import sys
import json

"""
Class represent configuration of genetic algorithm
it gets parameters from json file  

"""


class Configuration:

    def __init__(self, jsonPath):

        if jsonPath == 'conf.json':

            file = open(jsonPath, "r")
            jsonData = json.loads(file.read());
            file.close();

            self.srcPath = jsonData['srcPath'];
            self.populationSize = jsonData['populationSize'];
            self.chromosomeSize = jsonData['chromosomeSize'];
            self.parentsNumber = jsonData['parentsNumber'];
            self.mutationRate = jsonData['mutationRate'];
            self.generationsCount = jsonData['generationsCount'];
            self.geneTypeList = jsonData['geneTypeList'];
            self.whatToConsider = jsonData['whatToConsider'];
            self.debug = jsonData['debug'];
            self.showInfo = jsonData['showInfo'];
        else:
            print('conf.json not found', file=sys.stderr);

