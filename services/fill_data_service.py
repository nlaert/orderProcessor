from selenium.webdriver.support.select import Select
from config import read_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time


class FillDataService:
    def __init__(self):
        self.config = read_config.ReadConfig().read_configs()
        options = Options()
        options.headless = self.config['headless']
        self.driver = webdriver.Firefox()
        print('Creating firefox instance')

    def fill_dropshipping(self, order):
        print('Entering dropshipping')
        self.driver.get(self.config['dropshipping_url'])
        self.driver.find_element_by_css_selector('#login_header_button > span').click()
        self.__wait_for_load('handle').send_keys(self.config['dropshipping_login'])
        self.driver.find_element_by_id('pwd').send_keys(self.config['dropshipping_pass'])
        self.driver.find_element_by_id('login_button').click()
        self.__wait_for_load('customers_button').click()
        # Wait for element does not work here because this is a div and not a button / link
        time.sleep(5)
        if self.__check_if_customer_exists(order['customer_id']):
            self.__create_customer(order)

    def __create_customer(self, order):
        self.driver.find_element_by_id('new_customer').click()
        self.__wait_for_load_by_name('client_reference').send_keys(order['customer_id'])
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
        self.__wait_for_load_by_css('button.ui-button:nth-child(1)').click()

    def __check_if_customer_exists(self, customer_id):
        rows = self.driver.find_elements_by_css_selector('#table > table > tbody > tr')
        for row in rows:
            firstSpaceIndex = row.text.index(' ')
            ref = int(row.text[0:firstSpaceIndex])
            id = row.find_element_by_id('portfolio_ref_' + str(ref)).find_element_by_tag_name('span').text
            if int(id) == customer_id:
                return True
        return False

    def __wait_for_load(self, element_id):
        return WebDriverWait(self.driver, self.config['timeout'])\
            .until(EC.presence_of_element_located((By.ID, element_id)))

    def __wait_for_load_by_name(self, element_name):
        return WebDriverWait(self.driver, self.config['timeout']) \
            .until(EC.presence_of_element_located((By.NAME, element_name)))

    def __wait_for_load_by_xpath(self, xpath):
        return WebDriverWait(self.driver, self.config['timeout']) \
            .until(EC.presence_of_element_located((By.XPATH, xpath)))

    def __wait_for_load_by_css(self, selector):
        return WebDriverWait(self.driver, self.config['timeout']) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))