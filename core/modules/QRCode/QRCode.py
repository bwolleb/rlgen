from core.modules import ModuleInterface
from core import utils

from reportlab.graphics.barcode.qr import QrCode
from reportlab.lib.units import cm
from reportlab.lib import colors

class CustomQRCode(QrCode):
	def __init__(self, data, color, **kw):
		super().__init__(data, **kw)
		self.color = color
	
	def rect(self, x, y, w, h):
		self.canv.setFillColor(self.color)
		self.canv.rect(x, y, w, h, stroke=0, fill=1)

class QRCode(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["data", "width"]
	
	def identifier(self):
		return "core.modules.QRCode"
	
	def handles(self):
		return ["qr"]
	
	def process(self, block, path):
		data = block["data"]
		color = utils.hexcolor(block["color"]) if "color" in block else colors.black
		width = block["width"]*cm
		height = block["height"]*cm if "height" in block else width
		border = block["border"] if "border" in block else 1
		level = block["level"] if "level" in block else "L"
		version = block["version"] if "version" in block else None
		return [CustomQRCode(data, color, width=width, height=height, qrBorder=border, qrLevel=level, qrVersion=version)]
