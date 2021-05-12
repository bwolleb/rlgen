from core.modules import ModuleInterface
from core import utils

from reportlab.lib.units import cm
from reportlab.platypus import Flowable
from reportlab.lib import colors

class Hline(Flowable):
	def __init__(self, width, color=colors.black, thickness=0.5, rounded=True, dashes=[1, 0]):
		super().__init__()
		self.width = width
		self.color = color
		self.thickness = thickness
		self.cap = 1 if rounded else 2
		self.dashes = dashes

	def wrap(self, *args):
		return (self.width, self.thickness)

	def draw(self):
		self.canv.saveState()
		self.canv.setLineWidth(self.thickness)
		self.canv.setStrokeColor(self.color)
		self.canv.setLineCap(self.cap)
		self.canv.setDash(*self.dashes)
		self.canv.line(0, 0, self.width, 0)
		self.canv.restoreState()

class Line(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
	
	def identifier(self):
		return "core.modules.Line"
	
	def handles(self):
		return ["line"]
	
	def process(self, block, path):
		dashes = [1, 0]
		if "dashes" in block and type(block["dashes"]) is bool and block["dashes"]:
			dashes = [4, 3]
		elif "dashes" in block and type(block["dashes"]) is list:
			dashes = block["dashes"]
		
		# Page width
		frameWidth = 0
		pageStyleModule = self.engine.getModule("core.modules.PageStyle")
		
		if pageStyleModule is not None and pageStyleModule.currentPageTemplate is not None:
			framdIdx = block["frame"] if "frame" in block else 0
			frameWidth = pageStyleModule.currentPageTemplate.frames[framdIdx]._width
		
		width = frameWidth
		if "width" in block:
			unit = cm
			if "unit" in block:
				if block["unit"] == "cm": unit = cm
				elif block["unit"] == "mm": unit = mm
				elif block["unit"] == "percent": unit = frameWidth
			width = block["width"] * unit

		color = utils.hexcolor(block["color"]) if "color" in block else colors.black
		thickness = block["thickness"] if "thickness" in block else 0.5
		rounded = block["rounded"] if "rounded" in block else False
		align = block["align"] if "align" in block else "CENTER"
		hline = Hline(width, color, thickness, rounded, dashes)
		hline.hAlign = align
		return [hline]
