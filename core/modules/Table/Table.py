from core.modules import ModuleInterface
from core import utils
import copy

import reportlab.platypus
from reportlab.lib.units import cm
from reportlab.lib import colors

defaultStyle = [('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'TOP')]
defaultBorderStyle = ("GRID", (0,0), (-1,-1), 0.5, colors.black)
defaultHeaderStyle = ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)

class Table(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["rows"]
		
	def identifier(self):
		return "core.modules.Table"
	
	def handles(self):
		return ["table"]
	
	def processCell(self, cell, path):
		textModule = self.engine.getModule("core.modules.Text")
		
		if type(cell) is str and textModule is not None:
			return textModule.buildText(cell)
		elif type(cell) is dict:
			return self.engine.processBlock(cell, path)
		elif type(cell) is list:
			return self.engine.processBlocks(cell, path)
		
		return reportlab.platypus.NullDraw()
	
	def process(self, block, path):
		# Get rows data
		rowsData = block["rows"]
		if type(rowsData) is str:
			rowsData = utils.getData(self.engine.resources, rowsData)
			if rowsData is None:
				utils.error("Could not get resource: " + rowsData)
				return []
		
		if type(rowsData) is not list:
			utils.error("Rows data must be a list")
			return []
		
		# Process rows content
		keys = block["keys"] if "keys" in block else []
		rows = []
		style = copy.deepcopy(defaultStyle)
		
		for row in rowsData:
			cols = []
			
			if type(row) is dict and len(keys) > 0:
				# Process with keys
				for k in keys:
					cell = row[k]
					cols.append(self.processCell(cell, path))
			elif type(row) is list:
				for cell in row:
					cols.append(self.processCell(cell, path))
			
			rows.append(cols)
		
		# Process header if any
		if "header" in block:
			header = []
			for col in block["header"]:
				header.append(self.processCell(col, path))
			rows.insert(0, header)
			style.append(defaultHeaderStyle)
		
		# Process style
		if "border" not in block or block["border"]:
			style.append(defaultBorderStyle)
		
		# If style is specified, override it all. Style can be a path to a resource
		if "style" in block:
			requiredStyle = block["style"]
			if type(requiredStyle) is str:
				requiredStyle = utils.getData(self.engine.resources, requiredStyle)
			if type(requiredStyle) is list:
				style = requiredStyle
		
		
		# Process column widths
		frameWidth = 0
		pageStyleModule = self.engine.getModule("core.modules.PageStyle")
		
		if pageStyleModule is not None and pageStyleModule.currentPageTemplate is not None:
			framdIdx = block["frame"] if "frame" in block else 0
			frameWidth = pageStyleModule.currentPageTemplate.frames[framdIdx]._width
		
		nbCols = len(rows[0])
		
		unit = cm
		if "unit" in block:
			if block["unit"] == "cm": unit = cm
			elif block["unit"] == "mm": unit = mm
			elif block["unit"] == "percent": unit = frameWidth/100
		
		widths = [frameWidth / nbCols] * nbCols
		if "widths" in block:
			widths = [w * unit for w in block["widths"]]
		
		heights = None
		if "heights" in block:
			heights = [h * unit for h in block["heights"]]
		
		# Finally, build table
		align = block["align"] if "align" in block else None
		repeatRows = block["repeatRows"] if "repeatRows" in block else 0
		table = reportlab.platypus.Table(rows, colWidths=widths, rowHeights=heights, repeatRows=repeatRows, hAlign=align)
		table.setStyle(reportlab.platypus.TableStyle(style))
		
		return [table]
