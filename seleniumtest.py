#!/usr/bin/env python

from selenium.common.exceptions import NoSuchElementException
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
            if name.get_puzzle_name() in t:
                found = True
        self.assertTrue(found)

    def test_funny_name(self):
        '''
        Check that name is displayed.
        '''
        self.browser.get('http://127.0.0.1:5000')
        self.browser.find_element_by_xpath('//input[@value="Zeigs mir"]').click()
        t = self.browser.find_element_by_id('show').text

        found = False
        for name in self.names:
            if name.get_funny_name() in t:
                found = True
        self.assertTrue(found)

    def test_resolution(self):
        '''
        Check that name is displayed.
        '''
        self.browser.get('http://127.0.0.1:5000')
        self.browser.find_element_by_xpath('//input[@value="Zeigs mir"]').click()

        # Not all funny names need to be explained, so if the button is not
        # there, we don't test.
        # The value (displayed text) of this button contains an umlaut, so we
        # better search it by id, umlauts in an XPath, as we use it for the
        # first button, won't work.
        be = None
        try:
            be = self.browser.find_element_by_id('explainbutton')
        except NoSuchElementException:
            return
        if be:
            be.click()
            t = self.browser.find_element_by_id('explain').text

        found = False
        for name in self.names:
            if name.resolution in t:
                found = True
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
