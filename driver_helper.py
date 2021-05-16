from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from config import read_config


class DriverHelper:
    def __init__(self, config):
        options = Options()
        options.headless = config['headless']
        self.driver = webdriver.Firefox(firefox_binary=config['firefox_binary'], executable_path=config['geckodriver'], options=options)
        self.timeout = config['timeout']

    def wait_for_load(self, element_id):
        return WebDriverWait(self.driver, self.timeout)\
            .until(EC.presence_of_element_located((By.ID, element_id)))

    def wait_for_load_by_name(self, element_name):
        return WebDriverWait(self.driver, self.timeout) \
            .until(EC.presence_of_element_located((By.NAME, element_name)))

    def wait_for_load_by_xpath(self, xpath):
        return WebDriverWait(self.driver, self.timeout) \
            .until(EC.presence_of_element_located((By.XPATH, xpath)))

    def wait_for_load_by_css(self, selector):
        return WebDriverWait(self.driver, self.timeout) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
