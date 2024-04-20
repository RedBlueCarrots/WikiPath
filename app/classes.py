# creates a user object
class User:
    def __init__(self, id, name, points):
        self.id = id
        self.name = name
        self.points = points

# creates a challenge object, datetime_submit and datetime_finish are in Unix timestamps
class Challenge:
    def __init__(self, id, userid, title, path, datetime_submit, datetime_finish, finished, winpostid):
        self.id = id
        self.userid = userid
        self.title = title
        self.path = path
        self.datetime_submit = datetime_submit
        self.datetime_finish = datetime_finish
        self.finished = finished
        self.winpostid = winpostid

# creates a submission object, datetime_submit is in Unix timestamp
class Submission:
    def __init__(self, id, userid, postid, path, datetime_submit, articleno):
        self.id = id
        self.userid = userid
        self.postid = postid
        self.path = path
        self.datetime_submit = datetime_submit
        self.articleno = articleno