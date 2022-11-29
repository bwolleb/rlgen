import sys
import importlib

from core.modules import ModuleInterface
from core import utils

class ModuleLoader(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["id"]
	
	def identifier(self):
		return "core.modules.ModuleLoader"
	
	def handles(self):
		return ["module", "set", "call"]
	
	def loadModule(self, moduleId, args={}):
		try:
			module = importlib.import_module(moduleId)
			instance = module.Module(self.engine, **args)
			moduleIdentifier = instance.identifier()
			if moduleIdentifier in self.engine.modules:
				utils.error("Warning, module already loaded: " + moduleId)
			self.engine.modules[instance.identifier()] = instance
			for blockType in instance.handles():
				self.engine.blockHandlers[blockType] = instance.identifier()
			return instance
		except ModuleNotFoundError as e:
			utils.error("Could not load module: " + moduleId)
			utils.error(str(e))
			return None
	
	def process(self, block, path):
		if "path" in block:
			path = block["path"]
			if path not in sys.path:
				sys.path.append(path)
		
		args = block["args"] if "args" in block else {}
		moduleId = block["id"]
		
		if moduleId not in self.engine.modules:
			module = self.loadModule(moduleId, args)
		
		if "set" in block:
			if moduleId in self.engine.modules:
				method = block["set"]
				data = block["data"]
				module = self.engine.modules[moduleId]
				if hasattr(module, method):
					setattr(module, method, data)
		elif "call" in block:
			if moduleId in self.engine.modules:
				method = block["call"]
				data = block["data"]
				module = self.engine.modules[moduleId]
				if hasattr(module, method):
					getattr(module, method)(data)
		
		return []
