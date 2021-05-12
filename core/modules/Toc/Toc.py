from core.modules import ModuleInterface
from core import utils

from reportlab.platypus.tableofcontents import TableOfContents

class Toc(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
	
	def identifier(self):
		return "core.modules.Toc"
	
	def handles(self):
		return ["toc"]
	
	def process(self, block, path):
		toc = TableOfContents()
		fontModule = self.engine.modules["core.modules.FontLoader"] if "core.modules.FontLoader" in self.engine.modules else None
		
		if "dotsMinLevel" in block:
			toc.dotsMinLevel = block["dotsMinLevel"]
		
		if "style" in block:
			styles = []
			for s in block["style"]:
				if type(s) is str:
					if s in self.engine.fonts:
						styles.append(self.engine.fonts[s])
					else:
						utils.error("Unknown font: " + s)
				elif type(s) is dict:
					if fontModule is not None:
						newStyle = fontModule.buildFont(s)
						if "name" in s:
							self.engine.fonts[s["name"]] = newStyle
						styles.append(newStyle)
					else:
						utils.error("FontLoader is not available")
			toc.levelStyles = styles
		return [toc]
