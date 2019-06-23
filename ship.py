class Ship:
	def __init__(self, size):
		self.parts = []
		if size == 1:
			self.parts.insert(0,True)
		else:
			for x in range(size):
				self.parts.append(True)