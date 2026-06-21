import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from test_booking_flow_page import BookingFlowPage


@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if os.environ.get("HEADLESS") or os.environ.get("CI"):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()


@pytest.fixture
def booking_page(driver):
    page = BookingFlowPage(driver, "http://localhost:5000")
    page.navigate()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "eventType"))
    )
    time.sleep(1)

    yield page
