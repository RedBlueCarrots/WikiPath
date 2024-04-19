from classes import *
import sqlite3

db_path = './back-end/wikipath.db'


# receives a user object and attempts to insert it into database
# if something goes wrong, returns False, otherwise returns True
def insertUser(user):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    try: 
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user.id, user.name, user.points))
    except:
        return False
    con.commit()
    con.close()
    return True

def insertChallenge(post):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("INSERT INTO challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (post.id, post.userid, post.title, post.path, post.datetime_submit, post.datetime_finish, post.finished, post.winpostid))
    con.commit()
    con.close()
    return True

def insertSubmission(sub):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?)", (sub.id, sub.userid, sub.postid, sub.path, sub.datetime_submit, sub.articleno))
    con.commit()
    con.close()
    return True

def getUser(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    details = cur.fetchone()
    user = User(details[0], details[1], details[2])
    con.close()
    return user

def getChallenge(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM challenges WHERE id = ?", (id,))
    details = cur.fetchone()
    post = Challenge(details[0], details[1],details[2],details[3],details[4],details[5],details[6],details[7])
    con.close()
    return post

# I don't know if we will need this
def getSubmission(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM submissions WHERE id = ?", (id,))
    details = cur.fetchone()
    submission = Submission(details[0], details[1],details[2],details[3],details[4],details[5])
    con.close()
    return submission

def updateUser(user):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user.id))
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user.id, user.name, user.points))
    con.commit()
    con.close()
    return True

# when we want to update the challenge post
def updateChallenge(post):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("DELETE FROM challenges WHERE id = ?", (post.id))
    cur.execute("INSERT INTO challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (post.id, post.userid, post.title, post.path, post.datetime_submit, post.datetime_finish, post.finished, post.winpostid))
    con.commit()
    con.close()
    return True

def addPoints(user, points):
    user.points = user.points + points
    updateUser(user)

def testUser():
    user = getUser(0)
    print(user.name)
    challenge = getChallenge(1)
    print(challenge.title)
    submission = getSubmission(1)
    print(submission.path)