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
        self.__go_to_customers_page()
        
        customer_row = self.__check_if_customer_exists(order)
        if customer_row is None:
            self.__create_customer(order)
            time.sleep(5)
            self.__go_to_customers_page()
            customer_row = self.__check_if_customer_exists(order)
        self.__create_invoice(customer_row, order)
        self.driver.quit()

    def __go_to_customers_page(self):
        self.helper.wait_for_load_by_xpath('/html/body/div[6]/div[1]/div[2]/div/ul/li[2]/a').click()

    def __check_if_customer_exists(self, order):
        nif = self.__get_nif(order)
        search_key = nif if nif != '' else self.__get_full_name(order)
        print('searching for ' + search_key)
        self.helper.wait_for_load('keyword').send_keys(search_key)
        self.driver.find_element_by_id('keyword').send_keys(Keys.ENTER)
        time.sleep(2)

        rows = self.driver.find_elements_by_css_selector('table.object_list:nth-child(3) > tbody > .row')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if cols[0].text == str(order['customer_id']):
                print('found customer ' + self.__get_full_name(order))
                return row
        return None

    def __create_customer(self, order):
        self.helper.wait_for_load_by_name('Add').click()
        self.helper.wait_for_load('name').send_keys(self.__get_full_name(order))
        self.driver.find_element_by_id('code').send_keys(order['customer_id'])
        self.driver.find_element_by_id('nif').send_keys(self.__get_nif(order))
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
        self.__confirm_modal('Tem a certeza que quer criar o cliente?', '/html/body/div[8]/div[3]/div/button[1]')

    def __create_invoice(self, customer_row, order):
        customer_row.find_element_by_tag_name('a').click()
        self.helper.wait_for_load_by_xpath('/html/body/div[6]/div[2]/div/div/form/div[1]/div[2]/a[2]/img').click()
        Select(self.helper.wait_for_load('document_type')).select_by_visible_text('Factura Simplificada')
        self.__set_date_value(self.driver.find_element_by_name('date'), order['date_created'])
        self.__set_date_value(self.driver.find_element_by_name('payment_date'), order['date_created'])
        self.driver.find_element_by_name('Send').click()
        self.__confirm_modal('Tem a certeza que quer criar o documento?', '/html/body/div[8]/div[3]/div/button[1]')
        for item in order['line_items']:
            self.__add_products(item)
        self.__add_shipping(order['shipping_lines'][0])

    def __add_products(self, item):
        self.helper.wait_for_load('item_type_product').click()
        self.driver.find_element_by_id('item').send_keys(self.__create_item_name(item))
        self.helper.replace_input_value_by_id(element_id='quantity', number_of_chars_to_remove=1, value=item['quantity'])
        price = str(item['price']).replace('.', ',')
        self.helper.replace_input_value_by_id(element_id='price', number_of_chars_to_remove=4, value=price)
        self.driver.find_element_by_id('item_update').click()
        Select(self.helper.wait_for_load('taxfreereason')).select_by_visible_text('M10-IVA - Regime de isenção')
        self.__confirm_modal('Está a introduzir um artigo sem IVA', '/html/body/div[7]/div[3]/div/button[1]') # Probably no longer needed
        time.sleep(4)

    def __add_shipping(self, item):
        # Let's pretend the shipping line is just another item
        shipping_item = {
            'name': item['method_title'],
            'quantity': 1,
            'price': item['total']
        }
        self.__add_products(shipping_item)

    ############# AUX Methods #############

    def __get_nif(self, order):
        for meta_data in order['meta_data']:
            if meta_data['key'] == 'billing_nif':
                return meta_data['value']
        return ''
    
    def __get_full_name(self, order):
        return order['billing']['first_name'] + ' ' + order['billing']['last_name']

    def __confirm_modal(self, expected_modal_text, button_xpath):
        modal = self.driver.find_element_by_id('modal')
        if expected_modal_text in modal.text:
            self.helper.wait_for_load_by_xpath(button_xpath).send_keys(Keys.ENTER)

    def __set_date_value(self, element, date_time):
        date = date_time[0:11]
        element.clear()
        element.send_keys(date)

    def __create_item_name(self, item):
        if 'sku' not in item:
            return item['name']
        return '{name} (#{sku})'.format(name = item['name'], sku = item['sku'])
