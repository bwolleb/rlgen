import re

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import ActionFlowable

class TocEntryItem(ActionFlowable):
	def __init__(self, text, link, level):
		super().__init__()
		self.text = text
		self.link = link
		self.level = level
	
	def apply(self, doc):
		doc.notify('TOCEntry', (self.level, self.text, doc.page, self.link))
		doc.canv.addOutlineEntry(re.sub("<[^>]*>", "", self.text), self.link, self.level)

class TocEntry(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["text"]
	
	def identifier(self):
		return "core.modules.TocEntry"
	
	def handles(self):
		return ["tocEntry"]
	
	def buildTocEntry(self, text, link, level):
		return TocEntryItem(text, link, level)
	
	def process(self, block, path):
		text = block["text"]
		link = block["id"] if "id" in block else utils.uid()
		level = block["level"] if "level" in block else 0
		return [self.buildTocEntry(text, link, level)]
