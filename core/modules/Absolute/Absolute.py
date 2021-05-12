import importlib

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Flowable
from reportlab.lib.units import cm

class AbsoluteItem(Flowable):
	def __init__(self, block, x, y):
		super().__init__()
		self.block = block
		self.x = x
		self.y = y

	def draw(self):
		self.canv.saveState()
		self.canv.resetTransforms()
		self.block.wrap(self.canv._pagesize[0] - self.x, self.canv._pagesize[1] - self.x)
		self.block.drawOn(self.canv, self.x, self.y)
		self.canv.restoreState()

class Absolute(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["content", "x", "y"]
	
	def identifier(self):
		return "core.modules.Absolute"
	
	def handles(self):
		return ["absolute"]
	
	def process(self, block, path):
		blocks = self.engine.processBlocks(block["content"], path)
		
		if len(blocks) > 0:
			if len(blocks) > 1:
				utils.error("More than one block provided")
			return [AbsoluteItem(blocks[0], block["x"]*cm, block["y"]*cm)]
		
		return []
