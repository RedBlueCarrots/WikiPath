import requests
import json

def checkArticleExists(articleName):
	if articleName == "":
		return True
	query = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles="+str(articleName)+"&format=json&formatversion=2")
	queryJson = json.loads(query.text)
	return not "missing" in queryJson["query"]["pages"][0]
