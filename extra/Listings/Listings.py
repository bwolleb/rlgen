import os
import re

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import XPreformatted

class Listings(ModuleInterface):
	def __init__(self, engine, update="auto", backend="custom", numFormat="[{num}]"):
		super().__init__(engine)


	def identifier(self):
		return "extra.Listings"

	def handles(self):
		return ["lst"]

	def process(self, block, path):
		moduleDir = os.path.dirname(os.path.abspath(__file__))
		syntax = utils.loadFile(os.path.join(moduleDir, "python.yaml"))

		textModule = self.engine.getModule("core.modules.Text")
		txt = block["content"]

		for (reg, key) in syntax["match"]:
			print(reg)
			pos = 0
			markupRe = re.compile(reg)
			match = markupRe.search(txt, pos)
			while match is not None:
				beg, end = match.span(1)
				sub = match.groups()[0]

				if key in syntax["italic"]:
					sub = "<i>" + sub + "</i>"
				if key in syntax["bold"]:
					sub = "<b>" + sub + "</b>"
				if key in syntax["color"]:
					sub = "<font color='" + syntax["color"][key] + "'>" + sub + "</font>"
				txt = txt[:beg] + sub + txt[end:]

				pos = beg + len(sub)
				print("from", match.groups()[0], "TO", sub)
				match = markupRe.search(txt, pos)
		print("FINAL", txt)
		x = XPreformatted(txt, textModule.getDefaultFont())
		return [x]
