import sys
from termcolor import colored

class Debug:
	"""
	Helper class with one method write, which outputs to deisred file or if non provided defaulted by sys.stdout
	If its initialized with False it will not print anything
	"""
	def __init__(self, debug = False):
		#something
		self.dbg= debug
	def write(self, message = "", color = "white", end = '\n', file = sys.stdout):
		"""
		file - to white file to be written, default sys.stdout
		"""
		if self.dbg:
			print(colored(message, color), end = end,  file = file)
		
