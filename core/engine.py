import sys
import os

from collections import defaultdict
from core import utils
from .modules.ModuleLoader import Module as ModuleLoader
from .rl import DocTemplate, BuildTrigger

class Engine(object):
	def __init__(self):
		self.modules = {}
		self.blockHandlers = {}
		self.fonts = {}
		self.pagestyles = []
		self.resources = {}
		
		# Callbacks
		self.beforeBuildCallbacks = []
		self.buildBeginCallbacks = []
		self.buildEndCallbacks = []
		self.afterBuildCallbacks = []
		self.pageBeginCallbacks = []
		self.pageEndCallbacks = []
		self.preprocessing = defaultdict(list)

		self.moduleLoader = ModuleLoader(self)
		self.modules[self.moduleLoader.identifier()] = self.moduleLoader
		for blockType in self.moduleLoader.handles():
			self.blockHandlers[blockType] = self.moduleLoader.identifier()

	def processBlock(self, block, path):
		build = []
		
		if "type" in block:
			blockType = block["type"]
			if blockType in self.preprocessing:
				for preprocessor in self.preprocessing[blockType]:
					build += preprocessor(block, path)
			if blockType in self.blockHandlers:
				blockHandlerId = self.blockHandlers[blockType]
				build += self.modules[blockHandlerId].processBlock(block, path)
			else:
				utils.error("Warning, No module to handle " + blockType)
		else:
			utils.error("Warning, ignoring block because no type specified")
		
		return build

	def processBlocks(self, blocks, path):
		build = []
		for block in blocks:
			build += self.processBlock(block, path)
		return build

	def build(self, blocks, dest):
		self.resources["build"] = {}
		builder = DocTemplate(self, dest, self.pagestyles)
		blocks.append(BuildTrigger(self, builder))
		for c in self.beforeBuildCallbacks: c(self, builder, blocks)
		builder.multiBuild(blocks)
		for c in self.afterBuildCallbacks: c(self, builder)

	def getPageStyle(self, name):
		for ps in self.pagestyles:
			if ps.id == name:
				return ps
		return None
	
	def getModule(self, module, load=False):
		if module in self.modules:
			return self.modules[module]
		if load:
			return self.moduleLoader.loadModule(module)
		return None
