import os
import magic

from core.modules import ModuleInterface
from core import utils
from core import pdfutils

from reportlab.lib.units import cm
from reportlab.lib import utils as rlutils
import reportlab.platypus

mime = magic.Magic(mime=True)
allowedImages = [
	"image/jpeg",
	"image/png",
	"image/x-ms-bmp",
	"image/tiff",
	"image/gif"]

class SwapItem(reportlab.platypus.Flowable):
	def __init__(self, items, current=0):
		super().__init__()
		self.items = items
		self.current = current
	
	def wrap(self, *args, **kwargs): return self.items[self.current].wrap(*args, **kwargs)
	def self(self): return self.items[self.current].wrap()
	def identify(self, *args, **kwargs): return self.items[self.current].identify(*args, **kwargs)
	def drawOn(self, *args, **kwargs): return self.items[self.current].drawOn(*args, **kwargs)
	def wrapOn(self, *args, **kwargs): return self.items[self.current].wrapOn(*args, **kwargs)
	def splitOn(self, *args, **kwargs): return self.items[self.current].splitOn(*args, **kwargs)
	def split(self, *args, **kwargs): return self.items[self.current].split(*args, **kwargs)
	def minWidth(self): return self.items[self.current].minWidth()
	def getKeepWithNext(self): return self.items[self.current].getKeepWithNext()
	def getSpaceAfter(self): return self.items[self.current].getSpaceAfter()
	def getSpaceBefore(self): return self.items[self.current].getSpaceBefore()
	def isIndexing(self): return self.items[self.current].isIndexing()

class Image(ModuleInterface):
	def __init__(self, engine, renderOnLastBuild=True):
		super().__init__(engine)
		self.mandatoryArgs = ["path"]
		self.renderOnLastBuild = renderOnLastBuild
		self.placeholders = []
		
		if renderOnLastBuild:
			if "core.modules.PageCounter" in engine.modules:
				engine.modules["core.modules.PageCounter"].beforeLastBuildCallbacks.append(self.beforeLastBuild)
			else:
				utils.error("Can not register to last build callback, image optimization disabled")
				renderOnLastBuild = False
				
	def identifier(self):
		return "core.modules.Image"
	
	def handles(self):
		return ["image", "img"]
	
	def process(self, block, path):
		if "width" in block:
			width = block["width"]*cm
		else:
			pageStyleModule = self.engine.getModule("core.modules.PageStyle")
			if pageStyleModule is not None and pageStyleModule.currentPageTemplate is not None:
				width = pageStyleModule.currentPageTemplate.frames[0]._width
		
		fullpath = os.path.join(path, block["path"])
		imageType = mime.from_file(fullpath)
		align = block["align"] if "align" in block else "CENTER"
		
		if imageType in allowedImages:
			orig = rlutils.ImageReader(fullpath)
			iw, ih = orig.getSize()
			aspect = ih / float(iw)
			height = width * aspect if "height" not in block else block["height"]*cm
			img = reportlab.platypus.Image(fullpath, width=width, height=height)
		
		elif imageType == "application/pdf":
			pageIdx = block["page"] if "page" in block else 0
			img = pdfutils.PDFPage(pdfutils.getPdfPages(fullpath)[pageIdx], width)
			height = img.height
		
		else:
			utils.error("Unsupported image type: " + fullpath)
			return []
		
		img.hAlign = align
		
		if self.renderOnLastBuild:
			spacer = reportlab.platypus.Spacer(width, height)
			placeholder = SwapItem([spacer, img])
			self.placeholders.append(placeholder)
			spacer.hAlign = align
			placeholder.hAlign = align
			return [placeholder]
		else:
			return [img]
	
	def beforeLastBuild(self, *args, **kwargs):
		if self.renderOnLastBuild:
			for p in self.placeholders:
				p.current = 1
