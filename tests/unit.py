from app import create_app, db
from app.config import TestConfig
from app.models import *
from app.database import *
from unittest import TestCase

class UnitTests(TestCase):

	def setUp(self):
		app = create_app(TestConfig)
		self.app_context = app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_return_user_via_username(self):
		user1 = User(username = "Test", password_hash = "", WikiAura = 0, password_salt = random.choice(string.ascii_letters))
		db.session.add(user1)
		user2 = returnUserViaUsername("Test")
		self.assertEqual(user1, user2)
		user3 = returnUserViaUsername("NotExist")
		self.assertIsNone(user3)

	def test_create_user(self):
		createUser("TestCreate", "Password1")
		user = returnUserViaUsername("TestCreate")
		self.assertIsNotNone(user)

	def test_check_password(self):
		createUser("TestPassword", "Password2")
		user = returnUserViaUsername("TestPassword")
		self.assertTrue(user.check_password("Password2"))
		self.assertFalse(user.check_password("Password3"))

	def test_get_challenge(self):
		challenge1 = Challenge(creator_id = 1, title="testChallenge", path="testPath",
        dt_submit=500, dt_finish=700, finished=False)
		db.session.add(challenge1)
		challengeCheck = Challenge.query.filter_by(title="testChallenge").first()
		challengeId = challengeCheck.id
		challenge2 = getChallenge(challengeId)
		self.assertEqual(challenge1, challenge2)
		challenge3 = getChallenge(challengeId - 1)
		self.assertIsNone(challenge3)

	def test_create_challenge(self):
		createNewChallenge(1,"title","path",500,600)
		challenge = getChallenge(1)
		self.assertIsNotNone(challenge)

	def test_check_submission_exists(self):
		submission =  Submission(creator_id=1, challenge_id=1,
        path="testPath", dt_submit=500, article_no=3,win=False)
		db.session.add(submission)
		submissionCheck = Submission.query.filter_by(path="testPath").first()
		submissionId = submissionCheck.id
		self.assertTrue(checkSubmissionExists(submissionId))
		self.assertFalse(checkSubmissionExists(submissionId -1 ))
		
	def test_get_submissions_by_challenge_and_creator(self):
		submission1 =  Submission(creator_id=2, challenge_id=1,
        path="testPath", dt_submit=500, article_no=3,win=False)
		db.session.add(submission1)
		submission2 = getSubmissionByChallengeAndCreator(1,2)
		self.assertEqual(submission1, submission2)
		submission3 = getSubmissionByChallengeAndCreator(1,3)
		submission4 = getSubmissionByChallengeAndCreator(2,2)
		self.assertIsNone(submission3)
		self.assertIsNone(submission4)

	def test_create_new_submission(self):
		createNewSubmission(1,2,"path",600)
		submission = getSubmissionByChallengeAndCreator(2,1)
		self.assertIsNotNone(submission)

	def test_get_submission_by_challenge(self):
		createNewSubmission(1,1,"path",600)
		createNewSubmission(2,1,"path",600)
		createNewSubmission(3,2,"path",600)
		expectedChallenge1 = [getSubmissionByChallengeAndCreator(1,1), getSubmissionByChallengeAndCreator(1,2)]
		submissionsChallenge1 = getSubmissionsByChallenge(1)
		self.assertEqual(expectedChallenge1, submissionsChallenge1)

	def test_find_winner(self):
		createNewChallenge(1,"test","TestTest",500,600)
		challenge = Challenge.query.filter_by(title="test").first()
		challengeId = challenge.id
		createNewSubmission(1,challengeId, "Short|Path",550)
		createNewSubmission(2,challengeId, "A|Long|Path",550)
		winningSubmission = getSubmissionByChallengeAndCreator(challengeId,1)
		self.assertEqual(winningSubmission.id, findWinner(challenge))

	def test_check_challenges_completed(self):
		#challenge finished - challenge winner - wikiaura increase
		createUser("test1","pass1")
		createUser("test2","pass2")
		user1 = returnUserViaUsername("test1")
		user2 = returnUserViaUsername("test2")
		createNewChallenge(user1.id + user2.id,"ChallengeNotFinish","To|Here",time.time() - 5, time.time() + 10)
		createNewChallenge(user1.id + user2.id,"ChallengeFinish","To|There",time.time() - 5, time.time() - 1)
		challengeNotFinish = Challenge.query.filter_by(title="ChallengeNotFinish").first()
		challengeFinish = Challenge.query.filter_by(title="ChallengeFinish").first()
		createNewSubmission(user1.id, challengeNotFinish.id, "Short|Path",time.time() - 3)
		createNewSubmission(user2.id, challengeNotFinish.id, "A|Longer|Path",time.time() - 3)
		createNewSubmission(user1.id, challengeFinish.id, "Short|Path",time.time() - 3)
		createNewSubmission(user2.id, challengeFinish.id, "A|Longer|Path",time.time() - 3)
		checkChallengesCompleted()
		self.assertTrue(challengeFinish.finished)
		self.assertFalse(challengeNotFinish.finished)
		self.assertEqual(challengeFinish.winner_id, user1.id)
		self.assertEqual(user1.WikiAura, 10)
