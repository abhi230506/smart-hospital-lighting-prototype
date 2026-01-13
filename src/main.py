import network
import socket
from machine import ADC, Pin
import time
import math
import ujson
import utime

# Access Point Setup
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='IllumiNation_AP', password='smartlight123')

while not ap.active():
    pass

print("Access Point ready. Go to: http://192.168.4.1")

# Hardware Setup
light_sensor = ADC(Pin(26))
motion_sensor = ADC(Pin(27))
temp_adc = ADC(2)
led = Pin(16, Pin.OUT)

# Thermistor Constants
BETA = 3933
SERIES_RESISTOR = 10000
NOMINAL_RESISTANCE = 100000
NOMINAL_TEMPERATURE = 25 + 273.15

# Thresholds
LIGHT_THRESHOLD = 55000
MOTION_THRESHOLD = 46000

# State Flags
manual_on = False
ambient_mode = False
motion_mode = False

# Utility Functions
def read_temperature():
    analog = temp_adc.read_u16()
    voltage = analog * 3.3 / 65535
    resistance = SERIES_RESISTOR * voltage / (3.3 - voltage)
    temp_kelvin = 1 / (1 / NOMINAL_TEMPERATURE + (1 / BETA) * math.log(resistance / NOMINAL_RESISTANCE))
    temp_celsius = temp_kelvin - 273.15
    return round(temp_celsius, 1)

def get_status():
    return f"Light: {'ON' if led.value() else 'OFF'} | Ambient Mode: {'ON' if ambient_mode else 'OFF'} | Motion Mode: {'ON' if motion_mode else 'OFF'}"

def get_greeting():
    hour = (utime.localtime()[3] + 1) % 24
    if 5 <= hour < 12:
        return "Good Morning, Abhi!"
    elif 12 <= hour < 17:
        return "Good Afternoon, Abhi!"
    elif 17 <= hour < 21:
        return "Good Evening, Abhi!"
    else:
        return "Goodnight, Abhi!"

def webpage():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
      background-color: #121212;
      color: #f5f5f7;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 0;
      padding: 0;
    }
    .header {
      width: 90%;
      max-width: 400px;
      display: flex;
      justify-content: space-between;
      margin-top: 20px;
      color: #a1a1aa;
      font-size: 14px;
    }
    .greeting {
      width: 90%;
      max-width: 400px;
      text-align: left;
      margin-top: 10px;
    }
    .greeting h1 {
      margin: 0;
      font-weight: 600;
      font-size: 24px;
    }
    .card-container {
      width: 90%;
      max-width: 400px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 20px;
    }
    .card {
      background: #1c1c1e;
      border-radius: 14px;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .label {
      color: #a1a1aa;
      font-size: 14px;
    }
    .value {
      font-size: 20px;
      font-weight: 600;
    }
    .power-button {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      margin-top: 25px;
      background-color: #1c1c1e;
      border: 2px solid #f5f5f7;
      color: #f5f5f7;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    .power-on {
      background-color: #f5f5f7;
      color: #1c1c1e;
    }
    .toggle-row {
      display: flex;
      justify-content: space-between;
      width: 90%;
      max-width: 400px;
      margin-top: 20px;
      margin-bottom: 20px;
    }
    .toggle-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    .switch {
      position: relative;
      display: inline-block;
      width: 50px;
      height: 28px;
    }
    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0;
      right: 0; bottom: 0;
      background-color: #3a3a3c;
      transition: .4s;
      border-radius: 28px;
    }
    .slider:before {
      position: absolute;
      content: "";
      height: 22px;
      width: 22px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .4s;
      border-radius: 50%;
    }
    input:checked + .slider {
      background-color: #4cd964;
    }
    input:checked + .slider:before {
      transform: translateX(22px);
    }
    </style>
    </head>
    <body>

    <div class="header">
      <div>IllumiNation</div>
      <div>Apr 1st</div>
    </div>

    <div class="greeting">
      <h1 id="greeting">Loading...</h1>
    </div>

    <div class="card-container">
      <div class="card">
        <div class="label">Temperature</div>
        <div class="value"><span id="temp">--</span></div>
      </div>
      <div class="card">
        <div class="label">Room Brightness</div>
        <div class="value"><span id="brightness">--</span></div>
      </div>
    </div>

    <button id="powerButton" class="power-button" onclick="toggleMode('manual')">&#x23FB;</button>

    <div class="toggle-row">
      <div class="toggle-container">
        <span>Ambient</span>
        <label class="switch">
          <input type="checkbox" id="ambientSwitch" onchange="toggleMode('ambient')">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-container">
        <span>Motion</span>
        <label class="switch">
          <input type="checkbox" id="motionSwitch" onchange="toggleMode('motion')">
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <script>
    async function fetchData() {
      try {
        const res = await fetch('/data');
        const data = await res.json();
        document.getElementById('brightness').textContent = data.brightness;
        document.getElementById('temp').textContent = data.temp;
        document.getElementById('greeting').textContent = data.greeting;
        document.getElementById('powerButton').classList.toggle('power-on', data.manual);
        document.getElementById('ambientSwitch').checked = data.ambient;
        document.getElementById('motionSwitch').checked = data.motion;
      } catch (err) {
        console.error('Error fetching data:', err);
      }
    }

    async function toggleMode(mode) {
      try {
        await fetch('/toggle', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ mode: mode })
        });
        fetchData();
      } catch (err) {
        console.error('Error toggling mode:', err);
      }
    }

    setInterval(fetchData, 1000);
    fetchData();
    </script>

    </body>
    </html>
    """
    return html

# Web Server Setup
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

# Main Loop
while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()

    if 'POST /toggle' in request:
        content_length = 0
        for line in request.split('\r\n'):
            if line.lower().startswith('content-length:'):
                content_length = int(line.split(':')[1].strip())
        body = conn.recv(content_length).decode()
        data = ujson.loads(body)

        mode = data.get('mode')
        if mode == 'manual':
            manual_on = not manual_on
            ambient_mode = False
            motion_mode = False
            led.value(1 if manual_on else 0)
        elif mode == 'ambient':
            ambient_mode = not ambient_mode
            manual_on = False
            motion_mode = False
        elif mode == 'motion':
            motion_mode = not motion_mode
            manual_on = False
            ambient_mode = False

        conn.send("HTTP/1.1 200 OK\n\n")
        conn.close()
        continue

    if '/data' in request:
        light_value = light_sensor.read_u16()
        temp = read_temperature()
        brightness = "Dark" if light_value > LIGHT_THRESHOLD else "Bright"

        if not manual_on:
            if ambient_mode:
                led.value(1 if light_value > LIGHT_THRESHOLD else 0)
            elif motion_mode:
                ir_value = motion_sensor.read_u16()
                led.value(1 if ir_value > MOTION_THRESHOLD else 0)

        data = {
            "brightness": brightness,
            "temp": temp,
            "status": get_status(),
            "greeting": get_greeting(),
            "manual": manual_on,
            "ambient": ambient_mode,
            "motion": motion_mode
        }
        conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n")
        conn.sendall(ujson.dumps(data))
        conn.close()
        continue

    response = webpage()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n")
    conn.sendall(response)
    conn.close()

    time.sleep(0.1)
