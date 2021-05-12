from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class Text(ModuleInterface):
	def __init__(self, engine, defaultFont=None):
		super().__init__(engine)
		self.mandatoryArgs = {}
		self.mandatoryArgs["txt"] = ["content"]
		self.mandatoryArgs["text"] = ["content"]
		self.mandatoryArgs["textstyle"] = ["name"]
		self.defaultFont = defaultFont
		self.buildTextCallbacks = []
	
	def identifier(self):
		return "core.modules.Text"
	
	def handles(self):
		return ["text", "txt", "textstyle"]
	
	def buildText(self, txt, font=None):
		style = font
		if font is None:
			if self.defaultFont is not None and self.defaultFont in self.engine.fonts:
				style = self.engine.fonts[self.defaultFont]
			else:
				style = getSampleStyleSheet()["Normal"]
		elif type(font) is str:
			style = self.engine.fonts[font]
		
		paragraph = Paragraph(txt, style)
		for c in self.buildTextCallbacks: c(paragraph, None)
		return paragraph
	
	def getDefaultFont(self):
		return self.engine.fonts[self.defaultFont] if self.defaultFont is not None and self.defaultFont in self.engine.fonts else None

	def setDefaultFont(self, name):
		if name in self.engine.fonts:
			self.defaultFont = name
		else:
			utils.error("Could not find font: " + name)

	def buildTextFromBlock(self, block):
		style = None
		if "font" in block:
			font = block["font"]
			if type(font) is str:
				if font in self.engine.fonts:
					style = self.engine.fonts[font]
				else:
					utils.error("undefined font: " + font)
			elif type(font) is dict:
				if "core.modules.FontLoader" in self.engine.modules:
					fontModule = self.engine.modules["core.modules.FontLoader"]
					style = fontModule.buildFont(font)
					self.engine.fonts[font["name"]] = style
				else:
					utils.error("Asked to build a new font, but FontLoader module is not loaded")
		
		if style is None:
			style = self.getDefaultFont()

		if style is None:
			style = getSampleStyleSheet()["Normal"]
		
		paragraph = Paragraph(block["content"], style)
		for c in self.buildTextCallbacks: c(paragraph, block)
		return paragraph
	
	def process(self, block, path):
		blockType = block["type"]
		if blockType == "text" or blockType == "txt":
			return [self.buildTextFromBlock(block)]
		elif blockType == "textstyle":
			self.setDefaultFont(block["name"])
		return []
