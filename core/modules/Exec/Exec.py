from core.modules import ModuleInterface
from core import utils

class DynamicModule(ModuleInterface):
	def __init__(self, engine, blockTypes, code):
		super().__init__(engine)
		self.blockTypes = blockTypes
		self.code = code
		self.id = utils.uid()
	
	def identifier(self):
		return self.id
	
	def handles(self):
		return self.blockTypes
	
	def process(self, block, path):
		env = {"engine": self.engine, "block": block, "build": [], "path": path}
		exec(self.code, {"utils": utils}, env)
		return env["build"]

class Exec(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["python"]
	
	def identifier(self):
		return "core.modules.Exec"
	
	def handles(self):
		return ["exec", "function"]
	
	def process(self, block, path):
		if block["type"] == "exec":
			env = {"engine": self.engine, "build": [], "path": path}
			exec(block["python"], {"utils": utils}, env)
			return env["build"]
		elif block["type"] == "function":
			module = DynamicModule(self.engine, block["blockTypes"], block["python"])
			self.engine.modules[module.identifier()] = module
			for blockType in module.handles():
				self.engine.blockHandlers[blockType] = module.identifier()
		return []
