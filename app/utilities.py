def secondsToTime(totalSeconds):
	daysLeft = int(totalSeconds/(60*60*24))
	hoursLeft = int((totalSeconds - daysLeft*(60*60*24))/3600)
	minutesLeft = int((totalSeconds - daysLeft*(60*60*24)-hoursLeft*3600)/60)
	timeString = ""
	if daysLeft > 0:
	    timeString +=  str(daysLeft) + " day"
	    if daysLeft > 1:
	        timeString += "s"
	if hoursLeft > 0:
	    timeString += " "+str(hoursLeft)+" hour"
	    if hoursLeft > 1:
	        timeString += "s"
	if minutesLeft > 0:
	    timeString += " "+str(minutesLeft)+" minute"
	    if minutesLeft > 1:
	        timeString += "s"
	if timeString == "":
	    timeString += "0 minutes"
	return timeString.strip()

def pathify(articleList):
	pathString = ""
	for i in articleList:
		if i.strip() != "":
			pathString += i + "|"
	return pathString.strip("|")
