import os

from core.modules import ModuleInterface
from core import pdfutils

from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from reportlab.platypus import Flowable
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak

class PDFNativePage(Flowable):
	def __init__(self, page):
		super().__init__()
		self.page = page

	def wrap(self, availWidth, availHeight):
		return (availWidth, availHeight)

	def draw(self):
		self.canv.setPageSize((self.page.BBox[2], self.page.BBox[3]))
		self.canv.resetTransforms()
		self.canv.doForm(makerl(self.canv, self.page))

# https://stackoverflow.com/a/5921708
def intersperse(lst, item):
	result = [item] * (len(lst) * 2 - 1)
	result[0::2] = lst
	return result

class PDF(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["path"]

	def identifier(self):
		return "core.modules.PDF"
	
	def handles(self):
		return ["pdf"]
	
	def process(self, block, path):
		pages = None
		if "pages" in block: pages = [idx - 1 for idx in block["pages"]]
		elif "from" in block and "to" in block: pages = list(range(block["from"] - 1, block["to"])) # natural page number, starts at 1
		fullpath = os.path.join(path, block["path"])
		document = pdfutils.getPdfPages(fullpath)
		pages = document if pages is None else [document[idx] for idx in pages]
		pdfPages = [PDFNativePage(p) for p in pages]

		result = [PageBreak() for i in range(len(pdfPages) * 2 - 1)]
		result[0::2] = pdfPages

		return result
