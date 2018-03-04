#!/usr/bin/env python

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_login_page(self):
        self.browser.get('http://127.0.0.1:5000')
        t = self.browser.find_element_by_tag_name('p').text
        self.assertIn('Name:', t)

if __name__ == '__main__':
    unittest.main()
