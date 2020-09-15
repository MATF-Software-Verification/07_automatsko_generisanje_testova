#!/usr/bin/python
import os
import subprocess as sp
import sys
import gzip
import json


class Executor:

	tempFolderPath = '';
	srcPath = ''
	elfFile = ''
	extension = ''

	executed_lines = set();
	executed_functions = set();
	total_number_of_lines = -1;
	total_number_of_functions = -1;

	total_number_of_blocks = -1;


	saver = None;
	debugger = None;


	def __init__(self, srcPath, whatToConsider = 'lines', testSaver=None, debugger=None):

		if os.path.exists(srcPath):
			self.srcPath = srcPath;
			self.elfFile, self.extension = self.__getElfName(srcPath)

			#ovde kreiramo jedan tempFolder i svako kreiranje dodatnih fajlova ide u njega
			self.tempFolderPath = self.elfFile + '-temp-dir';

			#ovo proveriti da li cemo ovako
			try:
				os.mkdir(self.elfFile + '-temp-dir')
			except:
				print("Folder already exists")
			#finally:
				#os.rmdir(self.elfFile + '-temp-dir')

			self.whatToConsider = whatToConsider
			self.saver = testSaver;
			self.debugger = debugger;

			self.__compile_program();
		else: print('Neispravna putanja do fajla!', file=sys.stderr);



	#private member methods

	def __compile_program(self):

		self.debugger.write('Compiling program', self.elfFile + self.extension);

		os.system('g++ '  + self.srcPath + ' -fprofile-arcs -ftest-coverage -o '   + self.tempFolderPath + '/' + self.elfFile)

		if os.path.exists(self.tempFolderPath + '/' + self.elfFile):
			pass
		else:
			print('Creating executable file: Failed');

		# os.system('g++ -o ' + '../' + testing_dir + program_name + ' -fprofile-arcs -ftest-coverage ' + dir_path + '/' + testing_dir  + program_name + extension )


	def __getElfName(self, srcPath):

		if srcPath[-2:] == '.c': # c program

			extension = '.c'
			program_name = srcPath[:-2]
		elif srcPath[-4:] in ('.cpp','.c++'):

			extension = '.cpp'
			program_name = srcPath[:-4]
		else:
			print(srcPath)
			print("Extension is not c or c++")
			return -1

		return srcPath[srcPath.rfind('/')+1: srcPath.rfind('.'):], extension;


	def __handle_gcov_data(self, jsonStruct, whatToConsider, testinput):


		lines_count = 0;
		score = 0;
		functions_count = 0;

		if whatToConsider == 'lines':
			for file in jsonStruct['files']:
				lines_count += len(file['lines']);

				if self.total_number_of_lines <= 0:
					self.total_number_of_lines = len(file['lines']);

				for i in range(0, len(file['lines'])):

					if file['lines'][i]['count'] >= 1:
						score += 1

						if not i in self.executed_lines:
							self.saver.save_test_case(testinput);

						self.executed_lines.add(i);

			return score / lines_count

		if whatToConsider == 'functions':
			for file in jsonStruct['files']:
				functions_count += len(file['functions']);

				if self.total_number_of_functions <= 0:
					self.total_number_of_functions = len(file['functions']);

				for i in range(0, len(file['functions'])):

					if file['functions'][i]['execution_count'] >= 1:
						score += 1
						self.executed_functions.add(i)


			return score / functions_count

		if whatToConsider == 'blocks':
			blocks_total = 0
			blocks_executed = 0;

			for file in jsonStruct['files']:
				#functions_count += len(file['functions']);


				for i in range(0, len(file['functions'])):
					blocks_total += file['functions'][i]['blocks'];
					blocks_executed += file['functions'][i]['blocks_executed'];


			if self.total_number_of_blocks == -1:
				self.total_number_of_blocks = blocks_total


			return blocks_executed / blocks_total


		return 0;


	def __execute_test(self, data):

		self.debugger.write('Executing program:' + self.elfFile + ' with input:' + data);
		p_test = sp.Popen(['./' + self.tempFolderPath + '/' + self.elfFile], stdin=sp.PIPE, stdout=sp.PIPE,
						  stderr=sp.PIPE)

		data = bytes(data, 'UTF-8')

		outs, err = p_test.communicate(input=data)
		p_test.kill()

		return 0

	# public member functions

	def get_score(self,testinput):

		self.__execute_test(data=testinput);

		p_gcov = sp.Popen(['gcov', '-bac', '--json', self.elfFile + '.gcda'], stdout=sp.PIPE)

		outs ,_ = p_gcov.communicate()

		p_gcov.kill()

		if os.path.exists(self.elfFile + '.gcda'):
			os.remove(self.elfFile + '.gcda')
		else:
			print('The file ' + self.elfFile + '.gcda' + 'does not exist')


		with gzip.open(self.elfFile + '.gcda'+'.gcov.json.gz', 'rb') as f:
			file_content = f.read()


		if os.path.exists(self.elfFile + '.gcda'+'.gcov.json.gz'):
			os.remove(self.elfFile + '.gcda' + '.gcov.json.gz')
		else:
			print('The file:' + self.elfFile + '.gcda' + '.gcov.json.gz does not exist')

		gcovData = json.loads(file_content);

		return self.__handle_gcov_data(gcovData, self.whatToConsider, testinput);

	def __execute_list_tests(self, test_cases):
		for test in test_cases:
			self.__execute_test(test)

		return 0;

	def __pretty_progress(self, executed_count, total_number):
		length = 80;
		percentage = executed_count/total_number;
		self.debugger.log('Total coverage:[' + '#'*int(length*percentage) + '.'*int(length*(1-percentage)) +']'+ str(percentage*100)+ '%')

	def pretty_progress(self):
		if self.whatToConsider == 'lines':
			self.__pretty_progress(len(self.executed_lines), self.total_number_of_lines)
		if self.whatToConsider == 'functions':
			self.__pretty_progress(len(self.executed_functions),self.total_number_of_functions)

	def is100(self):
		return self.total_number_of_lines == len(self.executed_lines)