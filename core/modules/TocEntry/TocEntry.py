import re

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import ActionFlowable

class TocEntryItem(ActionFlowable):
	def __init__(self, text, link, level, notif="TOCEntry", outline=True):
		super().__init__()
		self.text = text
		self.link = link
		self.level = level
		self.notif = notif
		self.outline = outline

	def apply(self, doc):
		doc.notify(self.notif, (self.level, self.text, doc.page, self.link))
		if self.outline:
			doc.canv.addOutlineEntry(re.sub("<[^>]*>", "", self.text), self.link, self.level)

class TocEntry(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["text"]
	
	def identifier(self):
		return "core.modules.TocEntry"
	
	def handles(self):
		return ["tocEntry"]
	
	def buildTocEntry(self, text, link, level, notif="TOCEntry", outline=True):
		return TocEntryItem(text, link, level, notif, outline)
	
	def process(self, block, path):
		text = block["text"]
		level = block["level"] if "level" in block else 0
		notif = block["notif"] if "notif" in block else "TOCEntry"
		outline = block["outline"] if "outline" in block else True

		bookmarkModule = self.engine.getModule("core.modules.Bookmark")
		link = bookmarkModule.registerBookmark(block["id"]) if "id" in block else utils.uid()
		bookmark = bookmarkModule.buildBookmark(link)
		return [bookmark, self.buildTocEntry(text, link, level, notif, outline)]
