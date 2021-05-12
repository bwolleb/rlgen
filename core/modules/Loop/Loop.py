from core.modules import ModuleInterface
from core import utils


class Loop(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["data", "content"]
		engine.resources["loops"] = {}
	
	def identifier(self):
		return "core.modules.Loop"
	
	def handles(self):
		return ["loop"]
	
	def process(self, block, path):
		content = block["content"]
		data = utils.getData(self.engine.resources, block["data"])
		loopId = block["id"] if "id" in block else utils.uid()
		prefix = block["prefix"] if "prefix" in block else ""
		loopData = {}
		self.engine.resources["loops"][loopId] = loopData
		build = []
		
		if type(data) is list:
			loopData["nbitems"] = len(data)
			for i in range(len(data)):
				loopData["itemid"] = i
				loopData["currentitem"] = data[i]
				for k in loopData:
					self.engine.resources[prefix + k] = loopData[k]
				build += self.engine.processBlocks(content, path)
		elif type(data) is dict:
			keys = block["keys"]
			loopData["nbitems"] = len(keys)
			for key in keys:
				loopData["itemid"] = key
				loopData["currentitem"] = data[key]
				for k in loopData:
					self.engine.resources[prefix + k] = loopData[k]
				build += self.engine.processBlocks(content, path)
		
		self.engine.resources["loops"].pop(loopId)
		self.engine.resources.pop(prefix + "itemid")
		self.engine.resources.pop(prefix + "currentitem")
		self.engine.resources.pop(prefix + "nbitems")
		return build
