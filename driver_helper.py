from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class DriverHelper:
    def __init__(self, driver, timeout):
        self.driver = driver
        self.timeout = timeout    

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