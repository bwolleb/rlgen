from core.modules import ModuleInterface
from core import utils

class Debug(ModuleInterface):
	def __init__(self, engine, events=[]):
		super().__init__(engine)
		self.events = events
		self.registeredModules = set()
		
		if "core.modules.ModuleLoader" in engine.modules:
			loader = engine.modules["core.modules.ModuleLoader"]
			loader.afterProcessCallbacks.append(self.afterModuleLoad)
	
	def afterModuleLoad(self, module, block, *args):
		moduleId = block["id"]
		if moduleId not in self.registeredModules:
			if "loadModule" in self.events: print("Loaded module " + moduleId)
			self.registeredModules.add(moduleId)
			newModule = self.engine.modules[moduleId]
			newModule.beforeProcessCallbacks.append(self.beforeModule)
			newModule.afterProcessCallbacks.append(self.afterModule)
	
	def beforeModule(self, module, block, *args):
		if "beforeProcess" in self.events:
			print(module.identifier() + " processing " + block["type"])
	
	def afterModule(self, module, block, *args):
		if "afterProcess" in self.events:
			print(module.identifier() + " finished processing " + block["type"])
	
	def identifier(self):
		return "core.modules.Debug"
