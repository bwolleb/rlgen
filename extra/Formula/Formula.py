from io import BytesIO

from core.modules import ModuleInterface
from core import utils
from core import pdfutils

from reportlab.lib.units import cm
from matplotlib import pyplot as plt

def renderLaTeX(formula, fontsize=12, dpi=300, format="pdf", pad=0):
	fig = plt.figure(figsize=(0.01, 0.01))
	fig.text(0, 0, formula, fontsize=fontsize)
	renderBuffer = BytesIO()
	fig.savefig(renderBuffer, dpi=dpi, transparent=True, format=format, bbox_inches="tight", pad_inches=pad)
	plt.close(fig)
	renderBuffer.seek(0)
	return renderBuffer

class Formula(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["expression"]
	
	def identifier(self):
		return "extra.Formula"
	
	def handles(self):
		return ["formula"]
	
	def process(self, block, path):
		if "width" in block:
			width = block["width"]*cm
		else:
			pageStyleModule = self.engine.getModule("core.modules.PageStyle")
			if pageStyleModule is not None and pageStyleModule.currentPageTemplate is not None:
				width = pageStyleModule.currentPageTemplate.frames[0]._width
		
		pad = block["pad"] if "pad" in block else 0
		
		rendered = renderLaTeX(block["expression"], pad=pad)
		img = pdfutils.PDFPage(pdfutils.getPdfPages(rendered)[0], width)
		img.hAlign = block["align"] if "align" in block else "CENTER"
		return [img]
