from reportlab.platypus import BaseDocTemplate
from reportlab.platypus import IndexingFlowable

class BuildTrigger(IndexingFlowable):
	def __init__(self, engine, builder):
		self.engine = engine
		self.builder = builder
		self.width = 0
		self.height = 0
	
	def draw(self):
		pass
		
	def beforeBuild(self):
		for c in self.engine.buildBeginCallbacks: c(self.engine, self.builder)

	def afterBuild(self):
		for c in self.engine.buildEndCallbacks: c(self.engine, self.builder)

class DocTemplate(BaseDocTemplate):
	def __init__(self, engine, filename, pageTemplates):
		super().__init__(filename, pageTemplates=pageTemplates)
		self.engine = engine
	
	def beforePage(self):
		for c in self.engine.pageBeginCallbacks: c(self.engine, self, self.canv)
	
	def afterPage(self):
		for c in self.engine.pageEndCallbacks: c(self.engine, self, self.canv)
