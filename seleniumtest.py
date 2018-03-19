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

    def test_search(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@name="firstname"]'). send_keys('Ingo')
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
        t = self.browser.find_element_by_id('name').text
        self.assertEqual(t, 'Name: Knito, Ingo')

    def test_search_fail_no_field_filled(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
        t = self.browser.find_element_by_xpath('//ul[@class="flashes"]/li').text
        self.assertEqual(t,
            'At least one of Firstname, Lastname must be used for search')

    def test_search_fail_name_does_not_exist(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@name="firstname"]').send_keys('Hannibal')
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
        t = self.browser.find_element_by_xpath('//ul[@class="flashes"]/li').text
        self.assertEqual(t, 'No name found')

    def test_all_names(self):
        '''
        We don't care about details. If we have as many list elements with the
        right class as there are names in the data, we assume the page works.
        '''
        self.browser.get('http://127.0.0.1:5000/all')
        namez = names.Name.names_from_csv(open(names.CSV_FILE))
        self.assertEqual(len(self.browser.find_elements_by_xpath('//li[@class="nameentry"]')),
                len(namez))

if __name__ == '__main__':
    unittest.main()
