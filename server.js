const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// Mock data
const eventTypes = {
  1: {
    id: 1,
    title: 'Consulta Inicial',
    description: 'Primera consulta de 30 minutos',
    length: 30,
    price: 0,
    requiresConfirmation: true,
    seatsPerTimeSlot: 4,
  },
  2: {
    id: 2,
    title: 'Seguimiento',
    description: 'Seguimiento de 15 minutos',
    length: 15,
    price: 0,
    requiresConfirmation: true,
    seatsPerTimeSlot: 2,
  },
  3: {
    id: 3,
    title: 'Sesión Completa',
    description: 'Sesión de 60 minutos',
    length: 60,
    price: 500,
    requiresConfirmation: true,
    seatsPerTimeSlot: 1,
  },
};

const bookings = [];
let bookingId = 1;

// Funciones de booking.ts
function getAvailableSlots(date) {
  const slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00'];
  return slots;
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isSlotAvailable(date, time, eventTypeId) {
  const availableSlots = getAvailableSlots(date);
  const bookingsForDate = bookings.filter(
    b => b.date === date && b.time === time && b.eventTypeId === eventTypeId
  );
  
  const eventType = eventTypes[eventTypeId];
  const seatsPerSlot = eventType?.seatsPerTimeSlot || 1;
  
  return availableSlots.includes(time) && bookingsForDate.length < seatsPerSlot;
}

//  RUTA API

app.get('/api/event-types', (req, res) => {
  res.json({
    success: true,
    data: Object.values(eventTypes),
  });
});

app.get('/api/available-slots', (req, res) => {
  const { date, eventTypeId } = req.query;
  const slots = getAvailableSlots(date);
  const availableSlots = slots.filter(slot => 
    isSlotAvailable(date, slot, eventTypeId)
  );
  
  res.json({
    success: true,
    data: { date, eventTypeId, availableSlots },
  });
});

app.post('/api/bookings', (req, res) => {
  const { eventTypeId, date, time, attendeeName, attendeeEmail, attendeePhone, description } = req.body;
  
  const errors = {};
  
  if (!eventTypeId) errors.eventType = 'Requerido';
  if (!date) errors.date = 'Requerido';
  if (!time) errors.time = 'Requerido';
  if (!attendeeName || attendeeName.length < 3) errors.name = 'Mínimo 3 caracteres';
  if (!attendeeEmail || !validateEmail(attendeeEmail)) errors.email = 'Inválido';
  
  if (Object.keys(errors).length > 0) {
    return res.status(400).json({ success: false, errors });
  }
  
  if (!isSlotAvailable(date, time, eventTypeId)) {
    return res.status(409).json({ success: false, error: 'No disponible' });
  }
  
  const eventType = eventTypes[eventTypeId];
  const booking = {
    id: bookingId++,
    eventTypeId,
    eventTitle: eventType.title,
    date,
    time,
    startTime: `${date}T${time}`,
    status: eventType.requiresConfirmation ? 'PENDING' : 'ACCEPTED',
    attendee: {
      name: attendeeName,
      email: attendeeEmail,
      phoneNumber: attendeePhone || null,
    },
    description: description || null,
  };
  
  bookings.push(booking);
  
  res.status(201).json({
    success: true,
    message: 'Cita agendada exitosamente',
    data: booking,
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(`
✓ Servidor en: http://localhost:5000
✓ Frontend: http://localhost:5000
✓ API: http://localhost:5000/api/event-types
  `);
});