import pytest
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.calculator_page import CalculatorPage

BASE_URL = "http://localhost:8000/index.html"

class TestCalculator:
    @pytest.fixture(scope="class")
    def driver(self, request):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        import os, sys

        chrome_options = Options()
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

        path = ChromeDriverManager().install()
        if sys.platform.startswith("win") and not path.endswith("chromedriver.exe"):
            path = os.path.join(os.path.dirname(path), "chromedriver.exe")

        service = Service(path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        request.addfinalizer(driver.quit)
        return driver

    @pytest.fixture
    def page(self, driver):
        p = CalculatorPage(driver)
        p.load_url(BASE_URL)
        return p

    def test_addition(self, page):
        page.fill_form(10, 5, "add")
        assert "Résultat: 15" in page.get_result()

    def test_division_by_zero(self, page):
        page.fill_form(10, 0, "divide")
        assert "Erreur: Division par zéro" in page.get_result()

    def test_all_operations(self, page):
        tests = [
            ("add", 8, 2, "Résultat: 10"),
            ("subtract", 8, 2, "Résultat: 6"),
            ("multiply", 8, 2, "Résultat: 16"),
            ("divide", 8, 2, "Résultat: 4"),
        ]
        for op, a, b, expected in tests:
            page.fill_form(a, b, op)
            assert expected in page.get_result()
            time.sleep(1)

    def test_page_load_time(self, driver):
        start = time.time()
        driver.get(BASE_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "calculator")))
        duration = time.time() - start
        print(f"Load time: {duration:.2f}s")
        assert duration < 3.0

    # Floats
    def test_division_by_float(self, page):
        page.fill_form(1.5, 0.3, "divide")
        assert "Résultat: 5" in page.get_result()

    def test_multiplication_by_float(self, page):
        page.fill_form(1.5, 2, "multiply")
        assert "Résultat: 3" in page.get_result()

    def test_sum_by_float(self, page):
        page.fill_form(1.5, 0.3, "add")
        assert "Résultat: 1.8" in page.get_result()

    def test_sub_by_float(self, page):
        page.fill_form(1.5, 0.3, "subtract")
        assert "Résultat: 1.2" in page.get_result()

    # Négatifs
    def test_division_with_negative(self, page):
        page.fill_form(-6, 2, "divide")
        assert "Résultat: -3" in page.get_result()

    def test_multiplication_with_negative(self, page):
        page.fill_form(-3, 2, "multiply")
        assert "Résultat: -6" in page.get_result()

    def test_sum_with_negative(self, page):
        page.fill_form(-1.5, 0.3, "add")
        assert "Résultat: -1.2" in page.get_result()

    def test_sub_with_negative(self, page):
        page.fill_form(-1.5, 0.5, "subtract")
        assert "Résultat: -2" in page.get_result()
