import os
import re

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import XPreformatted

syntaxDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syntax")

def insertPos(tag, tags):
	beg, end = tag[0], tag[1]
	for i in range(len(tags)):
		t = tags[i]
		if (beg >= t[0] and beg <= t[1]) or (end >= t[0] and end <= t[1]):
			return -1
		if end < t[0]:
			return i
		elif i == len(tags) - 1:
			return i + 1
	return 0

class Listings(ModuleInterface):
	def __init__(self, engine, font=None):
		super().__init__(engine)
		self.font = font
		self.syntax = {}

		for filename in os.listdir(syntaxDir):
			lang, ext = os.path.splitext(filename)
			self.syntax[lang] = utils.loadFile(os.path.join(syntaxDir, filename))

	def identifier(self):
		return "extra.Listings"

	def handles(self):
		return ["lst"]

	def process(self, block, path):
		if "font" in block and block["font"] in self.engine.fonts:
			font = self.engine.fonts[block["font"]]
		elif self.font is not None:
			font = self.engine.fonts[self.font]
		else:
			textModule = self.engine.getModule("core.modules.Text")
			font = textModule.getDefaultFont()

		txt = block["content"]
		# Because XPreformatted would try to process lines like #include <someting.h>
		txt = txt.replace("&", "&amp;")
		txt = txt.replace("<", "&lt;")
		txt = txt.replace(">", "&gt;")
		
		syntax = None
		if "syntax" in block:
			s = block["syntax"]
			if type(s) is str:
				syntax = self.syntax[s]
			elif type(s) is dict:
				syntax = utils.loadFile(os.path.join(path, s["path"]))
				self.syntax[s["name"]] = syntax

		if syntax is not None:
			rules = syntax["match"]

			tags = []
			for (reg, key) in rules:
				markupRe = re.compile(reg)
				match = markupRe.search(txt, 0)
				while match is not None:
					beg, end = match.span(0)
					tag = (beg, end, key)
					p = insertPos(tag, tags)
					if p >= 0:
						tags.insert(p, tag)
					match = markupRe.search(txt, end)

			processed = txt
			if len(tags) > 0:
				prev = 0
				processed = ""
				for t in tags:
					beg, end, key = t
					processed += txt[prev:beg]
					sub = txt[beg:end]
					if key in syntax["italic"]:
						sub = "<i>" + sub + "</i>"
					if key in syntax["bold"]:
						sub = "<b>" + sub + "</b>"
					if key in syntax["color"]:
						sub = "<font color='" + syntax["color"][key] + "'>" + sub + "</font>"
					processed += sub
					prev = end
				processed += txt[prev:]
			return [XPreformatted(processed, font)]
		return [XPreformatted(txt, font)]
