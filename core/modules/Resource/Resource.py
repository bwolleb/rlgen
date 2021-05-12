import os

from core.modules import ModuleInterface
from core import utils

class Resource(ModuleInterface):
	def __init__(self, engine, prefix=None):
		super().__init__(engine)
		mandatoryArgs = {}
		mandatoryArgs["resource"] = ["alias", "path"]
		mandatoryArgs["data"] = ["alias", "data"]
		
		if prefix is not None:
			engine.resources[prefix] = {}
			self.container = engine.resources[prefix]
		else:
			self.container = engine.resources
	
	def identifier(self):
		return "core.modules.Resource"
	
	def handles(self):
		return ["resource", "data"]
	
	def process(self, block, path):
		if block["type"] == "resource":
			fullpath = os.path.join(path, block["path"])
			if not os.path.isfile(fullpath):
				utils.error("Can not open " + fullpath)
				return []
				
			data = utils.loadFile(fullpath)
		elif block["type"] == "data":
			data = block["data"]
		alias = block["alias"]
		if alias not in self.container:
			self.container[alias] = data
		else:
			utils.error("A resource already exists with that name: " + alias)
		return []
