from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import IndexingFlowable

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

class PageCounter(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.pageCounter = None
		self.beforeLastBuildCallbacks = []
		
		engine.beforeBuildCallbacks.append(self.beforeBuild)
		engine.buildBeginCallbacks.append(self.buildBegin)
		engine.buildEndCallbacks.append(self.buildEnd)
		engine.pageBeginCallbacks.append(self.pageBegin)
		
	def beforeBuild(self, engine, builder, blocks):
		self.pageCounter = PageCountBlocker()
		blocks.append(self.pageCounter)
		
	def buildBegin(self, engine, builder):
		buildData = engine.resources["build"]
		buildData["pageNum"] = 0
		if not self.pageCounter.firstRun:
			for c in self.beforeLastBuildCallbacks: c(engine, builder)
	
	def buildEnd(self, engine, builder):
		buildData = engine.resources["build"]
		buildData["pageTot"] = self.pageCounter.pageCount
	
	def pageBegin(self, engine, builder, canv):
		buildData = engine.resources["build"]
		buildData["pageNum"] += 1
				
	def identifier(self):
		return "core.modules.PageCounter"
