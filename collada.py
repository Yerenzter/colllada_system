import serial
import socket
import time
import os

# Setup serial connection (adjust your port and baudrate)
ser = serial.Serial('COM3', 9600, timeout=1)  # or '/dev/ttyUSB0' on Linux

# Setup socket to send data to Bun.js server
HOST = '127.0.0.1'  # Bun.js server IP
PORT = 4435         # Port Bun.js server listens on

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Read from serial: {data}")
            sock.sendall(data.encode('utf-8') + b'\n')  # send data to Bun.js
            time.sleep(0.1)
finally:
    sock.close()
    ser.close()
