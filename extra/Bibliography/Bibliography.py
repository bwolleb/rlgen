import os

from core.modules import ModuleInterface
from core import utils

import pybtex.database
from pybtex.style.formatting.plain import Style as PlainStyle
from pybtex.backends.plaintext import Backend as PlainBackend



#### Custom backend, copied from the HTML backend: https://bitbucket.org/pybtex-devs/pybtex/src/master/pybtex/backends/html.py
from xml.sax.saxutils import escape
import pybtex.io
from pybtex.backends import BaseBackend
class CustomBackend(BaseBackend):
	default_suffix = '.html'
	symbols = {
		'ndash': u'&ndash;',
		'newblock': u'\n',
		'nbsp': u'&nbsp;'
	}

	def format_str(self, text):
		return escape(text)

	def format_tag(self, tag, text):
		return r'<{0}>{1}</{0}>'.format(tag, text) if text else u''

	@staticmethod
	def format_href(url, text, external=False):
		target = ' target="_blank"' if external else ''
		return r'<a href="{0}"{1}>{2}</a>'.format(url, target, text) if text else u''

	def write_entry(self, key, label, text):
		self.output(u'<dt>%s</dt>\n' % label)
		self.output(u'<dd>%s</dd>\n' % text)

BACKENDS = {"plain": PlainBackend, "custom": CustomBackend}

class Bibliography(ModuleInterface):
	def __init__(self, engine, backend="custom", numFormat="[{num}]"):
		super().__init__(engine)
		self.db = None
		self.used = []
		self.backend = backend
		self.numFormat = numFormat
		engine.resources["biblio"] = {}

		# Register as text processor if available
		txtProc = engine.getModule("core.modules.TextProcessor")
		if txtProc is not None:
			txtProc.processors["cite"] = self.processor

	def processor(self, engine, ref, kind="no"):
		if ref not in self.used:
			self.used.append(ref)
		if ref in self.engine.resources["biblio"]:
			entry = self.engine.resources["biblio"][ref]
			txt = ""
			if kind == "al":
				return True, entry["author"]
			elif kind == "authors":
				return True, entry["authors"]
			elif kind == "title":
				return True, entry["title"]
			elif kind == "no":
				if entry["num"] is not None:
					txt = self.numFormat.format(num=entry["num"])
					if entry["link"] is not None:
						txt = "<a href=\"#{}\">{}</a>".format(entry["link"], txt)
					return True, txt
		return False, ""

	def identifier(self):
		return "extra.Bibliography"

	def handles(self):
		return ["bib", "bibliography"]

	def formatAuthor(self, entry):
		authors = entry.persons["author"]
		names = authors[0].last_names
		txt = str.join(" ", names)
		if len(authors) > 1:
			txt += " et al."
		return txt

	def formatAuthors(self, entry):
		style = PlainStyle()
		formatter = style.format_names("author")
		txt = formatter.format_data({"entry": entry, "style": style, "bib_data": None})
		if txt.endswith("."):
			txt = txt[:-1]
		return txt

	def formatTitle(self, entry):
		style = PlainStyle()
		title = style.format_title(entry, "title")
		txt = title.format_data({"entry": entry, "style": style, "bib_data": None})
		if txt.endswith("."):
			txt = txt[:-1]
		return txt

	def formatFull(self, entry):
		style = PlainStyle()
		backend = BACKENDS[self.backend]()
		fEntry = style.format_entry("", entry)
		return fEntry.text.render(backend)

	def process(self, block, path):
		biblioData = self.engine.resources["biblio"]

		if block["type"] == "bib":
			fullpath = os.path.join(path, block["path"])
			if not os.path.isfile(fullpath):
				utils.error("Can not open " + fullpath)
				return []

			db = pybtex.database.parse_file(fullpath)
			if self.db is None:
				self.db = db
			else:
				self.db.entries.update(db.entries)
			
			for k in db.entries:
				entry = db.entries[k]
				data = {}
				data["author"] = self.formatAuthor(entry)
				data["authors"] = self.formatAuthors(entry)
				data["title"] = self.formatTitle(entry)
				data["formatted"] = self.formatFull(entry)
				data["num"] = None
				data["link"] = None
				biblioData[k] = data

			return []
		elif block["type"] == "bibliography":
			textModule = self.engine.getModule("core.modules.Text")
			bookmarkModule = self.engine.getModule("core.modules.Bookmark")
			formatted = []
			if textModule is not None:
				keys = self.used if "render" in block and block["render"] == "used" else list(self.db.entries.keys())
				i = 1
				for k in keys:
					entry = biblioData[k]
					uid = utils.uid()
					entry["num"] = i
					entry["link"] = uid
					if bookmarkModule is not None:
						formatted.append(bookmarkModule.buildBookmark(uid))
					label = self.numFormat.format(num=i)
					par = textModule.buildText(label + " " + entry["formatted"])
					formatted.append(par)
					i += 1
			return formatted
