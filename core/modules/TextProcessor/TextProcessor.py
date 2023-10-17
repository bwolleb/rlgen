import re

from core.modules import ModuleInterface
from core import utils
from .processors import Processors

markupRe = re.compile("{{\s*(.[a-z]*)\s*[(]\s*(.[-a-zA-Z0-9._\/\[\],% ]*)?\s*[)]\s*}}")
funcRe = re.compile("\s*(.[a-z]*)\s*[(]\s*(.[-a-zA-Z0-9._\/\[\],% ]*)?\s*[)]\s*")

class TextProcessor(ModuleInterface):
	def __init__(self, engine, processors=[]):
		super().__init__(engine)
		self.paragraphs = []
		self.processors = {}
		
		enabledProcessors = processors if len(processors) > 0 else Processors.keys()

		for p in enabledProcessors:
			if p in Processors:
				self.processors[p] = Processors[p]
			else:
				utils.error("Unknown text processor:" + p)
		
		if "core.modules.Text" in engine.modules:
			engine.modules["core.modules.Text"].buildTextCallbacks.append(self.newText)
		else:
			utils.error("Text module doesn ot seem to be loaded, text processors won't work")
		
		engine.buildBeginCallbacks.append(self.buildBegin)
		engine.afterBuildCallbacks.append(self.afterBuild)
	
	def buildBegin(self, engine, builder):
		remainingParagraphs = []
		for p in self.paragraphs:
			finished = self.processText(*p)
			if not finished:
				remainingParagraphs.append(p)
		self.paragraphs = remainingParagraphs

	def afterBuild(self, engine, builder):
		if len(self.paragraphs):
			print("Warning, there are", len(self.paragraphs), "unresolved text processor tags")
			for (par, data) in self.paragraphs:
				print(par.text)

	def newText(self, paragraph, data):
		if data is not None and "format" in data or len(markupRe.findall(paragraph.text)) > 0:
			finished = self.processText(paragraph, data)
			if not finished:
				self.paragraphs.append((paragraph, data))

	def processText(self, paragraph, data):
		if data is not None and "format" in data:
			form = data["format"]
			formattingValues = {}
			formatting = data["format"]
			ableToFormat = True
			
			for key in formatting:
				formatter = form[key]
				funcs = funcRe.findall(formatter)
				if len(funcs) > 0:
					func, arg = funcs[0]
					if arg is None: arg = ""
				else:
					func = "data"
					arg = formatter
				
				if func in self.processors:
					ok, result = self.processors[func](self.engine, *arg.split(","))
					formattingValues[key] = result
					ableToFormat = ableToFormat and ok
				else:
					ableToFormat = False
			
			if ableToFormat:
				try:
					paragraph.text = paragraph.text.format(**formattingValues)
					paragraph.__init__(paragraph.text, paragraph.style)
					return True
				except:
					return False
		
		if len(markupRe.findall(paragraph.text)) > 0:
			allProcessed = True
			pos = 0
			match = markupRe.search(paragraph.text, pos)
			while match is not None:
				beg, end = match.span()
				func, arg = match.groups()
				if arg is None: arg = ""
				
				if func in self.processors:
					ok, result = self.processors[func](self.engine, *arg.split(","))
					if ok:
						newString = paragraph.text[:beg] + str(result) + paragraph.text[end:]
						paragraph.text = newString
						paragraph.__init__(newString, paragraph.style)
					else:
						allProcessed = False
						pos = end
				match = markupRe.search(paragraph.text, pos)
			return allProcessed
		return True

	def identifier(self):
		return "core.modules.TextProcessor"
