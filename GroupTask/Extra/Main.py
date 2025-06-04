import network
import machine
import dht
import ssd1306
import time
import socket
import os
import ubinascii
import gc
from neopixel import NeoPixel

# Wi-Fi Setup
SSID = "Wifi-79J"
PASSWORD = "797979jjjj"

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

timeout = 10
while not sta.isconnected() and timeout > 0:
    print("Connecting to WiFi...")
    time.sleep(1)
    timeout -= 1

if sta.isconnected():
    print("Connected! IP:", sta.ifconfig()[0])
else:
    print("Failed to connect to WiFi")

# Access Point Setup (Optional)
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="SSS", password="12345678", authmode=network.AUTH_WPA2_PSK)
print("Access Point Active, IP:", ap.ifconfig()[0])

# Initialize Components
dht_sensor = dht.DHT11(machine.Pin(4))
i2c = machine.I2C(scl=machine.Pin(9), sda=machine.Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
pin = machine.Pin(48, machine.Pin.OUT)
neo = NeoPixel(pin, 1)

# Store last encrypted text
last_encrypted = ""

def set_color(r, g, b):
    neo[0] = (r, g, b)
    neo.write()

def display_text_on_oled(text):
    oled.fill(0)
    oled.text("OLED Display:", 0, 0)
    oled.text(text[:16], 0, 20)
    oled.text(text[16:32], 0, 40)
    oled.show()

def encrypt_text(data):
    global last_encrypted
    key = 42
    encrypted = ubinascii.hexlify(bytes([b ^ key for b in data.encode()])).decode()
    last_encrypted = encrypted
    display_text_on_oled(encrypted)
    return encrypted

def decrypt_text(data):
    key = 42
    decrypted = bytes([b ^ key for b in ubinascii.unhexlify(data)]).decode()
    display_text_on_oled(last_encrypted + " -> " + decrypted)
    return decrypted

def list_files():
    return "\n".join(os.listdir())

def get_system_info():
    total_ram = gc.mem_alloc() + gc.mem_free()
    used_ram = gc.mem_alloc()
    free_ram = gc.mem_free()
    return f"Total RAM: {total_ram} bytes\nUsed RAM: {used_ram} bytes\nFree RAM: {free_ram} bytes"

def read_file(filename):
    """Reads and returns the content of an HTML file."""
    try:
        with open(filename, "r") as file:
            return file.read()
    except:
        return "<h1>File Not Found</h1>"

def web_server():
    server = socket.socket()
    server.bind(("", 80))
    server.listen(5)
    print("Web Server Running on IP:", sta.ifconfig()[0])

    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()

        if "GET / " in request or "GET /home.html" in request:
            response = read_file("home.html")
            content_type = "text/html"

        elif "GET /index.html" in request:
            response = read_file("index.html")
            content_type = "text/html"

        elif "GET /sensorData" in request:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            oled.fill(0)
            oled.text(f"Temp: {temp}C", 0, 10)
            oled.text(f"Humidity: {humidity}%", 0, 30)
            oled.show()
            response = f'{{"temperature": {temp}, "humidity": {humidity}}}'
            content_type = "application/json"

        elif "GET /files" in request:
            response = list_files()
            content_type = "text/plain"

        elif "GET /system" in request:
            response = get_system_info()
            content_type = "text/plain"

        elif "POST /encrypt" in request:
            content = request.split("\r\n\r\n")[-1]
            response = encrypt_text(content)
            content_type = "text/plain"

        elif "POST /decrypt" in request:
            content = request.split("\r\n\r\n")[-1]
            response = decrypt_text(content)
            content_type = "text/plain"

        else:
            response = "<h1>404 Not Found</h1>"
            content_type = "text/html"

        # Send the HTTP response
        conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(response)}\r\n\r\n".encode())
        conn.sendall(response.encode())
        conn.close()
        gc.collect()

web_server()
