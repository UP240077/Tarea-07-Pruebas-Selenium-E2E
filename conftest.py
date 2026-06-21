import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    
    yield driver
    driver.quit()

@pytest.fixture
def booking_page(driver):
    from test_booking_flow_page import BookingFlowPage
    
    # Navegar a la página
    page = BookingFlowPage(driver, "http://localhost:5000")
    page.navigate()
    
    # Esperar a que cargue completamente
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "eventType"))
    )
    
    import time
    time.sleep(1)  # Espera 1 seg después de cargar
    
    yield page