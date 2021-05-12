from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.platypus import Flowable

def getPdfPages(path):
	pages = PdfReader(path).pages
	return [pagexobj(x) for x in pages]

class PDFPage(Flowable):
	def __init__(self, page, width):
		super().__init__()
		self.page = page
		self.width = width
		self.height = width / (page.BBox[2] / page.BBox[3])

	def wrap(self, availWidth, availHeight):
		if availWidth < self.width:
			self.width = availWidth
			self.height = width / (page.BBox[2] / page.BBox[3])
		return (self.width, self.height)

	def draw(self):
		factor = 1 / (self.page.BBox[2] / self.width)
		self.canv.saveState()
		self.canv.scale(factor, factor)
		self.canv.doForm(makerl(self.canv, self.page))
		self.canv.restoreState()
