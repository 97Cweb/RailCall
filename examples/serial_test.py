import serial
import time

PORT = '/dev/ttyUSB0'  # Adjust this if needed
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=2)

# Send a ping
message = b'ping\n'
ser.write(message)
print(f'Sent: {message.strip()}')

# Wait for reply
response = ser.readline().strip()
print(f'Received: {response}')

