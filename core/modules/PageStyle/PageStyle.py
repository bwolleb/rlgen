from core.modules import ModuleInterface
from core import utils

from reportlab.lib.units import cm
from reportlab.platypus import PageTemplate, Frame, Flowable
import reportlab.lib.pagesizes

def pagesizeFromString(requestedSize, orientation):
	size = None
	if hasattr(reportlab.lib.pagesizes, requestedSize):
		size = getattr(reportlab.lib.pagesizes, requestedSize)
	
	if orientation is not None and size is not None:
		if orientation == "portrait":
			size = reportlab.lib.pagesizes.portrait(size)
		elif orientation == "landscape":
			size = reportlab.lib.pagesizes.landscape(size)
	
	return size

class CustomPageTemplate(PageTemplate):
	def __init__(self, engine, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.engine = engine

	def beforeDrawPage(self, canvas, builder):
		buildData = self.engine.resources["build"]
		buildData["pageTemplate"] = self.id

class PageStyle(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = {}
		self.mandatoryArgs["page"] = ["name", "size", "frames"]
		self.mandatoryArgs["pagestyle"] = ["name"]
		self.currentPageTemplate = None
	
	def identifier(self):
		return "core.modules.PageStyle"
	
	def handles(self):
		return ["page", "pagestyle"]
	
	def buildTemplate(self, block):
		size = None
		requestedSize = block["size"]
		if type(requestedSize) is list:
			size = (requestedSize[0]*cm, requestedSize[1]*cm)
		elif type(requestedSize) is str:
			size = pagesizeFromString(requestedSize, block["orientation"] if "orientation" in block else None)
		
		if size is None:
			utils.error(self.identifier() + ": invalid size: " + str(requestedSize))
			return []
		
		frames = []
		for f in block["frames"]:
			if "x" in f and "y" in f and "width" in f and "height" in f:
				x = f["x"]*cm
				y = f["y"]*cm
				width = f["width"]*cm
				height = f["height"]*cm
			elif "margin_left" in f and "margin_bottom" in f and "margin_right" in f and "margin_top" in f:
				x = f["margin_left"]*cm
				y = f["margin_bottom"]*cm
				width = size[0] - x - f["margin_right"]*cm
				height = size[1] - y - f["margin_top"]*cm
			else:
				utils.error(self.identifier() + ": invalid frame: " + str(f))
				return []
			
			frames.append(Frame(x, y, width, height, 0, 0, 0, 0))
		
		return CustomPageTemplate(self.engine, block["name"], frames, pagesize=size)
	
	def setDefault(self, name):
		found = False
		for i, ps in enumerate(self.engine.pagestyles):
			if ps.id == name:
				found = True
				self.currentPageTemplate = self.engine.pagestyles.pop(i)
				self.engine.pagestyles.insert(0, self.currentPageTemplate)
				break
		
		if not found:
			utils.error("Could not find page style: " + name)
	
	def process(self, block, path):
		blockType = block["type"]
		if blockType == "page":
			template = self.buildTemplate(block)
			self.engine.pagestyles.append(template)
			
			if "default" in block and block["default"] or self.currentPageTemplate is None and "default" not in block:
				self.setDefault(block["name"])
		elif blockType == "pagestyle":
			self.setDefault(block["name"])
		return []
