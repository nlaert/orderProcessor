from driver_helper import DriverHelper
from selenium.webdriver.support.select import Select
from config import read_config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re


class FillDropshippingDataService:
    def __init__(self):
        self.config = read_config.ReadConfig().read_configs()
        options = Options()
        options.headless = self.config['headless']
        self.driver = webdriver.Firefox(firefox_binary=self.config['firefox_binary'], executable_path=self.config['geckodriver'], options=options)
        self.helper = DriverHelper(self.driver, self.config['timeout'])
        print('Creating firefox instance')

    def fill_dropshipping(self, order):
        print('Entering dropshipping')
        self.driver.get(self.config['dropshipping_url'])
        self.driver.find_element_by_css_selector('#login_header_button > span').click()
        self.helper.wait_for_load('handle').send_keys(self.config['dropshipping_login'])
        self.driver.find_element_by_id('pwd').send_keys(self.config['dropshipping_pass'])
        self.driver.find_element_by_id('login_button').click()
        self.helper.wait_for_load('customers_button').click()
        # Wait for element does not work here because this is a div and not a button / link
        time.sleep(5)
        customer_row = self.__check_if_customer_exists(order['customer_id'])
        if customer_row is None:
            self.__create_customer(order)
            time.sleep(5)
            customer_row = self.__check_if_customer_exists(order['customer_id'])
        self.__create_order(order, customer_row)
        self.driver.quit()

    def __create_customer(self, order):
        self.driver.find_element_by_id('new_customer').click()
        self.helper.wait_for_load_by_name('client_reference').send_keys(order['customer_id'])
        self.driver.find_element_by_name('name').send_keys(order['shipping']['first_name'] + ' '
                                                           + order['shipping']['last_name'])
        self.driver.find_element_by_name('organization').send_keys(order['shipping']['company'])
        self.driver.find_element_by_name('email').send_keys(order['billing']['email'])
        self.driver.find_element_by_name('tel').send_keys(order['billing']['phone'])
        self.driver.find_element_by_name('addressLine1').send_keys(order['shipping']['address_1'])
        self.driver.find_element_by_name('addressLine2').send_keys(order['shipping']['address_2'])
        self.driver.find_element_by_name('postalCode').send_keys(order['shipping']['postcode'])
        self.driver.find_element_by_name('locality').send_keys(order['shipping']['city'])
        self.driver.find_element_by_name('administrativeArea').send_keys(order['shipping']['city'])
        dropdown = Select(self.driver.find_element_by_id('country_select'))
        dropdown.select_by_value(order['shipping']['country'])

        self.driver.find_element_by_id('save_new_client_button').click()
        self.helper.wait_for_load_by_css('button.ui-button:nth-child(1)').click()

    def __check_if_customer_exists(self, customer_id):
        rows = self.driver.find_elements_by_css_selector('#table > table > tbody > tr')
        for row in rows:
            firstSpaceIndex = row.text.index(' ')
            ref = int(row.text[0:firstSpaceIndex])
            id = row.find_element_by_id('portfolio_ref_' + str(ref)).find_element_by_tag_name('span').text
            if int(id) == customer_id:
                return row
        return None

    def __create_order(self, order, customer_row):
        customer_row.find_element_by_class_name('fa-shopping-cart').click()
        for item in order['line_items']:
            self.__add_products(item)

    def __add_products(self, item):
        sku = self.__get_complete_sku(item['sku'])
        self.helper.wait_for_load_by_xpath('//*[@id="block_0"]/div[2]/span/table/thead/tr[1]/td/div/input[1]').send_keys(sku)
        self.driver.find_element_by_xpath('//*[@id="block_0"]/div[2]/span/table/thead/tr[1]/td/div/input[2]').send_keys(item['quantity'])
        time.sleep(2)
        self.helper.wait_for_load_by_css('.add_item_results').click()
        self.driver.find_element_by_class_name('fa-cloud').click()

    def __get_complete_sku(self, sku):
        index = re.search(r'\d', sku).start()
        return sku[0: index] + '-' + sku[index: len(sku)]
