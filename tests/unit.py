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

