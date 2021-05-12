import os

from core.modules import ModuleInterface
from core import utils

assetsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

class Template(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["name"]
	
	def identifier(self):
		return "core.modules.Template"
	
	def handles(self):
		return ["template"]

	def process(self, block, path):
		loader = self.engine.getModule("core.modules.Include", True)
		name = block["name"]
		
		for filename in os.listdir(assetsDir):
			template, ext = os.path.splitext(filename)
			if template == name and loader is not None:
				return loader.processFile(assetsDir, filename)
		
		utils.error("Unable to load template: " + name)
		return []
