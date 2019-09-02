import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Melina has heard that there is a new todo-list ap and wants to check it out.
		# so she goes to the website
		self.browser.get(self.live_server_url)

		# she notices the page title and the header mentions the to-do list
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a todo item straight away
		inputbox = self.browser.find_element_by_id('id-new-item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'), 'Enter a to-do item'
			)

		# She types "Buy a new laptop"  into the box text
		inputbox.send_keys("Buy a new laptop")

		# when she hits enter the page refresh, updates and now the pag elist: "1 - Buy a new laptop"
		inputbox.send_keys(Keys.ENTER)

		time.sleep(3)

		melina_list_url = self.browser.current_url
		self.assertRegex(melina_list_url,'/lists/.+')

		time.sleep(3)

		self.check_for_row_in_list_table('1: Buy a new laptop')

		# There is anothe rtextbox inviting her to insert another item. she enters "Use the laptop to make design"
		inputbox = self.browser.find_element_by_id('id-new-item')
		inputbox.send_keys("Use the laptop to design a brand")
		inputbox.send_keys(Keys.ENTER)

		time.sleep(3)

		self.check_for_row_in_list_table('1: Buy a new laptop')
		self.check_for_row_in_list_table('2: Use the laptop to design a brand')

		#Now a new user, Francis, come along to the site

		# We use a new browser session to make sure that no information of Edith's coming through the cookies
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

		# Francis visits the home page. There is no sign of Edith's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy a new laptop', page_text)
		self.assertNotIn('Use the laptop to design a brand', page_text)

		#Francis starts a new list by entering  a new item. He is less interesting than Edith
		inputbox = self.browser.find_element_by_id('id-new-item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		time.sleep(3)

		# Francis get his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, melina_list_url)

		# Again there is no trace of Melina's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy a new laptop', page_text)
		self.assertIn('Buy milk', page_text)

		#Satisfied, they both go to sleep

		#self.fail('Finish the test!')

		# the page updates again and now shows both the items of the list

		# Melina aks ehreself if the site will remebember her list; then she seees that there is generated unique URL for her

		# she visits that URL, and her to do list is there

		# She goes back to sleep


	def test_layout_and_styling(self):
		#Melina goes to the homepage
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024,768)

		#Melina must note that the input box is centered
		inputbox = self.browser.find_element_by_id('id-new-item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)