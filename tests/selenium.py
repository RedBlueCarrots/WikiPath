
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
		self.driver.implicitly_wait(10)
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

	def test_create_and_login(self):
		self.driver.implicitly_wait(10)
		self.create_account()
		username_display = self.driver.find_element(by=By.ID, value="usernameDisplay")
		self.assertEquals(username_display.text, "TestingUsername")
		self.logout()
		username_exists = self.driver.find_elements(by=By.ID, value="usernameDisplay")
		self.assertFalse(username_exists)
		self.login()
		username_display = self.driver.find_element(by=By.ID, value="usernameDisplay")
		self.assertEquals(username_display.text, "TestingUsername")