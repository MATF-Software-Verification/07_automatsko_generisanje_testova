import sys
from termcolor import colored

class Debug:
	"""
	Helper class with one method write, which outputs to deisred file or if non provided defaulted by sys.stdout
	If its initialized with False it will not print anything
	"""
	def __init__(self, debug = False, info=False):
		#something
		self.dbg = debug
		self.info = info

	def write(self, message = "", color = "white", end = '\n', file = sys.stdout):
		"""
		file - to white file to be written, default sys.stdout
		"""
		if self.dbg:
			print(colored(message, color), end = end,  file = file)
		
	def write_err(self, message = "", color="red", end = '\n', file = sys.stderr):
		print(colored(message,color), end=end, file = file)

	def log(self, message = "", extra_data = "", color="white", end = '\n', file = sys.stdout):
		if self.info:
			print(colored(message, color), colored(extra_data, color), end=end, file=file)