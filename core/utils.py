import sys
import os
import json
import yaml
import hashlib
import datetime
import re
import csv

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib import colors

AcceptedDataTypes = [".json", ".yaml"]

_idPrefix = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).hexdigest()
_lastId = 0

def uid():
	global _lastId
	_lastId += 1
	return _idPrefix + str(_lastId)

def error(txt):
	print(txt, file=sys.stderr)

def loadJson(path):
	f = open(path, encoding="utf8")
	data = json.load(f)
	f.close()
	return data

def loadYaml(path):
	f = open(path, encoding="utf8")
	data = yaml.load(f, Loader=yaml.FullLoader)
	f.close()
	return data

def guessCsvDelimiter(path):
	f = open(path, encoding="utf8")
	firstLine = f.readline()
	firstLine += f.readline()
	firstLine += f.readline()
	firstLine += f.readline()
	firstLine += f.readline()
	f.close()
	
	delimiters = [";", ","]
	scores = [len(firstLine.split(delim)) for delim in delimiters]
	return delimiters[scores.index(max(scores))]

def loadCsv(path):
	delim = guessCsvDelimiter(path)
	f = open(path, encoding="utf8")
	reader = csv.reader(f, delimiter=delim)
	data = list(reader)
	f.close()
	return data

def getExt(filename):
	name, ext = os.path.splitext(filename)
	return ext.lower()

def loadFile(path):
	ext = getExt(path)
	
	if ext == ".json":
		return loadJson(path)
	elif ext == ".yaml":
		return loadYaml(path)
	elif ext == ".csv":
		return loadCsv(path)
	else:
		error("Unsupported file type: " + path)
	return None

def alignFromTxt(text):
	text = text.strip().upper()
	if text == "LEFT": return TA_LEFT
	elif text == "CENTER": return TA_CENTER
	elif text == "RIGHT": return TA_RIGHT
	elif text == "JUSTIFY": return TA_JUSTIFY
	else: return TA_LEFT

def hexcolor(string):
	if not string.startswith("#"): string = "#" + string
	hasAlpha = len(string) == 9
	return colors.HexColor(string, hasAlpha=hasAlpha)

def getData(data, ref):
	tableRegex = re.compile("^([^\[\]]+)\[(\d+)\]$")
	parts = ref.split("/")
	alias = parts[0]
	path = parts[1:]
	
	if data is None or alias not in data:
		return None
	
	resource = data[alias]
	for child in path:
		result = tableRegex.findall(child)
		if len(result) > 0:
			(key, index) = result[0]
			resource = resource[key][int(index)]
		else:
			try:
				resource = resource[child]
			except:
				return None
	return resource
