import copy

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Frame, Flowable
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus.frames import ShowBoundaryValue

frameDefaults = {}
frameDefaults["leftPadding"] = 6
frameDefaults["bottomPadding"] = 6
frameDefaults["rightPadding"] = 6
frameDefaults["topPadding"] = 6
frameDefaults["showBoundary"] = 0

class FrameItem(Flowable):
	def __init__(self, x, y, width, height, blocks, args={}):
		super().__init__()
		self.x = x
		self.y = y
		self.frameWidth = width
		self.frameHeight = height
		self.args = args
		self.blocks = blocks

	def draw(self):
		self.canv.saveState()
		self.canv.resetTransforms()
		frame = Frame(self.x, self.y, self.frameWidth, self.frameHeight, **self.args)
		frame.addFromList(copy.deepcopy(self.blocks), self.canv)
		self.canv.restoreState()

class FixedFrame(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = {}
		self.mandatoryArgs["frame"] = ["x", "y", "width", "height", "content"]
		self.mandatoryArgs["appendFrame"] = ["content"]
		self.frames = {}
	
	def identifier(self):
		return "core.modules.FixedFrame"
	
	def handles(self):
		return ["frame", "appendFrame"]
	
	def process(self, block, path):
		blocks = self.engine.processBlocks(block["content"], path) if "content" in block else []
		
		if block["type"] == "frame":
			args = {}
			for key in frameDefaults:
				args[key] = block[key] if key in block else frameDefaults[key]
			
			if "border" in block:
				borderData = block["border"]
				border = 0
				if type(borderData) is float or type(borderData) is int:
					border = ShowBoundaryValue(colors.black, borderData, None)
				elif type(borderData) is dict:
					color = utils.hexcolor(borderData["color"]) if "color" in borderData else colors.black
					width = borderData["width"] if "width" in borderData else 0.5
					dashes = borderData["dashes"] if "dashes" in borderData else None
					border = ShowBoundaryValue(color, width, dashes)
				elif type(borderData) is bool and borderData:
					border = 1
				args["showBoundary"] = border
			
			frame = FrameItem(block["x"]*cm, block["y"]*cm, block["width"]*cm, block["height"]*cm, blocks, args)
			if "id" in block:
				self.frames[block["id"]] = frame
			return [frame]
		elif block["type"] == "appendFrame" and block["id"] in self.frames:
			self.frames[block["id"]].blocks += blocks

		return []
