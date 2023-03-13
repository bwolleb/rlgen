import matplotlib.pyplot as plt
import io

from core.modules import ModuleInterface
from core import utils
from core import pdfutils
from reportlab.lib.units import cm

class Plot(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
	
	def identifier(self):
		return "extra.plot"
	
	def handles(self):
		return ["plot"]
	
	def process(self, block, path):
		if "width" in block:
			width = block["width"]*cm
		else:
			pageStyleModule = self.engine.getModule("core.modules.PageStyle")
			if pageStyleModule is not None and pageStyleModule.currentPageTemplate is not None:
				width = pageStyleModule.currentPageTemplate.frames[0]._width

		align = block["align"] if "align" in block else "CENTER"

		exec(block["python"])
		buff = io.BytesIO()
		plt.savefig(buff, format="pdf")
		buff.seek(0)
		img = pdfutils.PDFPage(pdfutils.getPdfPages(buff)[0], width)
		img.hAlign = align
		return [img]
