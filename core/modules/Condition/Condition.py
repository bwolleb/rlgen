from core.modules import ModuleInterface
from core import utils
import copy

class Condition(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
		self.mandatoryArgs = ["condition", "then"]
	
	def identifier(self):
		return "core.modules.Condition"
	
	def handles(self):
		return ["if"]
	
	def process(self, block, path):
		then = block["then"]
		otherwise = block["else"] if "else" in block else []
		
		# Eval condition
		exprData = copy.deepcopy(self.engine.resources)
		exprVar = "_" + utils.uid()
		exec("{} = {}".format(exprVar, block["condition"]), {}, exprData)
		exprOk = exprData[exprVar]
		
		return self.engine.processBlocks(then if exprOk else otherwise, path)
