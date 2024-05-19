import requests
import json
from .utilities import *

VALID = 0
MISSING = 1
INVALID = 2

#Only used for checking challenge creation
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

#We can check for article and path validity in a single wikipedia API call
def checkValidPath(pathList):
	#because of article verification, from list should be a | delimited string of all articles in path
	fromList = ""
	#To list won't contain the start article, as nothing needs to link to it
	toList = ""
	for index in range(len(pathList)-1):
		toList += pathList[index+1] + "|"
		fromList += pathList[index] + "|"
	fromList += pathList[len(pathList)-1]
	toList = toList.strip("|")
	#Wikipedia puts articles in normalized form (e.g. pasta->Pasta)
	#We need to be able to convert between these to interpret the api response, and report back to the user
	#normalized will be a dictionary, with normalized[article]=Normalized article
	normalized = {}
	for path in pathList:
		normalized[path] = path
	#Make the API call, see below
	pathInfo = checkArticleLink(fromList, toList)
	#will contain INVALID, MISSING, or VALID for every article
	pathReport = {}
	#Check the API response was valid
	if "query" in pathInfo and "pages" in pathInfo["query"]:
		if "normalized" in pathInfo["query"]:
			#for every article that wikipedia has normalized, update the normalized dictionary
			for num in pathInfo["query"]["normalized"]:
				normalized[num["from"]] = num["to"]
		#Check every article, except the last (nothing links from the last article), start and end have been validated before
		for path in range(len(pathList)-1):
			currentId  = 0
			#Search through the API response for info about the current article in the loop
			for pageId in pathInfo["query"]["pages"]:
				if pathInfo["query"]["pages"][pageId]["title"]==normalized[pathList[path]]:
					currentId = pageId
					break
			#assume invalid unless otherwise found
			state = INVALID
			#Prioritise missing pages for the report
			if "missing" in pathInfo["query"]["pages"][currentId]:
				state = MISSING
			elif "links" in pathInfo["query"]["pages"][currentId]:
				#check found links to see if next article is a valid link
				for link in pathInfo["query"]["pages"][currentId]["links"]:
					if link["title"] == normalized[pathList[path+1]]:
						state = VALID
						break
			pathReport[pathList[path]] = state
		#can safely assume the end article is valid, include in the dictionary so nothing breaks later
		pathReport[pathList[len(pathList)-1]] = VALID
	return pathReport

def checkArticleLink(from_article, to_article):
	url = "https://en.wikipedia.org/w/api.php"
	url += "?action=query"
	url += "&format=json"
	url += "&titles="+from_article
	url += "&prop=links"
	#will only return links to articles listed in the pltitles prop
	url += "&pltitles="+to_article
	url += "&pllimit=max"
	query = requests.get(url)
	return json.loads(query.text)