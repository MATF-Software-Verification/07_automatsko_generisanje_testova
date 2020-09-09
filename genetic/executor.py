#!/usr/bin/python
import os
import subprocess as sp
import sys
import gzip
import json


DEBUG = 0

"""
To get file coverage we first call compiler with follwoing commands
	1) Compile program for coverage - g++ -o test	-fprofile-arcs -ftest-coverage test.cpp  
	2) Run program with given tests
	3) Calculate coverage gcov test.cpp
	4) Read retunred values
"""
class Executor:

	tempFolderPath = '';
	srcPath = ''
	elfFile = ''
	extension = ''

	executed_lines = set();
	executed_functions = set();
	total_number_of_lines = -1;
	total_number_of_functions = -1;

	saver = None;

	def __init__(self, srcPath, testSaver=None):

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

			self.saver = testSaver;

			self.__compile_program();
		else: print('Neispravna putanja do fajla!', file=sys.stderr);



	#private member methods

	def __compile_program(self):
		"""
		Parsing program
		"""

		#print('g++ '  + self.elfFile + self.extension + ' -fprofile-arcs -ftest-coverage -o '   + self.tempFolderPath + '/' + self.elfFile)

		#ovde ustekati provere da li je ovo proslo sve kako treba itd itd...
		os.system('g++ '  + self.srcPath + ' -fprofile-arcs -ftest-coverage -o '   + self.tempFolderPath + '/' + self.elfFile)

		if os.path.exists(self.tempFolderPath + '/' + self.elfFile):
			pass
		else:
			print('Creating executable file: Failed');

		# os.system('g++ -o ' + '../' + testing_dir + program_name + ' -fprofile-arcs -ftest-coverage ' + dir_path + '/' + testing_dir  + program_name + extension )


	def __getElfName(self, srcPath):

		if srcPath[-2:] == '.c': # c program
			#print("Working with C")
			extension = '.c'
			program_name = srcPath[:-2]
		elif srcPath[-4:] in ('.cpp','.c++'):
			#print("Working with c++")
			extension = '.cpp'
			program_name = srcPath[:-4] # cutting off extension
		else:
			print(srcPath)
			print("Extension is not c or c++")
			return -1
		# data = bytes(program_data[0],'UTF-8')
		return srcPath[srcPath.rfind('/')+1: srcPath.rfind('.'):], extension;


	def __handle_gcov_data(self, jsonStruct, whatToConsider, testinput):

		#print(testinput)
		lines_count = 0;
		score = 0;
		functions_count = 0;

		if whatToConsider == 'lines':
			for file in jsonStruct['files']:
				lines_count += len(file['lines']); #mozda ovde neka provera da li postoji lines i sl.

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
				functions_count += len(file['lines']);

				if self.total_number_of_functions <= 0:
					self.total_number_of_functions = len(file['functions']);

				for i in range(0, len(file['lines'])):

					if file['functions'][i]['count'] >= 1:
						score += 1
						self.executed_functions.add(i)
			return score / functions_count



		return 0;


	def __execute_test(self, data):

		# print('Executing program', program_name);
		p_test = sp.Popen(['./' + self.tempFolderPath + '/' + self.elfFile], stdin=sp.PIPE, stdout=sp.PIPE,
						  stderr=sp.PIPE)

		data = bytes(data, 'UTF-8')

		outs, err = p_test.communicate(input=data)
		p_test.kill()
		if DEBUG:
			print("Debug: return stdout:", outs.decode("utf-8"), file=sys.stderr)
			print("Debug: return err:", err.decode("utf-8"), file=sys.stderr)
			print("Debug: return code:", p_test.returncode, file=sys.stderr)

		# print(outs);

		# We slice string by new line, since output is always same for gcov, we can hardcode numbers
		# We perform 2 slices ( 3 list elements) and we are intereseted in 2nd element, and then we split by : so we just get number of %
		# Possible hack
		# extracted_data = outs.decode('UTF-8').split('\n',2)[1].split(':')[1].split(' ',1)[0][:-1]

		return 0

	# public member functions

	def get_score(self,testinput):

		self.__execute_test(data=testinput);

		p_gcov = sp.Popen(['gcov', '--json', self.elfFile + '.gcda'], stdout=sp.PIPE)

		outs ,_ = p_gcov.communicate()
		if DEBUG:
			#outs, _ = p_gcov.communicate()
			print("Debug: return stdout:", outs.decode('UTF-8'),file=sys.stderr)
		p_gcov.kill()

		if os.path.exists(self.elfFile + '.gcda'):
			os.remove(self.elfFile + '.gcda')
		else:
			print('The file ' + self.elfFile + '.gcda' + 'does not exist')


		with gzip.open(self.elfFile + '.gcda'+'.gcov.json.gz', 'rb') as f:
			file_content = f.read()
		#
		# if os.path.exists('test.gcno'):
		# 	os.remove('test.gcno')
		# else:
		# 	print("The file test.gcno does not exist")

		if os.path.exists(self.elfFile + '.gcda'+'.gcov.json.gz'):
			os.remove(self.elfFile + '.gcda' + '.gcov.json.gz')
		else:
			print('The file:' + self.elfFile + '.gcda' + '.gcov.json.gz does not exist')

		gcovData = json.loads(file_content);

		return self.__handle_gcov_data(gcovData, 'lines',testinput);

	def __execute_list_tests(self, program_name, test_cases):
		for test in test_cases:
			self.__execute_test(test)

		return 0;

	def pretty_progress(self, executed_lines, total_number_of_lines):
		length = 80;
		percentage = executed_lines/total_number_of_lines;
		print('Total coverage:','[' + '#'*int(length*percentage) + '.'*int(length*(1-percentage)) +']', percentage*100, '%')