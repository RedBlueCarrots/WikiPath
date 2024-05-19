
#From what I could find, the method shown in the slides does not work on windows (gives Can't pickle local object)
#https://github.com/pytest-dev/pytest-flask/issues/54 - seems to be a thing, may just not work on windows.
#If running windows, you will have to flask --run on a seperate terminal, and remove the server_thread lines
#Note that doing that will edit the default app.db, which is far from ideal.

import multiprocessing
import time
from app import create_app, db
from app.config import TestConfig
from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

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


		# self.driver = webdriver.Chrome()
		# self.driver.implicitly_wait(10)

		
		options = Options()
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		geckodriver_path = "/snap/bin/geckodriver"
		driver_service = Service(executable_path=geckodriver_path)
		self.driver = webdriver.Firefox(options=options, service=driver_service)

		self.driver.get(localHost)
		

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

		self.server_thread.terminate()
		self.driver.close()

	def keyIndividualLetters(self, input, sendTo):
		for i in input:
			sendTo.send_keys(i)

	def create_account(self):
		login_button = self.driver.find_element(by=By.ID, value="loginButton")
		login_button.click()
		username_field = self.driver.find_element(by=By.ID, value="username")
		self.keyIndividualLetters("TestingUsername", username_field)
		password_field = self.driver.find_element(by=By.ID, value="password")
		self.keyIndividualLetters("TestPassword", password_field)
		create_account_button = self.driver.find_element(by=By.ID, value="/create_account")
		create_account_button.click()

	def logout(self):
		logout_button = self.driver.find_element(by=By.ID, value="logoutButton")
		logout_button.click()

	def login(self):
		login_button = self.driver.find_element(by=By.ID, value="loginButton")
		login_button.click()
		username_field = self.driver.find_element(by=By.ID, value="username")
		self.keyIndividualLetters("TestingUsername", username_field)
		password_field = self.driver.find_element(by=By.ID, value="password")
		self.keyIndividualLetters("TestPassword", password_field)
		confirm_login_button = self.driver.find_element(by=By.ID, value="/login")
		confirm_login_button.click()

	def create_challenge(self):
		create_challenge_button = self.driver.find_element(by=By.ID, value="createChallengeButton")
		create_challenge_button.click()
		challenge_title = self.driver.find_element(by=By.ID, value="title")
		self.keyIndividualLetters("Test Title", challenge_title)
		start_article = self.driver.find_element(by=By.ID, value="start")
		self.keyIndividualLetters("Left", start_article)
		end_article = self.driver.find_element(by=By.ID, value="destination")
		self.keyIndividualLetters("Right", end_article)
		time=self.driver.find_element(by=By.ID, value="time")
		self.keyIndividualLetters("99999999p", time)
		submit = self.driver.find_element(by=By.ID, value="submit")
		submit.click()

	def view_challenge(self):
		view_challenge_button = self.driver.find_element(by=By.ID, value="title")
		view_challenge_button.click()


	def create_and_login(self):
		# self.driver.implicitly_wait(10)
		self.create_account()
		username_display = self.driver.find_element(by=By.ID, value="usernameDisplay")
		self.assertEqual(username_display.text, "TestingUsername")
		self.logout()
		username_exists = self.driver.find_elements(by=By.ID, value="usernameDisplay")
		self.assertFalse(username_exists)
		self.login()
		username_display = self.driver.find_element(by=By.ID, value="usernameDisplay")
		self.assertEqual(username_display.text, "TestingUsername")		

	def create_and_view_challenge(self):
		self.create_challenge()
		title = self.driver.find_element(by=By.ID, value="title")
		self.assertEqual(title.text, "Test Title")
		start = self.driver.find_element(by=By.ID, value="start")
		self.assertEqual(start.text, "Left")
		end = self.driver.find_element(by=By.ID, value="end")
		self.assertEqual(end.text, "Right")
		guesses = self.driver.find_element(by=By.ID, value="guesses")
		self.assertEqual(guesses.text, "0")
		creator = self.driver.find_element(by=By.ID, value="creator")
		self.assertEqual(creator.text, "TestingUsername")
		# really difficult to check the time remaining as it's constantly changing
		time = self.driver.find_element(by=By.ID, value="time")
		self.assertNotEqual(time.text, "Finished")
		# self.view_challenge()


	def test_overall_functionality(self):
		self.create_and_login()
		self.create_and_view_challenge()

		
	