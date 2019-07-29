from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Melina has heard that there is a new todo-list ap and wants to check it out.
		# so she goes to the website
		self.browser.get('http://localhost:8000')

		# she notices the page title and the header mentions the to-do list
		self.assertIn('To-Do', self.browser.title)
		self.fail("Finish the test")

		# She is invited to enter a todo item straight away

		# She types "Buy a new laptop"  into the box text

		# when she hits enter the page refresh, updates and now the pag elist: "1 - Buy a new laptop"

		# There is anothe rtextbox inviting her to insert another item. she enters "Use the laptop to make design"

		# the page updates again and now shows both the items of the list

		# Melina aks ehreself if the site will remebember her list; then she seees that there is generated unique URL for her

		# she visits that URL, and her to do list is there

		# She goes back to sleep

if __name__ == '__main__':
	unittest.main(warnings='ignore')