from core.modules import ModuleInterface
from core import utils

from reportlab.platypus import Flowable

class MetadataItem(Flowable):
    def __init__(self, title="", author="", subject="", keywords="", creator="", producer=""):
        super().__init__()
        self.title = title
        self.author = author
        self.subject = subject
        self.keywords = keywords
        self.creator = creator
        self.producer = producer

    def draw(self):
        infos = self.canv._doc.info
        infos.title = self.title
        infos.author = self.author
        infos.subject = self.subject
        infos.keywords = self.keywords
        infos.creator = self.creator
        infos.producer = self.producer

class Metadata(ModuleInterface):
	def __init__(self, engine):
		super().__init__(engine)
	
	def identifier(self):
		return "core.modules.Metadata"
	
	def handles(self):
		return ["meta"]
	
	def process(self, block, path):
		metadata = MetadataItem(block["title"] if "title" in block else "",
		block["author"] if "author" in block else "",
		block["subject"] if "subject" in block else "",
		block["keywords"] if "keywords" in block else "",
		block["creator"] if "creator" in block else "rlgen",
		block["producer"] if "producer" in block else "ReportLab PDF Library")
		return [metadata]
