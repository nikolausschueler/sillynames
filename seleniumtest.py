#!/usr/bin/env python3

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import unittest

import names


class NewVisitorTest(unittest.TestCase):

    def set_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=options)

    def set_firefox(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        self.browser = webdriver.Firefox(options=options)

    def set_phantomjs(self):
        self.browser = webdriver.PhantomJS()

    def setUp(self):
        self.set_firefox()
        self.browser.implicitly_wait(3)
        with open(names.CSV_FILE, encoding='utf-8') as csv_file:
            self.names = names.Name.names_from_csv(csv_file)

    def tearDown(self):
        self.browser.quit()

    def test_name(self):
        """
        Check that name is displayed.
        """
        self.browser.get('http://127.0.0.1:5000')
        t = self.browser.find_element_by_id('name').text.strip()
        self.assertIn(t.strip(), ["Name: " + name.get_puzzle_name() for name in self.names])

    def test_funny_name(self):
        """
        Check that fun version of name is displayed.
        """
        self.browser.get('http://127.0.0.1:5000')
        self.browser.find_element_by_xpath('//input[@value="Zeigs mir"]').click()
        t = self.browser.find_element_by_id('show').text.strip()
        self.assertIn(t.strip(), [name.get_funny_name() for name in self.names])

    def test_resolution(self):
        """
        Check that resolution is displayed, if available..
        """
        self.browser.get('http://127.0.0.1:5000')
        self.browser.find_element_by_xpath('//input[@value="Zeigs mir"]') \
            .click()

        # Not all funny names need to be explained, so if the button is not
        # there, we don't test.
        # The value (displayed text) of this button contains an umlaut, so we
        # better search it by id, umlauts in an XPath, as we use it for the
        # first button, won't work.
        try:
            be = self.browser.find_element_by_id('explainbutton')
        except NoSuchElementException:
            return
        be.click()
        t = self.browser.find_element_by_id('explain').text.strip()
        self.assertIn(t.strip(), [name.resolution for name in self.names])

    def test_search_by_firstname(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@name="firstname"]') \
            .send_keys('Ingo')
        self.browser.find_element_by_xpath('//input[@value="Suchen"]').click()
        t = self.browser.find_element_by_id('name').text.strip()
        self.assertEqual(t, 'Name: Knito, Ingo')

    def test_search_by_lastname(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@name="lastname"]') \
            .send_keys('Madecke')
        self.browser.find_element_by_xpath('//input[@value="Suchen"]').click()
        t = self.browser.find_element_by_id('name').text.strip()
        self.assertEqual(t, 'Name: Madecke, Roy')

    def test_search_fail_no_field_filled(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@value="Suchen"]').click()
        t = self.browser.find_element_by_xpath('//ul[@class="flashes"]/li').text.strip()
        self.assertEqual(t, names.ERROR_EMPTY_SEARCH)

    def test_search_fail_name_does_not_exist(self):
        self.browser.get('http://127.0.0.1:5000/search')
        self.browser.find_element_by_xpath('//input[@name="firstname"]') \
            .send_keys('Hannibal')
        self.browser.find_element_by_xpath('//input[@value="Suchen"]').click()
        t = self.browser.find_element_by_xpath('//ul[@class="flashes"]/li').text.strip()
        self.assertEqual(t, names.ERROR_NO_NAME_FOUND)

    def test_all_names(self):
        """
        We don't care about details. If we have as many list elements with the
        right class as there are names in the data, we assume the page works.
        """
        self.browser.get('http://127.0.0.1:5000/all')
        list_items = self.browser.find_elements_by_xpath('//li[@class="nameentry"]')
        self.assertCountEqual([name.get_puzzle_name() for name in self.names],
                              [item.text.strip() for item in list_items])


if __name__ == '__main__':
    unittest.main()
