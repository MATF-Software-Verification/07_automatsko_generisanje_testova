import sys

class Debug:
	"""

	"""
	def __init__(self, write = False):
		#something
		self.write = write

	def write_to_outs(self, message = None, file = sys.stdout):
		"""
		file - to white file to be written, default sys.stdout
		"""
		if self.write != True:
			return
		print(message, file = file)
