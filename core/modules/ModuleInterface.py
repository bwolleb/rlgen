from core import utils

class ModuleInterface(object):
	def __init__(self, engine):
		self.engine = engine
		self.mandatoryArgs = []
		self.beforeProcessCallbacks = []
		self.afterProcessCallbacks = []
	
	def identifier(self):
		return "core.modules.ModuleInterface"
	
	def handles(self):
		return []
	
	def processBlock(self, block, path="."):
		if not self.validate(block): return []
		for c in self.beforeProcessCallbacks: c(self, block, path)
		build = self.process(block, path)
		for c in self.afterProcessCallbacks: c(self, block, path, build)
		return build
	
	def process(self, block, path="."):
		return []
	
	def validate(self, block):
		missingArgs = []
		
		# Get list of mandatory args
		mandatoryList = []
		blockType = block["type"]
		if type(self.mandatoryArgs) is list:
			mandatoryList = self.mandatoryArgs
		elif type(self.mandatoryArgs) is dict and blockType in self.mandatoryArgs:
			mandatoryList = self.mandatoryArgs[blockType]

		for arg in mandatoryList:
			if arg not in block:
				missingArgs.append(arg)

		if len(missingArgs) > 0:
			utils.error(self.identifier() + ": ignoring block due to missing args: " + str.join(",", missingArgs))
			return False
		return True
