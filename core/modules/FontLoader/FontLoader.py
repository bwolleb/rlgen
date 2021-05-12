import os

from core.modules import ModuleInterface
from core import utils

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle


def registerFont(name, normal, bold, italic, boldItalic, root="."):
	pdfmetrics.registerFont(TTFont(name, os.path.join(root, normal)))
	pdfmetrics.registerFont(TTFont(name + "B", os.path.join(root, bold)))
	pdfmetrics.registerFont(TTFont(name + "I", os.path.join(root, italic)))
	pdfmetrics.registerFont(TTFont(name + "BI", os.path.join(root, boldItalic)))
	pdfmetrics.registerFontFamily(name, normal=name, bold=name + "B", italic=name + "I", boldItalic=name + "BI")

class FontLoader(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["name", "font", "align", "size", "color"]
	
	def identifier(self):
		return "core.modules.FontLoader"
	
	def handles(self):
		return ["font"]
	
	def buildFont(self, block, path=""):
		fontName = block["font"]
		if "ttf" in block:
			registerFont(fontName, root=path, **block["ttf"])
		
		args = {}
		args["name"] = block["name"] if "name" in block else ""
		args["alignment"] = utils.alignFromTxt(block["align"])
		args["textColor"] = utils.hexcolor(block["color"])
		args["fontName"] = fontName
		args["fontSize"] = block["size"]
		
		for additionalKey in ParagraphStyle.defaults:
			if additionalKey in block:
				args[additionalKey] = block[additionalKey]

		return ParagraphStyle(**args)
	
	def process(self, block, path):
		newStyle = self.buildFont(block, path)
		styleName = block["name"]
		self.engine.fonts[styleName] = newStyle
		textModule = self.engine.getModule("core.modules.Text")
		if textModule is not None:
			if "default" in block and block["default"] or textModule.defaultFont is None and "default" not in block:
				textModule.setDefaultFont(styleName)
		return []
