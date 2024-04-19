class User:
    def __init__(self, id, name, points):
        self.id = id
        self.name = name
        self.points = points

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

class Submission:
    def __init__(self, id, userid, postid, path, datetime_submit, articleno):
        self.id = id
        self.userid = userid
        self.postid = postid
        self.path = path
        self.datetime_submit = satetime_submit
        self.articleno = articleno