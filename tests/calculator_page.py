import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    def load_url(self, url):
        self.driver.get(url)

    def fill_form(self, num1, num2, operation):
        self.clear_fields()
        self.driver.find_element(By.ID, "num1").send_keys(str(num1))
        self.driver.find_element(By.ID, "num2").send_keys(str(num2))
        select = Select(self.driver.find_element(By.ID, "operation"))
        select.select_by_value(operation)
        self.driver.find_element(By.ID, "calculate").click()

    def clear_fields(self):
        self.driver.find_element(By.ID, "num1").clear()
        self.driver.find_element(By.ID, "num2").clear()

    def get_result(self):
        result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        return result.text
