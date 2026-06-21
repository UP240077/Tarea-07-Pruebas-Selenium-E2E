from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BookingFlowPage:
    EVENT_TYPE_SELECT = (By.ID, "eventType")
    BOOKING_DATE_INPUT = (By.ID, "bookingDate")
    SLOT_BUTTONS = (By.CLASS_NAME, "slot-button")
    SELECTED_SLOT_INPUT = (By.ID, "selectedSlot")
    ATTENDEE_NAME_INPUT = (By.ID, "attendeeName")
    ATTENDEE_EMAIL_INPUT = (By.ID, "attendeeEmail")
    ATTENDEE_PHONE_INPUT = (By.ID, "attendeePhone")
    ATTENDEE_DESCRIPTION_INPUT = (By.ID, "attendeeDescription")
    SUBMIT_BUTTON = (By.ID, "submitBtn")
    SUCCESS_MESSAGE = (By.ID, "successMessage")
    
    EVENT_TYPE_ERROR = (By.ID, "eventTypeError")
    DATE_ERROR = (By.ID, "dateError")
    SLOT_ERROR = (By.ID, "slotError")
    NAME_ERROR = (By.ID, "nameError")
    EMAIL_ERROR = (By.ID, "emailError")
    
    def __init__(self, driver, base_url="http://localhost:5000"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
    
    def navigate(self):
        self.driver.get(self.base_url)
        time.sleep(1)
    
    def select_event_type(self, event_type_id):
        dropdown = self.wait.until(EC.presence_of_element_located(self.EVENT_TYPE_SELECT))
        dropdown.click()
        time.sleep(0.5)
        option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"option[value='{event_type_id}']")))
        option.click()
        time.sleep(0.5)
    
    def set_booking_date(self, date):
        date_input = self.wait.until(EC.presence_of_element_located(self.BOOKING_DATE_INPUT))
        date_input.clear()
        date_input.send_keys(date)
        time.sleep(0.5)
    
    def select_time_slot(self, time_str):
        time.sleep(0.5)
        slots = self.driver.find_elements(*self.SLOT_BUTTONS)
        for slot in slots:
            if slot.get_attribute("data-time") == time_str:
                self.driver.execute_script("arguments[0].scrollIntoView();", slot)
                self.wait.until(EC.element_to_be_clickable(slot))
                slot.click()
                time.sleep(0.5)
                return
        raise Exception(f"Slot {time_str} not found")
    
    def set_attendee_name(self, name):
        name_input = self.wait.until(EC.presence_of_element_located(self.ATTENDEE_NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)
        time.sleep(0.3)
    
    def set_attendee_email(self, email):
        email_input = self.wait.until(EC.presence_of_element_located(self.ATTENDEE_EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(0.3)
    
    def set_attendee_phone(self, phone):
        phone_input = self.driver.find_element(*self.ATTENDEE_PHONE_INPUT)
        phone_input.clear()
        phone_input.send_keys(phone)
        time.sleep(0.3)
    
    def submit_booking(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()
        time.sleep(1)
    
    def wait_for_success_message(self, timeout=5):
        success_msg = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
        )
        return success_msg.text
    
    def get_error_message(self, error_type):
        error_map = {
            "eventType": self.EVENT_TYPE_ERROR,
            "date": self.DATE_ERROR,
            "slot": self.SLOT_ERROR,
            "name": self.NAME_ERROR,
            "email": self.EMAIL_ERROR,
        }
        error_element = self.driver.find_element(*error_map[error_type])
        return error_element.text
    
    def fill_booking_form(self, booking_data):
        self.select_event_type(booking_data['eventType'])
        self.set_booking_date(booking_data['date'])
        self.select_time_slot(booking_data['time'])
        self.set_attendee_name(booking_data['name'])
        self.set_attendee_email(booking_data['email'])
        if 'phone' in booking_data:
            self.set_attendee_phone(booking_data['phone'])