from core import utils
import datetime

def dataProcessor(engine, arg):
	data = utils.getData(engine.resources, arg)
	return data is not None, data

def chapterProcessor(engine, arg, label="fulltext"):
	if "chapters" in engine.resources:
		if arg in engine.resources["chapters"]["id"]:
			chapterData = engine.resources["chapters"]["id"][arg]
			txt = chapterData[label]
			link = chapterData["link"]
			return True, "<a href=\"#{}\">{}</a>".format(link, txt)
	return False, ""

def bookmarkProcessor(engine, bookmark, text):
	if "bookmarks" in engine.resources:
		if bookmark in engine.resources["bookmarks"]:
			return True, "<a href=\"#{}\">{}</a>".format(engine.resources["bookmarks"][bookmark], text)
	return False, ""

def buildDate(engine, form):
	formatting = form if form != "" else "%d.%m.%Y %H:%M:%S"
	return True, datetime.datetime.now().strftime(formatting)

def increment(engine, name, key=None):
	if "counters" not in engine.resources:
		engine.resources["counters"] = {}
	counters = engine.resources["counters"]
	if name not in counters:
		counters[name] = 0
	counters[name] += 1
	val = counters[name]
	formatted = str(val)
	if key is not None:
		if "countersRef" not in engine.resources:
			engine.resources["countersRef"] = {}
		engine.resources["countersRef"][key] = val
		bookmarkModule = engine.getModule("core.modules.Bookmark")
		if bookmarkModule is not None:
			uid = bookmarkModule.registerBookmark(key)
			formatted = "<a name=\"{}\"/>".format(uid) + formatted
	return True, formatted

def counterRef(engine, key, text=""):
	if len(text) > 0:
		text += " "
	if "countersRef" not in engine.resources:
		return False, ""
	if key not in engine.resources["countersRef"]:
		return False, ""
	val = engine.resources["countersRef"][key]
	formatted = text + str(val)
	if "bookmarks" in engine.resources and key in engine.resources["bookmarks"]:
		formatted = "<a href=\"#{}\">{}{}</a>".format(engine.resources["bookmarks"][key], text, val)
	return True, formatted

Processors = {}
Processors["data"] = dataProcessor
Processors["chapter"] = chapterProcessor
Processors["ref"] = bookmarkProcessor
Processors["now"] = buildDate
Processors["inc"] = increment
Processors["cnt"] = counterRef
