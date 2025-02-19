import serial
import time
import requests

# Define serial port and baud rate (adjust based on your Arduino configuration)
SERIAL_PORT = "COM3"  # Change to "/dev/ttyUSB0" on Linux/Mac
BAUD_RATE = 9600

# (Optional) IoT server for logging data
IOT_SERVER_URL = "https://your-iot-server.com/log"  # Replace with actual endpoint

def log_data(distance):
    """Logs obstacle data locally and optionally sends it to a cloud server."""
    log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Distance: {distance} cm"
    print(log_entry)

    # Save log to a local file
    with open("smart_cane_log.txt", "a") as file:
        file.write(log_entry + "\n")

    # (Optional) Send data to cloud
    try:
        response = requests.post(IOT_SERVER_URL, json={"distance": distance})
        if response.status_code == 200:
            print("Data sent to cloud successfully!")
        else:
            print("Failed to send data to cloud.")
    except Exception as e:
        print("Cloud connection error:", e)

def main():
    """Main function to read sensor data and process alerts."""
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allow time for Arduino to initialize
        print("Connected to Arduino. Listening for data...")

        while True:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode('utf-8').strip()
                if data.isnumeric():
                    distance = int(data)
                    log_data(distance)
                    
                    # Alert the user if an obstacle is detected within 50 cm
                    if distance < 50:
                        print("Obstacle detected! Alerting user...\a")  # Beep sound
                time.sleep(1)  # Avoid excessive reads

    except serial.SerialException:
        print("Error: Could not connect to Arduino. Check connection.")
    except KeyboardInterrupt:
        print("Stopping program...")
    finally:
        if 'arduino' in locals():
            arduino.close()

if __name__ == "__main__":
    main()
