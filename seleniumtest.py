#!/usr/bin/env python

from selenium import webdriver
import unittest

import names

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)
        self.names = names.Name.from_csv(open(names.CSV_FILE))

    def tearDown(self):
        self.browser.quit()

    def test_name(self):
        '''
        Check that name is displayed.
        '''
        self.browser.get('http://127.0.0.1:5000')
        t = self.browser.find_element_by_id('name').text

        found = False
        for name in self.names:
            if name.get_puzzle_name().decode('utf-8') in t:
                found = True
        self.assertTrue(found)

    def test_funny_name(self):
        '''
        Check that name is displayed.
        '''
        self.browser.get('http://127.0.0.1:5000')
        t = self.browser.find_element_by_xpath('//input[@value="Zeigs mir"]').click()
        t = self.browser.find_element_by_id('show').text

        found = False
        for name in self.names:
            if name.get_funny_name().decode('utf-8') in t:
                found = True
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
