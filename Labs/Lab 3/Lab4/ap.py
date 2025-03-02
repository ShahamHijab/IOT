import network

ssid = "Shaham-ESP"
password = "shaham1234"  # Minimum 8 characters
auth_mode = network.AUTH_WPA2_PSK  # Secure mode (recommended)

# Create an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)  # Activate AP mode
ap.config(essid=ssid, password=password, authmode=auth_mode)  # Set SSID and password

print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])