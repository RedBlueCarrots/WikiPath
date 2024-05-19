import requests
import json
from .utilities import *

def checkArticlesExists(pathList):
	#Converts list of articles into a formatted string (art1|art2|art3), using pathify from utilities.py
	pathString = pathify(pathList)
	#Make api call using this string - | will allow for multiple searches at once
	#Wikipedia API handles normalizing the data format
	query = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles="+pathString+"&format=json&formatversion=2")
	queryJson = json.loads(query.text)
	articleInfo = {}
	#Redundancy check to ensure api response contains expected information
	if "query" in queryJson and "pages" in queryJson["query"]:
		#reconvert from normalised to original form (Used on js side for error messages)
		if "normalized" in queryJson["query"]:
			for article in queryJson["query"]["pages"]:
				for normalised in queryJson["query"]["normalized"]:
					if normalised["to"] == article["title"]:
						article["title"] = normalised["from"]
		for article in queryJson["query"]["pages"]:
			articleInfo[article["title"]] = not "missing" in article
	return articleInfo

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
			hasNext = False
			if "links" in pathInfo["query"]["pages"][currentId]:
				for link in pathInfo["query"]["pages"][currentId]["links"]:
					if link["title"] == normalized[pathList[path+1]]:
						hasNext = True
						break
			pathReport[pathList[path]] = hasNext
			print(pathList[path] + " to " + pathList[path+1], hasNext)
	pathReport[pathList[len(pathList)-1]] = True
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