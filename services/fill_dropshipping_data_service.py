from config.read_config import ReadConfig
from playwright.sync_api import sync_playwright
import time
import re


class FillDropshippingDataService:
    def __init__(self):
        super().__init__()
        self.options = ReadConfig().read_configs()
        with sync_playwright() as playwright:
            self.browser = playwright.chromium.launch(headless=self.options["headless"])

    def fill_dropshipping(self, order):
        with sync_playwright() as playwright:
            browser, context, page = self.__setup_playwright(playwright, self.options["headless"])
            try:
                page.goto(self.options["dropship_url"])
                self.__process_order(page, order)
            finally:
                context.close()
                browser.close()

    
    def __setup_playwright(self, playwright, headless):
        """Set up playwright."""
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        
        return browser, context, page

    def __process_order(self, page, order):
        print("Entering dropship")
        page.locator("#login_header_button > span").click()
        time.sleep(5)
        page.locator("#handle").fill(self.options["dropship_login"])
        page.locator("#pwd").fill(self.options["dropship_pass"])
        page.get_by_role("button", name="Log in").click()
        
        customer_row = self.__check_if_customer_exists(page, order['customer_id'])
        if customer_row is None:
            self.__create_customer(page, order)
            print('created new customer')
        else:
            customer_row.query_selector('.fa-shopping-cart').click()
        self.__create_order(page, order)

    def __create_customer(self, page, order):
        page.locator('#order_for_new_customer').click()
        self.__get_by_name(page, 'client_reference').fill(str(order['customer_id']))
        self.__get_by_name(page, 'name').fill(order['shipping']['first_name'] + ' '
                                                           + order['shipping']['last_name'])
        self.__get_by_name(page, 'organization').fill(order['shipping']['company'])
        self.__get_by_name(page, 'email').fill(order['billing']['email'])
        self.__get_by_name(page, 'tel').fill(order['billing']['phone'])
        self.__get_by_name(page, 'addressLine1').fill(order['shipping']['address_1'])
        self.__get_by_name(page, 'addressLine2').fill(order['shipping']['address_2'])
        self.__get_by_name(page, 'postalCode').fill(order['shipping']['postcode'])
        self.__get_by_name(page, 'locality').fill(order['shipping']['city'])
        self.__get_by_name(page, 'administrativeArea').fill(order['shipping']['city'])
        self.__get_by_name(page, 'country').select_option(order['shipping']['country'])

        page.locator('#save_order_for_new_customer_button').click()

    def __check_if_customer_exists(self, page, customer_id):        
        print('looking for customer id ' + str(customer_id))
        # Wait for the table to load
        page.wait_for_selector('.backgrid')
        rows = page.query_selector_all('table tbody tr')
        
        for i, row in enumerate(rows):
            cells = row.query_selector_all('td')
            for cell in cells:
                value = cell.inner_text()
                if value == str(customer_id):
                    print('found customer id')
                    return row
           
        return None

    def __create_order(self, page, order):
        for item in order['line_items']:
            self.__add_products(page, item)

    def __add_products(self, page, item):
        sku = self.__get_complete_sku(item['sku'])
        page.locator('input.item').fill(sku)
        page.locator('.qty').fill(str(item['quantity']))
        page.locator('.ok.result.selected').click()
        page.locator('.fa-cloud').click()
        time.sleep(5)

    def __get_complete_sku(self, sku):
        index = re.search(r'\d', sku).start()
        return sku[0: index] + '-' + sku[index: len(sku)]
    
    def __get_by_name(self, page, name):
        str = "[name=%s]" % name
        return page.locator(str)
