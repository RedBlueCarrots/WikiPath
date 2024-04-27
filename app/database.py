from .classes import *
from .models import *
from .utilities import *
import sqlite3
import time
from app import login

db_path = './app/back-end/wikipath.db'

@login.user_loader
def load_user(id):
    return getUser(id)

# receives a user object and inserts it into database
def insertUser(user):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user.id, user.name, user.points))
    con.commit()
    con.close()
    
# receives a challenge object and inserts it into database
def insertChallenge(post):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("INSERT INTO challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (post.id, post.userid, post.title, post.path, post.datetime_submit, post.datetime_finish, post.finished, post.winpostid))
    con.commit()
    con.close()
    
# receives a submission object and inserts it into database
def insertSubmission(sub):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?)", (sub.id, sub.userid, sub.postid, sub.path, sub.datetime_submit, sub.articleno))
    con.commit()
    con.close()
    
# receives a user id and retrieves and returns a user object
def getUser(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    details = cur.fetchone()
    user = User(details[0], details[1], details[2])
    con.close()
    return user

# receives a username and retrieves and returns a user object
def getUserViaName(name):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    details = cur.fetchone()
    user = User(details[0], details[1], details[2])
    con.close()
    return user

# recieves challenge id and retrieves and returns a challenge object
def getChallenge(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM challenges WHERE id = ?", (id,))
    details = cur.fetchone()
    post = Challenge(details[0], details[1],details[2],details[3],details[4],details[5],details[6],details[7])
    con.close()
    return post

def getAllChallenges():
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("""SELECT challenges.*,COUNT(submissions.id), users.name
                 FROM challenges LEFT JOIN submissions ON challenges.id=submissions.postid
                 JOIN users ON challenges.userid = users.id 
                 GROUP BY challenges.id""")
    allChallenges = []
    details = cur.fetchone()
    while details:
        timeLeft = secondsToTime(details[5]-int(time.time()))
        allChallenges.append(Challenge(*details, timeLeft))
        details = cur.fetchone()
    con.close()
    return allChallenges

# recieves submission id and retrieves and returns a submission object
def getSubmission(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM submissions WHERE id = ?", (id,))
    details = cur.fetchone()
    submission = Submission(details[0], details[1],details[2],details[3],details[4],details[5])
    con.close()
    return submission

# recieves challenge id and retrieves and returns an array of all related submission
def getSubmissions(id):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    submissions = []
    # sqlite by default will order results from earliest submission to latest
    for details in cur.execute("SELECT * FROM submissions WHERE id = ?", (id,)):
        submissions.append(Submission(details[0], details[1],details[2],details[3],details[4],details[5]))
    con.close()
    return submissions

# updates the values of a user
def updateUser(user):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user.id))
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user.id, user.name, user.points))
    con.commit()
    con.close()

# updates the values of a challenge
def updateChallenge(post):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("DELETE FROM challenges WHERE id = ?", (post.id))
    cur.execute("INSERT INTO challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (post.id, post.userid, post.title, post.path, post.datetime_submit, post.datetime_finish, post.finished, post.winpostid))
    con.commit()
    con.close()

# determines if a username is already taken
def checkUsernameExists(name):
    con = sqlite3.connect(db_path, uri=True)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    details = cur.fetchall()
    con.close()
    if len(details) == 0:
        # username doesn't exist
        return False
    else:
        return True
    
 # add points to a user, updates the database and returns the user
def addPoints(user, points):
    user.points = user.points + points
    updateUser(user)
    return user
