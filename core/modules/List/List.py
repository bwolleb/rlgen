from core.modules import ModuleInterface
from core import utils
import copy

import reportlab.platypus
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ListStyle
from reportlab.platypus import ListFlowable

bullets = {}
bullets["longdash"] = u"\u2014"
bullets["bullet"] = "circle"
bullets["emptyBullet"] = u"\u25E6"
bullets["arrow"] = u"\u2192"

defaultFormat = "%s. "

defaultProps = copy.deepcopy(ListStyle.defaults)
defaultProps["bulletFontSize"] = 6
defaultProps["bulletOffsetY"] = -4
defaultProps["bulletDedent"] = 15
defaultProps["leftIndent"] = 30
defaultProps["bulletFontName"] = "Times-Roman"

class List(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["items"]
		self.lastList = None
		engine.resources["lists"] = {}
	
	def identifier(self):
		return "core.modules.List"
	
	def handles(self):
		return ["list"]
	
	def process(self, block, path):
		textModule = self.engine.getModule("core.modules.Text")
		listId = block["id"] if "id" in block else utils.uid()
		if listId not in self.engine.resources["lists"]:
			if "start" in block:
				start = block["start"]
				if type(start) is int:
					startValue = start
				elif type(start) is str and start == "continue":
					startValue = self.engine.resources["lists"][self.lastList]
				else:
					startValue = self.engine.resources["lists"][start]
			else:
				startValue = 1
			self.engine.resources["lists"][listId] = startValue

		args = {}
		for prop in defaultProps.keys():
			args[prop] = block[prop] if prop in block else defaultProps[prop]
		
		font = block["font"] if "font" in block else None
		
		if "numbered" in block and block["numbered"]:
			args["bulletFormat"] = defaultFormat if "format" not in block else block["format"]
			args["start"] = self.engine.resources["lists"][listId]
			
			currentFont = textModule.getDefaultFont() if textModule is not None else None
			if "bulletFontName" not in block and currentFont is not None:
				args["bulletFontName"] = currentFont.fontName
			if "bulletFontSize" not in block and currentFont is not None:
				args["bulletFontSize"] = currentFont.fontSize
			if "bulletOffsetY" not in block:
				args["bulletOffsetY"] = 0
		else:
			args["value"] = "bullet"
			args["bulletType"] = "bullet"
			bullet = bullets["bullet"]
			
			if "bullet" in block:
				if block["bullet"] == "custom":
					bullet = block["bulletChar"]
				else:
					bullet = bullets[block["bullet"]]
			
			args["start"] = bullet
		
		items = []
		if type(block["items"]) is list:
			items = block["items"]
		elif type(block["items"]) is str:
			items = utils.getData(self.engine.resources, block["items"])
			if items is None:
				utils.error("Could not get resource: " + block["items"])
		
		listItems = []
		for i in items:
			if type(i) is str:
				listItems.append(textModule.buildText(i, font))
			elif type(i) is dict:
				listItems.append(self.engine.processBlock(i, path))
			elif type(i) is list:
				listItems.append(self.engine.processBlocks(i, path))
		
		self.engine.resources["lists"][listId] += len(listItems)
		self.lastList = listId
		
		return [ListFlowable(listItems, **args)]
