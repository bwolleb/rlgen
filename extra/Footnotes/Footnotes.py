from io import BytesIO

from core.modules import ModuleInterface
from core import utils

import reportlab.platypus
from reportlab.lib.units import cm
from reportlab.lib import colors

DEFAULT_NUMFORMAT = "<para align='right'>{num}. </para>"
DEFAULT_INLINEFORMAT = "[{num}]"
DEFAULT_STYLE = []
DEFAULT_STYLE.append(("VALIGN", (0,0), (0,-1), "TOP"))
DEFAULT_STYLE.append(("TOPPADDING", (0,0), (-1,0), 3))
DEFAULT_STYLE.append(("TOPPADDING", (0,1), (-1,-1), 1))
DEFAULT_STYLE.append(("BOTTOMPADDING", (0,0), (-1,-1), 1))
DEFAULT_STYLE.append(("RIGHTPADDING", (0,0), (-1,-1), 0))
DEFAULT_STYLE.append(("LEFTPADDING", (0,0), (0,-1), 0))
DEFAULT_STYLE.append(("LEFTPADDING", (1,0), (1,-1), 4))

class FNote(reportlab.platypus.Flowable):
	def __init__(self, fnId, content, callback):
		super().__init__()
		self.fnId = fnId
		self.content = content
		self.callback = callback

	def draw(self):
		self.callback(self.fnId, self.content)

class Footnotes(ModuleInterface):
	def __init__(self, engine, counting=True, width=None, maxHeight=None, x=None, y=1*cm, style=DEFAULT_STYLE, font=None,
				 counterWidth=0.5*cm, numFormat=DEFAULT_NUMFORMAT, inlineFormat=DEFAULT_INLINEFORMAT, preprocess=["text", "txt"],
				 warnOverlap=True, lineWidth=1, lineThickness=0.5, lineColor="000000"):
		super().__init__(engine)
		txtProc = engine.getModule("core.modules.TextProcessor")
		if txtProc is None:
			utils.error("The TextProcessor is not loaded, footnotes won't work")
		else:
			txtProc.processors["fn"] = self.processor

		if isinstance(preprocess, list):
			for blockType in preprocess:
				engine.preprocessing[blockType].append(self.preprocessor)

		engine.pageEndCallbacks.append(self.pageEnd)
		engine.beforeBuildCallbacks.append(self.buildBegins)

		self.builder = None
		self.onPage = []
		self.refs = {}
		self.counting = counting
		self.counter = 0
		self.warnOverlap = warnOverlap

		# Drawing parameters
		self.width = width
		self.maxHeight = maxHeight
		self.x = x
		self.y = y
		self.style = style
		self.counterWidth = counterWidth
		self.numFormat = numFormat
		self.inlineFormat = inlineFormat
		self.font = font
		self.lineWidth = lineWidth
		self.lineThickness = lineThickness
		self.lineColor = lineColor

	def processor(self, engine, *fnids):
		for fnid in fnids:
			if fnid not in self.refs:
				return False, ""
		num = str.join(",", [str(self.refs[fnid]) for fnid in fnids])
		return True, self.inlineFormat.format(num=num)

	def preprocessor(self, block, path):
		notes = {}
		processed = []
		for kw in ["fn", "note", "notes", "footnote", "footnotes"]:
			if kw in block:
				entry = block[kw]
				if type(entry) is str:
					notes[utils.uid()] = entry
				elif type(entry) is dict:
					notes.update(entry)
		for nid in notes:
			processed += self.process({"id": nid, "content": notes[nid]}, path)
		return processed

	def pageEnd(self, engine, builder, canvas):
		if len(self.onPage) > 0:
			textModule = self.engine.getModule("core.modules.Text")
			widths = [self.counterWidth, self.width - self.counterWidth] if self.counting else [self.width]
			rows = []
			for n in self.onPage:
				num, content = n
				row = []
				if self.counting:
					row.append(textModule.buildText(self.numFormat.format(num=num), self.font))
				row.append(content)
				rows.append(row)
			tbl = reportlab.platypus.Table(rows, colWidths=widths)
			tbl.setStyle(reportlab.platypus.TableStyle(self.style))
			w, h = tbl.wrap(self.width, self.maxHeight)

			# Draw line
			canvas.setLineWidth(self.lineThickness)
			canvas.setStrokeColor(utils.hexcolor(self.lineColor))
			canvas.line(self.x, self.y + h, self.x + self.lineWidth * self.builder.frame._width, self.y + h)

			if self.warnOverlap and self.builder.frame._y <= self.y + h:
				height = (self.y + h) - self.builder.frame._y
				heightCm = round(height / cm, 2)
				utils.error("Warning, potential footnote overlap detected on page: " + str(canvas.getPageNumber()) + " (" + str(heightCm) + " cm)")
			tbl.drawOn(canvas, self.x, self.y)
			self.onPage = []

	def buildBegins(self, engine, builder, blocks):
		self.builder = builder
		defaultFrame = None

		pageStyleModule = self.engine.getModule("core.modules.PageStyle")
		if pageStyleModule is not None and pageStyleModule.currentPageTemplate is not None:
			defaultFrame = pageStyleModule.currentPageTemplate.frames[0]

		if self.width is None:
			self.width = defaultFrame._width
		if self.maxHeight is None:
			self.maxHeight = self.width / 2
		if self.x is None:
			self.x = defaultFrame._x1

	def addNote(self, fnId, content):
		self.onPage.append((self.refs[fnId], content))

	def identifier(self):
		return "extra.Footnotes"

	def handles(self):
		return ["footnote", "fn"]

	def process(self, block, path):
		textModule = self.engine.getModule("core.modules.Text")
		content = block["content"]
		processed = None
		fnId = block["id"] if "id" in block else utils.uid()

		if type(content) is str and textModule is not None:
			processed = textModule.buildText(content, self.font)
		elif type(content) is dict:
			processed = self.engine.processBlock(content, path)
		elif type(content) is list:
			processed = self.engine.processBlocks(content, path)
		else:
			utils.error("Unsupported content in footnote")

		if self.counting:
			self.counter += 1
		self.refs[fnId] = self.counter

		return [FNote(fnId, processed, self.addNote)]
