from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Flowable

class BookmarkItem(Flowable):
	def __init__(self, name):
		super().__init__()
		self.name = name

	def draw(self):
		self.canv.bookmarkPage(self.name)

class Bookmark(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["name"]
		engine.resources["bookmarks"] = {}
	
	def identifier(self):
		return "core.modules.Bookmark"
	
	def handles(self):
		return ["bookmark"]
	
	def registerBookmark(self, name):
		uid = utils.uid()
		self.engine.resources["bookmarks"][name] = uid
		return uid
	
	def buildBookmark(self, uid):
		return BookmarkItem(uid)
	
	def process(self, block, path):
		name = block["name"]
		return [self.buildBookmark(self.registerBookmark(name))]
