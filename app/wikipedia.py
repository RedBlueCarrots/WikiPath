import requests
import json
from .utilities import *

def checkArticleExists(articleName):
	if articleName == "":
		return True
	query = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles="+str(articleName)+"&format=json&formatversion=2")
	queryJson = json.loads(query.text)
	return not "missing" in queryJson["query"]["pages"][0]

def checkArticlesExists(pathList):
	pathString = pathify(pathList)
	query = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles="+pathString+"&format=json&formatversion=2")
	queryJson = json.loads(query.text)
	articleInfo = {}
	#reconvert from normalised to original form
	if "normalized" in queryJson["query"]:
		for article in queryJson["query"]["pages"]:
			for normalised in queryJson["query"]["normalized"]:
				if normalised["to"] == article["title"]:
					article["title"] = normalised["from"]
	for article in queryJson["query"]["pages"]:
		articleInfo[article["title"]] = not "missing" in article
	return articleInfo