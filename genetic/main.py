from genetic import Genetic
from configuration import Configuration
from executor import Executor
from testsaver import TestSaver
from debugger import Debug


def main():

    C = Configuration('conf.json')

    debug = Debug(debug=C.debug, info=C.showInfo)

    saver = TestSaver('out.txt')
    executorObject = Executor(srcPath=C.srcPath, testSaver=saver, debugger = debug);

    geneticObject = Genetic(populationSize=C.populationSize,  # Population pop_size
              chromosomeSize=C.chromosomeSize,  # size of chromosome (can be bytes, size of a number, size of a string...)
              parentsNumber=C.parentsNumber,  # How many chromosomes are entering crossover
              mutationRate=C.mutationRate,  # selfexplanatory
              generationsCount=C.generationsCount,  # Number of generations (iterations)
              geneTypeList=C.geneTypeList, #list of
              executor=executorObject,
              debugger=debug)

    geneticObject.start_evolution();

    saver.export_to_file()

    return 0;

main()