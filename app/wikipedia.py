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
	for index in range(len(pathList)):
		if index == len(pathList) - 1:
			return True
		
		links = getArticleLinks(pathList[index])

		if pathList[index + 1] not in links:
			return False

def getArticleLinks(article):
	links = []
	session = requests.Session()
	url = "https://en.wikipedia.org/w/api.php"
	params = {
		"action": "query",
		"format": "json",
		"titles": article,
		"prop": "links", 
		"pllimit": "max"
	}
	
	while True:
		response = session.get(url=url, params=params)
		data = response.json()
		pages = data["query"]["pages"]

		for key, value in pages.items():
			try:
				for link in value["links"]:
					print(link)
					links.append(link["title"])
			except KeyError:
				continue

		
		if "continue" in data:
			plcontinue = data["continue"]["plcontinue"]
			params["plcontinue"] = plcontinue
		else:
			break
	
	return links