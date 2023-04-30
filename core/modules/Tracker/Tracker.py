from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Flowable

class TrackerItem(Flowable):
	def __init__(self, key, res):
		super().__init__()
		self.key = key
		self.res = res

	def draw(self):
		res = self.res
		path = self.key.split("/")
		for p in path[:-1]:
			if p not in res:
				res[p] = {}
			res = res[p]
		res[path[-1]] = self.canv.getPageNumber()
		print("Tracking", self.key, res[path[-1]])

class Tracker(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)

	def identifier(self):
		return "core.modules.Tracker"

	def handles(self):
		return ["track"]

	def process(self, block, path):
		return [TrackerItem(block["id"], self.engine.resources)]
