from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Flowable
from reportlab.lib.units import cm

class Painting(Flowable):
	def __init__(self, engine, code, path):
		super().__init__()
		self.engine = engine
		self.code = code
		self.path = path

	def draw(self):
		self.canv.saveState()
		self.canv.resetTransforms()
		env = {"engine": self.engine, "canvas": self.canv, "path": self.path}
		exec(self.code, {"utils": utils, "cm": cm}, env)
		self.canv.restoreState()

class Painter(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["python"]
	
	def identifier(self):
		return "core.modules.Painter"
	
	def handles(self):
		return ["paint"]
	
	def process(self, block, path):
		return [Painting(self.engine, block["python"], path)]
