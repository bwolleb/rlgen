import os
import re

from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import XPreformatted

syntaxDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syntax")

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

	# Detect comments so that they don't get formatted
	def isInComments(self, txt, commentRegs, start):
		comments = []
		pos = 0
		for reg in commentRegs:
			commentsRe = re.compile(reg)
			match = commentsRe.search(txt, pos)
			while match is not None:
				beg, end = match.span(1)
				if start >= beg and start < end:
					return True
				if start < beg:
					return False
				match = commentsRe.search(txt, end)
		return False

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
		txt = txt.replace("<", "&lt;")
		txt = txt.replace(">", "&gt;")
		txt = txt.replace("&", "&amp;")
		
		syntax = None
		if "syntax" in block:
			s = block["syntax"]
			if type(s) is str:
				syntax = self.syntax[s]
			elif type(s) is dict:
				syntax = utils.loadFile(os.path.join(path, s["path"]))
				self.syntax[s["name"]] = syntax

		if syntax is not None:
			comments = syntax["comments"]
			rules = syntax["match"]
			rules += [(reg, "comments") for reg in comments]

			for (reg, key) in rules:
				pos = 0
				markupRe = re.compile(reg)
				match = markupRe.search(txt, pos)
				while match is not None:
					beg, end = match.span(1)
					sub = match.groups()[0]
					if key == "comments" or not self.isInComments(txt, comments, beg):
						if key in syntax["italic"]:
							sub = "<i>" + sub + "</i>"
						if key in syntax["bold"]:
							sub = "<b>" + sub + "</b>"
						if key in syntax["color"]:
							sub = "<font color='" + syntax["color"][key] + "'>" + sub + "</font>"
						txt = txt[:beg] + sub + txt[end:]
					pos = beg + len(sub)
					match = markupRe.search(txt, pos)

		x = XPreformatted(txt, font)
		return [x]
