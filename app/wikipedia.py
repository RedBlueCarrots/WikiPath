import requests
import json
from .utilities import *

VALID = 0
MISSING = 1
INVALID = 2

def checkValidPath(pathList):
	fromList = ""
	toList = ""
	for index in range(len(pathList)-1):
		toList += pathList[index+1] + "|"
		fromList += pathList[index] + "|"
	fromList += pathList[len(pathList)-1]
	toList = toList.strip("|")
	normalized = {}
	for path in pathList:
		normalized[path] = path
	pathInfo = checkArticleLink(fromList, toList)
	pathReport = {}
	if "query" in pathInfo:
		if "normalized" in pathInfo["query"]:
			for num in pathInfo["query"]["normalized"]:
				normalized[num["from"]] = num["to"]
		for path in range(len(pathList)-1):
			currentId  = 0
			for pageId in pathInfo["query"]["pages"]:
				if pathInfo["query"]["pages"][pageId]["title"]==normalized[pathList[path]]:
					currentId = pageId
					break
			state = INVALID
			if "missing" in pathInfo["query"]["pages"][currentId]:
				state = MISSING
			elif "links" in pathInfo["query"]["pages"][currentId]:
				for link in pathInfo["query"]["pages"][currentId]["links"]:
					if link["title"] == normalized[pathList[path+1]]:
						state = VALID
						break
			pathReport[pathList[path]] = state
			print(pathList[path] + " to " + pathList[path+1], state)
	pathReport[pathList[len(pathList)-1]] = VALID
	return pathReport

def checkArticleLink(from_article, to_article):
	url = "https://en.wikipedia.org/w/api.php"
	url += "?action=query"
	url += "&format=json"
	url += "&titles="+from_article
	url += "&prop=links"
	url += "&pltitles="+to_article
	url += "&pllimit=max"
	query = requests.get(url)
	print(url)
	return json.loads(query.text)
	return False