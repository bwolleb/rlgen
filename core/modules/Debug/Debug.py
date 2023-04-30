from core.modules import ModuleInterface
from core import utils

class Debug(ModuleInterface):
	def __init__(self, engine, events=[]):
		super().__init__(engine)
		self.events = events
		self.registeredModules = set()
		engine.beforeBuildCallbacks.append(self.beforeBuild)
		engine.afterBuildCallbacks.append(self.afterBuild)
		self.paras = []

		if "core.modules.ModuleLoader" in engine.modules:
			loader = engine.modules["core.modules.ModuleLoader"]
			loader.afterProcessCallbacks.append(self.afterModuleLoad)

		if "dumpText" in events:
			if "core.modules.Text" in engine.modules:
				engine.modules["core.modules.Text"].buildTextCallbacks.append(self.newText)

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

	def beforeBuild(self, *args):
		if "showFrames" in self.events:
			for ps in self.engine.pagestyles:
				for f in ps.frames:
					f.showBoundary = 1

	def afterBuild(self, *args):
		if "dumpText" in self.events:
			paraTxt = [p.text for p in self.paras]
			print(str.join("\n\n", paraTxt))

	def newText(self, paragraph, data):
		self.paras.append(paragraph)

	def identifier(self):
		return "core.modules.Debug"
