import copy

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Flowable
from reportlab.lib.units import cm

exprVar = "coreModulesDecoratorPageMatch"

class Decoration(object):
	def __init__(self, items, path, trigger="begin", expression=None, enabled=True):
		self.items = items
		self.path = path
		self.trigger = trigger
		self.expression = expression
		self.enabled = enabled
	
	def match(self, engine, trigger):
		triggerOk = self.trigger == trigger
		exprOk = True
		
		if self.expression is not None:
			exprData = copy.deepcopy(engine.resources["build"])
			exec("{} = {}".format(exprVar, self.expression), {}, exprData)
			exprOk = exprData[exprVar]
			
		return self.enabled and triggerOk and exprOk
	
	def decorate(self, engine, builder, canvas):
		canvas.saveState()
		canvas.resetTransforms()
		for item in self.items:
			blocks = engine.processBlock(item, self.path)
			x = item["x"]*cm if "x" in item else 0
			y = item["y"]*cm if "y" in item else 0
			w = item["width"]*cm if "width" in item else canvas._pagesize[0] - x
			h = item["height"]*cm if "height" in item else canvas._pagesize[1] - y
			for block in blocks:
				block.wrap(w, h)
				block.drawOn(canvas, x, y)
		canvas.restoreState()
				

class DecorationTrigger(Flowable):
	def __init__(self, deco, enabled):
		super().__init__()
		self.deco = deco
		self.enabled = enabled

	def draw(self):
		self.deco.enabled = self.enabled

class Decorator(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = {}
		self.mandatoryArgs["decoration"] = ["items"]
		self.decorations = {}
		
		engine.pageBeginCallbacks.append(self.pageBegin)
		engine.pageEndCallbacks.append(self.pageEnd)
	
	def identifier(self):
		return "core.modules.Decorator"
	
	def handles(self):
		return ["decoration", "enableDecoration", "disableDecoration"]
	
	def pageBegin(self, engine, builder, canvas):
		for deco in self.decorations.values():
			if deco.match(engine, "begin"):
				deco.decorate(engine, builder, canvas)

	def pageEnd(self, engine, builder, canvas):
		for deco in self.decorations.values():
			if deco.match(engine, "end"):
				deco.decorate(engine, builder, canvas)
	
	def process(self, block, path):
		if block["type"] == "decoration":
			trigger = block["trigger"] if "trigger" in block else "begin"
			expression = block["expression"] if "expression" in block else None
			enabled = block["enabled"] if "enabled" in block else True
			decoId = block["id"] if "id" in block else utils.uid()
			decoration = Decoration(block["items"], path, trigger, expression, enabled)
			self.decorations[decoId] = decoration
		elif block["type"] == "enableDecoration":
			return [DecorationTrigger(self.decorations[block["id"]], True)]
		elif block["type"] == "disableDecoration":
			return [DecorationTrigger(self.decorations[block["id"]], False)]
			
		return []
