#!/usr/bin/env python

from selenium import webdriver
import unittest

import names

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_login_page(self):
        self.browser.get('http://127.0.0.1:5000')
        t = self.browser.find_element_by_id('name').text

        allnames = names.Name.from_csv(open(names.CSV_FILE))
        found = False
        for name in allnames:
            if name.get_puzzle_name().decode('utf-8') in t:
                found = True
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
