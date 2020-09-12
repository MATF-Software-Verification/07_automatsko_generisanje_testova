

# Automatic generation of test cases using genetic algorithm


<!---
(c) 2009-2012 Jonathan Turner
(c) 2009-2017 Jason Turner

Release under the BSD license, see "license.txt" for details.
--->

### Introduction

AGTGA represents tool written in python that tries to generate collection of test inputs that have full coverage of source code. It relies on the implementation of genetic algorithm.  


### Requirements

Python interpreter

g++/gcc - GNU project C and C++ compiler

gcov - coverage testing tool

termcolor 1.1.0 
### Usage
First, you need to define parameters for genetic algorithm in file conf.json (see Description for details).

Start a program with:

	make run



### Description
Configuration file consists of the following parameters:

srcPath - the absolute or relative path to the source file that is being executed

populationSize - maximum number of chromosomes (test inputs) in each generation

chromosomeSize - length of each chromosomes

parentsNumber - number of chromosome needed to make crossover

generationsCount - number of iterations in evolution of genetic algorithm

whatToConsider - one of the possible values ['lines', 'functions', 'branches']. 

	'lines': -if selected, score for each test input depends on number of lines executed

	'functions':- if selected, score for each test input depends on number of functions called

	'brances':- if selected, score for each test input depends on number of brances taken 

showIterations - display evolution progress on screen

debug - display additional information about steps in evolution process

geneTypeList - represents list of types of characters that is considered in making chromosome. It can have following values ["digits", "alpha", "ALPHA","whitespace", "punctuation"].


Conf.file example:
```python
{
	"srcPath": "test/test.cpp",
	"populationSize": 3,
	"chromosomeSize": 3,
	"parentsNumber": 2,
	"mutationRate": 0.8,
	"generationsCount": 8,
	"whatToConsider": "lines",
	"showIterations": true,
	"debug": false,
	"geneTypeList": ["digits"]

}
 
```
