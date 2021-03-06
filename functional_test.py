from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
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
		self.browser.get('http://localhost:8000')

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

		import time
		time.sleep(3)

		self.check_for_row_in_list_table('1: Buy a new laptop')

		# There is anothe rtextbox inviting her to insert another item. she enters "Use the laptop to make design"
		inputbox = self.browser.find_element_by_id('id-new-item')
		inputbox.send_keys("Use the laptop to design a brand")
		inputbox.send_keys(Keys.ENTER)

		import time
		time.sleep(3)

		self.check_for_row_in_list_table('1: Buy a new laptop')
		self.check_for_row_in_list_table('2: Use the laptop to design a brand')


		self.fail('Finish the test!')

		# the page updates again and now shows both the items of the list

		# Melina aks ehreself if the site will remebember her list; then she seees that there is generated unique URL for her

		# she visits that URL, and her to do list is there

		# She goes back to sleep

if __name__ == '__main__':
	unittest.main(warnings='ignore')