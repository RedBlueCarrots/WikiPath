
#From what I could find, the method shown in the slides does not work on windows (gives Can't pickle local object)
#https://github.com/pytest-dev/pytest-flask/issues/54 - seems to be a thing, may just not work on windows.


import multiprocessing
import time
from app import create_app, db
from app.config import TestConfig
from selenium import webdriver
from unittest import TestCase

localHost = "http://localhost:5000/"


class SeleniumTests(TestCase):

	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

		self.server_thread = multiprocessing.Process(target=self.app.run)
		self.server_thread.start()

		self.driver = webdriver.Chrome()
		self.driver.get(localHost)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

		self.server_thread.terminate()
		self.driver.close()

	def test_testing_works(self):
		time.sleep(10)
		self.assertTrue(True)