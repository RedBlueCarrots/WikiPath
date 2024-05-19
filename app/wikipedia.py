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
	#from list should be a | delimited string of all articles in path
	fromList = ""
	for index in range(len(pathList)):
		fromList += pathList[index] + "|"
	fromList = fromList.strip("|")
	#Wikipedia puts articles in normalized form (e.g. pasta->Pasta)
	#We need to be able to convert between these to interpret the api response, and report back to the user
	#normalized will be a dictionary, with normalized[article]=Normalized article
	normalized = {}
	for path in pathList:
		normalized[path] = path
	#Make the first API call, to get all redirects
	normalInfo = getNormalized(fromList)

	if "query" in normalInfo and "pages" in normalInfo["query"]:
		if "normalized" in normalInfo["query"]:
			#for every article that wikipedia has normalized, update the normalized dictionary
			for num in normalInfo["query"]["normalized"]:
				normalized[num["from"]] = num["to"]
		if "redirects" in normalInfo["query"]:
			for redir in normalInfo["query"]["redirects"]:
				fromVal = ""
				for art in normalized:
					if normalized[art] == redir["from"]:
						fromVal = art
						break
				normalized[fromVal] = redir["to"]

		fromList = ""
		for art in normalized:
			fromList += normalized[art] + "|"
		fromList = fromList.strip("|")
		#Make the main API call, with all articles replaced with their normalized and redirected version
		pathInfo = checkArticleLink(fromList)
		#will contain INVALID, MISSING, or VALID for every article
		pathReport = {}
		#Check the API response was valid
		if "query" in pathInfo and "pages" in pathInfo["query"]:
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

def getNormalized(articles):
	url = "https://en.wikipedia.org/w/api.php"
	url += "?action=query"
	url += "&format=json"
	url += "&titles="+articles
	url += "&redirects"
	query = requests.get(url)
	return json.loads(query.text)

def checkArticleLink(from_articles):
	url = "https://en.wikipedia.org/w/api.php"
	url += "?action=query"
	url += "&format=json"
	url += "&titles="+from_articles
	url += "&prop=links"
	#will only return links to articles listed in the pltitles prop
	url += "&pltitles="+from_articles
	url += "&pllimit=max"
	url += "&redirects"
	query = requests.get(url)
	return json.loads(query.text)
