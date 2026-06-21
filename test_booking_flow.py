import pytest
from datetime import datetime, timedelta

class TestBookingFlowValidCases:
    def test_successful_booking_with_valid_data(self, booking_page):
        """Caso 1: Usuario reserva con datos válidos"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_data = {
            'eventType': '1',
            'date': tomorrow,
            'time': '10:00',
            'name': 'Juan Pérez García',
            'email': 'juan.perez@example.com',
        }
        
        booking_page.fill_booking_form(booking_data)
        booking_page.submit_booking()
        
        success_message = booking_page.wait_for_success_message()
        assert 'exitosamente' in success_message.lower()
        assert booking_data['email'] in success_message
    
    def test_booking_without_phone(self, booking_page):
        """Caso 2: Reserva sin teléfono (opcional)"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_data = {
            'eventType': '2',
            'date': tomorrow,
            'time': '14:00',
            'name': 'María López',
            'email': 'maria@example.com'
        }
        
        booking_page.fill_booking_form(booking_data)
        booking_page.submit_booking()
        
        success_message = booking_page.wait_for_success_message()
        assert 'exitosamente' in success_message.lower()

class TestBookingFlowBoundaryConditions:
    def test_minimum_name_length(self, booking_page):
        """Caso 3: Nombre con 3 caracteres (mínimo)"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_data = {
            'eventType': '1',
            'date': tomorrow,
            'time': '09:00',
            'name': 'Ana',
            'email': 'ana@example.com'
        }
        
        booking_page.fill_booking_form(booking_data)
        booking_page.submit_booking()
        
        success_message = booking_page.wait_for_success_message()
        assert 'exitosamente' in success_message.lower()

class TestBookingFlowErrorCases:
    def test_booking_without_event_type(self, booking_page):
        """Caso 4: Error sin tipo de evento"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_page.set_booking_date(tomorrow)
        booking_page.select_time_slot('10:00')
        booking_page.set_attendee_name('Test User')
        booking_page.set_attendee_email('test@example.com')
        booking_page.submit_booking()
        
        error = booking_page.get_error_message('eventType')
        assert len(error) > 0
    
    def test_booking_without_date(self, booking_page):
        """Caso 5: Error sin fecha"""
        booking_page.select_event_type('1')
        booking_page.select_time_slot('10:00')
        booking_page.set_attendee_name('Test')
        booking_page.set_attendee_email('test@example.com')
        booking_page.submit_booking()
        
        error = booking_page.get_error_message('date')
        assert len(error) > 0
    
    def test_booking_without_time(self, booking_page):
        """Caso 6: Error sin horario"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_page.select_event_type('1')
        booking_page.set_booking_date(tomorrow)
        booking_page.set_attendee_name('Test')
        booking_page.set_attendee_email('test@example.com')
        booking_page.submit_booking()
        
        error = booking_page.get_error_message('slot')
        assert len(error) > 0
    
    def test_invalid_email(self, booking_page):
        """Caso 7: Error con correo inválido"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_page.select_event_type('1')
        booking_page.set_booking_date(tomorrow)
        booking_page.select_time_slot('10:00')
        booking_page.set_attendee_name('Test')
        booking_page.set_attendee_email('invalid-email')
        booking_page.submit_booking()
        
        error = booking_page.get_error_message('email')
        assert len(error) > 0
    
    def test_short_name(self, booking_page):
        """Caso 8: Error con nombre muy corto"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_page.select_event_type('1')
        booking_page.set_booking_date(tomorrow)
        booking_page.select_time_slot('10:00')
        booking_page.set_attendee_name('AB')
        booking_page.set_attendee_email('ab@example.com')
        booking_page.submit_booking()
        
        error = booking_page.get_error_message('name')
        assert len(error) > 0

@pytest.mark.parametrize("event_type,time", [
    ("1", "09:00"),
    ("1", "10:00"),
    ("2", "14:00"),
    ("3", "15:00"),
])
class TestBookingFlowDataDriven:
    def test_booking_combinations(self, booking_page, event_type, time):
        """Casos 9-12: Pruebas parametrizadas"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_data = {
            'eventType': event_type,
            'date': tomorrow,
            'time': time,
            'name': f'Test {event_type}',
            'email': f'user{event_type}@example.com'
        }
        
        booking_page.fill_booking_form(booking_data)
        booking_page.submit_booking()
        
        success_message = booking_page.wait_for_success_message()
        assert 'exitosamente' in success_message.lower()
        