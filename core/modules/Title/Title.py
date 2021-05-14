from collections import defaultdict
from core.modules import ModuleInterface
from core import utils
from .formatters import Formatters

class Title(ModuleInterface):
	def __init__(self, engine, styles=[], levelSep=".", numberingEnd=". "):
		super().__init__(engine)
		self.chapterStyles = styles
		self.levelSep = levelSep
		self.numberingEnd = numberingEnd
		self.levelFormatters = defaultdict(lambda: Formatters["1"])
		self.customFormatters = defaultdict(lambda: None)
		
		self.mandatoryArgs = {}
		self.mandatoryArgs["title"] = ["text"]
		self.mandatoryArgs["titleStyle"] = ["style"]
		self.mandatoryArgs["titleNum"] = ["num"]
		self.mandatoryArgs["titleFormat"] = ["format"]
		
		chaptersData = {}
		chaptersData["counters"] = []
		chaptersData["id"] = {}
		chaptersData["current"] = None
		
		engine.resources["chapters"] = chaptersData
	
	def identifier(self):
		return "core.modules.Title"
	
	def handles(self):
		return ["title", "chapter", "titleStyle", "titleNum", "titleFormat"]
	
	def formatLevel(self, level, num):
		return self.levelFormatters[level](num)
	
	def formatLevels(self, levels):
		level = len(levels) - 1
		formatter = self.customFormatters[level]
		if formatter is not None:
			lvlDict = {}
			for i in range(level + 1):
				lvlDict["t" + str(i)] = self.formatLevel(i, levels[i])
			lvlDict["current"] = self.formatLevel(len(levels) - 1, levels[-1])
			return self.customFormatters[level].format(**lvlDict)
		else:
			# Default formatting
			formatted = [str(self.formatLevel(i, levels[i])) for i in range(len(levels))]
			formatted = list(filter(lambda x: x != "", formatted))
			return str.join(self.levelSep, formatted)
	
	def process(self, block, path):
		if block["type"] == "title" or block["type"] == "chapter":
			text = block["text"]
			chapterId = block["id"] if "id" in block else utils.uid()
			displayText = text
			fullNumbering = None
			numbered = "numbered" not in block or block["numbered"]
			
			bookmarkModule = self.engine.modules["core.modules.Bookmark"] if "core.modules.Bookmark" in self.engine.modules else None
			textModule = self.engine.modules["core.modules.Text"] if "core.modules.Text" in self.engine.modules else None
			tocEntryModule = self.engine.modules["core.modules.TocEntry"] if "core.modules.TocEntry" in self.engine.modules else None
			
			chaptersData = self.engine.resources["chapters"]
			currentChapter = chaptersData["current"]
			levels = chaptersData["counters"]

			if "level" in block:
				level = block["level"]
			elif currentChapter is not None:
				level = currentChapter["level"]
			else:
				level = 0
			
			if currentChapter is None and level != 0 or currentChapter is not None and level - currentChapter["level"] > 1:
				utils.error("Title level can't jump")
				return []
			
			if numbered:
				# Create new level counter is needed
				if len(levels) < level + 1:
					levels.append(0)
				
				# Reset children levels if any
				for i in range(level + 1, len(levels)):
					levels[i] = 0
				
				# Increment current level
				levels[level] += 1
				
				# Process displayable number
				displayLevels = levels[:level + 1]
				fullNumbering = self.formatLevels(displayLevels)
				displayText = fullNumbering + self.numberingEnd + text
				
			
			chapterData = {}
			chapterData["text"] = text
			chapterData["id"] = chapterId
			chapterData["level"] = level
			chapterData["number"] = levels[level] if numbered else None
			chapterData["fullnumber"] = fullNumbering
			chapterData["fulltext"] = displayText
			chaptersData["id"][chapterId] = chapterData
			chaptersData["current"] = chapterData
			
			
			build = []
			
			if bookmarkModule is not None:
				link = bookmarkModule.registerBookmark(chapterId)
				chapterData["link"] = link
				build.append(bookmarkModule.buildBookmark(link))
			
			if textModule is not None:
				style = self.chapterStyles[level] if len(self.chapterStyles) > level else None
				build.append(textModule.buildText(displayText, style))
			
			if bookmarkModule is not None and tocEntryModule is not None and ("toc" not in block or block["toc"]):
				build.append(tocEntryModule.buildTocEntry(displayText, link, level))
			
			return build
		
		elif block["type"] == "titleStyle":
			style = block["style"]
			if type(style) is list:
				self.chapterStyles = block["style"]
			elif type(style) is str:
				self.chapterStyles[block["level"]] = style
			elif type(style) is dict:
				fontModule = self.engine.modules["core.modules.FontLoader"] if "core.modules.FontLoader" in self.engine.modules else None
				if fontModule is not None:
					newStyle = fontModule.buildFont(style)
					styleName = style["name"]
					self.engine.fonts[styleName] = newStyle
					self.chapterStyles[block["level"]] = styleName
		
		elif block["type"] == "titleNum":
			num = block["num"]
			if "level" in block:
				self.levelFormatters[block["level"]] = Formatters[num]
			elif type(num) is list:
				for i in range(len(num)):
					self.levelFormatters[i] = Formatters[num[i]]
			elif type(num) is str:
				self.levelFormatters = defaultdict(lambda: Formatters[num])
			elif type(num) is None:
				self.levelFormatters = defaultdict(lambda: Formatters["1"])

		elif block["type"] == "titleFormat":
			formatter = block["format"]
			if "level" in block:
				self.customFormatters[block["level"]] = formatter
			elif type(formatter) is list:
				for i in range(len(formatter)):
					self.customFormatters[i] = formatter[i]
			elif type(formatter) is str:
				self.customFormatters = defaultdict(lambda: formatter)
			elif formatter is None:
				self.customFormatters = defaultdict(lambda: None)
		return []
