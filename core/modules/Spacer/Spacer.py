from core.modules import ModuleInterface
from core import utils

import reportlab.platypus
from reportlab.lib.units import cm, mm

class Spacer(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
	
	def identifier(self):
		return "core.modules.Spacer"
	
	def handles(self):
		return ["vspace", "hspace", "space"]
	
	def process(self, block, path):
		factor = [1, 1]
		
		if "unit" in block and block["unit"] == "cm":
			factor = [cm, cm]
		elif "unit" in block and block["unit"] == "mm":
			factor = [mm, mm]
		elif "unit" in block and block["unit"] == "percent":
			pagesize = self.engine.pagestyles[0].pagesize if len(self.engine.pagestyles) > 0 else None
			newPageModule = self.engine.getModule("core.modules.NewPage")
			if  newPageModule is not None:
				if newPageModule.currentPageTemplate is not None:
					pagesize = newPageModule.currentPageTemplate.pagesize
			if pagesize is None:
				utils.error("Current page size is unknown")
			else:
				factor = [pagesize[0] / 100, pagesize[1] / 100]
		
		size = [12, 12]
		if "size" in block:
			requiredSize = block["size"]
			if type(requiredSize) is int or type(requiredSize) is float:
				size = [requiredSize, requiredSize]
			elif type(requiredSize) is list and len(requiredSize) == 2:
				size = requiredSize
		
		if block["type"] == "vspace":
			size[0] = 0
		elif block["type"] == "hspace":
			size[1] = 0
		
		return [reportlab.platypus.Spacer(size[0] * factor[0], size[1] * factor[1])]
