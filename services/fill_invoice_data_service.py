import time
from config.read_config import ReadConfig
from selenium.webdriver.support.select import Select
from driver_helper import DriverHelper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class FillInvoiceDataService:
    def __init__(self):
        self.config = ReadConfig().read_configs()
        
    def fill_invoice(self, order):
        self.helper = DriverHelper(self.config)
        self.driver = self.helper.driver

        print('Entering invoice system')
        self.driver.get(self.config['invoice.url'])
        self.driver.find_element_by_id("email").send_keys(self.config['invoice.login'])
        self.driver.find_element_by_id("password").send_keys(self.config['invoice.pass'])
        self.driver.find_element_by_name('submit').click()

        self.helper.wait_for_load('news')
        self.helper.wait_for_load_by_xpath('/html/body/div[6]/div[1]/div[2]/div/ul/li[2]/a').click()
        customer_row = self.__check_if_customer_exists(order)
        if customer_row is None:
            self.create_customer(order)
        time.sleep(10)
        self.driver.quit()

    def __check_if_customer_exists(self, order):
        nif = self.__get_nif__(order)
        search_key = nif if nif is not None else self.__get_full_name(order)
        print('searching for ' + search_key)
        self.helper.wait_for_load('keyword').send_keys(search_key)
        self.driver.find_element_by_id('keyword').send_keys(Keys.ENTER)
        time.sleep(5)

        rows = self.driver.find_elements_by_css_selector('table.object_list:nth-child(3) > tbody > .row')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if cols[0].text == str(order['customer_id']):
                print('found customer ' + self.__get_full_name(order))
                return row
        return None


    def create_customer(self, order):
        self.helper.wait_for_load_by_name('Add').click()
        self.helper.wait_for_load('name').send_keys(self.__get_full_name(order))
        self.driver.find_element_by_id('code').send_keys(order['customer_id'])
        self.driver.find_element_by_id('nif').send_keys(self.__get_nif__(order))
        self.driver.find_element_by_id('entity').send_keys(order['billing']['company'])
        self.driver.find_element_by_name('email').send_keys(order['billing']['email'])
        Select(self.driver.find_element_by_id('status')).select_by_visible_text('Aberto')
        self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/form/div[3]/div[2]/div[1]/ul/li[2]/a').click()

        self.driver.find_element_by_id('address').send_keys(order['billing']['address_1'] + ' ' + order['billing']['address_2'])
        self.driver.find_element_by_id('postcode').send_keys(order['billing']['postcode'])
        self.driver.find_element_by_id('city').send_keys(order['billing']['city'])
        Select(self.driver.find_element_by_id('country')).select_by_value(order['billing']['country'])
        self.driver.find_element_by_id('telephone').send_keys(order['billing']['phone'])

        self.driver.find_element_by_name('Send').click()
        modal = self.driver.find_element_by_id('modal')
        if modal.text == 'Tem a certeza que quer criar o cliente?':
            self.helper.wait_for_load_by_xpath('/html/body/div[8]/div[3]/div/button[1]').send_keys(Keys.ENTER)

    def __get_nif__(self, order):
        for meta_data in order['meta_data']:
            if meta_data['key'] == 'billing_nif':
                return meta_data['value']
        return ''
    
    def __get_full_name(self, order):
        return order['billing']['first_name'] + ' ' + order['billing']['last_name']
