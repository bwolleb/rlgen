from core import utils
import datetime

def dataProcessor(engine, arg):
	data = utils.getData(engine.resources, arg)
	return data is not None, data

def chapterProcessor(engine, arg):
	if "chapters" in engine.resources:
		if arg in engine.resources["chapters"]["id"]:
			chapterData = engine.resources["chapters"]["id"][arg]
			txt = chapterData["fulltext"]
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

Processors = {}
Processors["data"] = dataProcessor
Processors["chapter"] = chapterProcessor
Processors["ref"] = bookmarkProcessor
Processors["now"] = buildDate
