from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import IndexingFlowable, NullDraw

# This class is a trick to count the total number of pages. This class must be included at
# the end of the report and ask for one more generation to include the correct page count.

class PageCountBlocker(IndexingFlowable):
	def __init__(self):
		super().__init__()
		self.pageCount = 0
		self.firstRun = True

	def draw(self):
		self.pageCount = self.canv.getPageNumber()

	def isSatisfied(self):
		if self.firstRun:
			self.firstRun = False
			return False
		return True

class SectionMark(NullDraw):
	def __init__(self, callback, identifier):
		super().__init__()
		self.callback = callback
		self.identifier = identifier

	def draw(self):
		self.callback(self.identifier)

class PageCounter(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["id"]
		self.pageCounter = None
		self.beforeLastBuildCallbacks = []

		engine.beforeBuildCallbacks.append(self.beforeBuild)
		engine.buildBeginCallbacks.append(self.buildBegin)
		engine.buildEndCallbacks.append(self.buildEnd)
		engine.pageBeginCallbacks.append(self.pageBegin)

	def beforeBuild(self, engine, builder, blocks):
		self.pageCounter = PageCountBlocker()
		blocks.append(self.pageCounter)
		defaultSec = {"id": "_default", "start": 1, "page": 0, "tot": 0}
		engine.resources["sections"] = {"_current": defaultSec, "_default": defaultSec}

	def buildBegin(self, engine, builder):
		buildData = engine.resources["build"]
		buildData["pageNum"] = 0
		engine.resources["sections"]["_current"] = engine.resources["sections"]["_default"]
		engine.resources["sections"]["_current"]["page"] = 0
		if not self.pageCounter.firstRun:
			for c in self.beforeLastBuildCallbacks: c(engine, builder)

	def buildEnd(self, engine, builder):
		buildData = engine.resources["build"]
		buildData["pageTot"] = self.pageCounter.pageCount

		curSec = self.engine.resources["sections"]["_current"]
		curSec["tot"] = self.pageCounter.pageCount - curSec["start"] + 1

	def pageBegin(self, engine, builder, canv):
		buildData = engine.resources["build"]
		buildData["pageNum"] += 1
		curSec = self.engine.resources["sections"]["_current"]
		curSec["page"] = buildData["pageNum"] - curSec["start"] + 1

	def handles(self):
		return ["section"]

	def identifier(self):
		return "core.modules.PageCounter"

	def sectionStart(self, identifier):
		page = self.engine.resources["build"]["pageNum"]
		curSec = self.engine.resources["sections"]["_current"]
		curSec["tot"] = page - curSec["start"]
		if identifier not in self.engine.resources["sections"]:
			newSec = {"id": identifier, "start": page, "page": 1, "tot": 0}
			self.engine.resources["sections"][identifier] = newSec
		else:
			self.engine.resources["sections"][identifier]["page"] = 1
		self.engine.resources["sections"]["_current"] = self.engine.resources["sections"][identifier]

	def process(self, block, path):
		return [SectionMark(self.sectionStart, block["id"])]
