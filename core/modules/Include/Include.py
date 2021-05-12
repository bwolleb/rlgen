import os
import re

from core.modules import ModuleInterface
from core import utils

supportedFilesRe = re.compile(".*[.](json|yaml)$")

class Include(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["path"]
	
	def identifier(self):
		return "core.modules.Include"
	
	def handles(self):
		return ["include"]
	
	def processFile(self, path, filename):
		fullpath = os.path.join(path, filename)
		if os.path.isfile(fullpath):
			data = utils.loadFile(fullpath)
			if type(data) is list:
				return self.engine.processBlocks(data, path)
			elif type(data) is dict:
				return self.engine.processBlock(data, path)
		return []
	
	def processFolder(self, path, matcher, recursive=False):
		processed = []
		for filename in sorted(os.listdir(path)):
			fullpath = os.path.join(path, filename)
			if os.path.isfile(fullpath) and matcher.match(fullpath) is not None:
				processed += self.processFile(path, filename)
			elif os.path.isdir(fullpath) and recursive:
				processed += self.processFolder(fullpath, matcher, recursive)
		return processed

	def process(self, block, path):
		name = block["path"]
		matcher = re.compile(block["match"]) if "match" in block else supportedFilesRe
		fullpath = os.path.join(path, name)
		if os.path.isfile(fullpath) and matcher.match(fullpath) is not None:
			return self.processFile(path, name)
		elif os.path.isdir(fullpath):
			return self.processFolder(fullpath, matcher, block["recursive"] if "recursive" in block else False)
		return []
