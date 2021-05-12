from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import PageBreak, CondPageBreak, NextPageTemplate

class NewPage(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
	
	def identifier(self):
		return "core.modules.NewPage"
	
	def handles(self):
		return ["newpage"]
	
	def process(self, block, path):
		beforeBreak = []
		pageBreak = []
		pageStyleModule = self.engine.getModule("core.modules.PageStyle")
		currentPageTemplate = None
		
		if pageStyleModule is not None:
			currentPageTemplate = pageStyleModule.currentPageTemplate
		
		if currentPageTemplate is None and len(self.engine.pagestyles) > 0:
			currentPageTemplate = self.engine.pagestyles[0]
		
		if currentPageTemplate is not None:
			pageBreak.append(CondPageBreak(0.9 * currentPageTemplate.pagesize[1]))
		else:
			pageBreak.append(PageBreak())
		
		if "nextPage" in block:
			layout = block["nextPage"]
			if type(layout) is str:
				nextPagestyle = self.engine.getPageStyle(layout)
				if nextPagestyle is not None:
					beforeBreak.append(NextPageTemplate(layout))
					if pageStyleModule is not None:
						pageStyleModule.currentPageTemplate = nextPagestyle
				else:
					utils.error("Unknown pagestyle: " + layout)
			elif type(layout) is dict:
				if pageStyleModule is not None:
					template = pageStyleModule.buildTemplate(layout)
					pageStyleModule.currentPageTemplate = template
					self.engine.pagestyles.append(template)
					beforeBreak.append(NextPageTemplate(layout["name"]))
				else:
					utils.error("Asked to build a new page layout, but PageStyle module is not loaded")
			
		return beforeBreak + pageBreak
