# Azure IoT Hub Scripts

## Overview
This repository contains three Python scripts designed to interact with Azure IoT Hub. Each script serves a distinct purpose in device-to-cloud (D2C) or cloud-to-device (C2D) communication.

## Comparison of Scripts

| Aspect                        | `send_telemetry_to_cloud.py`            | `receive_messages_from_cloud.py`          | `send_cloud_to_device_message.py`         |
|--------------------------------|-----------------------------------------|-------------------------------------------|-------------------------------------------|
| **Communication Direction**   | Device-to-Cloud (D2C)                   | Cloud-to-Device (C2D)                     | Cloud-to-Device (C2D)                     |
| **Authentication**            | Device connection string                | Device connection string                  | Service connection string                 |
| **Purpose**                   | Simulates sending telemetry to the cloud | Listens for commands/messages from the cloud | Sends commands/messages to a device      |
| **Target**                    | IoT device sending data                 | IoT device receiving messages             | Admin/server sending messages to a device |
| **Use Case**                  | Data pipeline simulation                | Command/message reception                 | Command/message delivery                  |
| **Frequency**                 | Periodic (e.g., every second)           | Continuous listening                      | One-time message delivery                 |

## Script Descriptions

### 1. `send_telemetry_to_cloud.py`
- Simulates an IoT device sending periodic telemetry data (e.g., temperature, humidity) to Azure IoT Hub.
- Includes features like JSON message formatting and custom properties (`temperatureAlert`).
- **Usage**: Simulate device telemetry for testing or data pipeline validation.

### 2. `receive_messages_from_cloud.py`
- Listens for Cloud-to-Device (C2D) messages sent by Azure IoT Hub to a specific device.
- Decodes message content and handles custom properties.
- **Usage**: Simulate an IoT device receiving commands or alerts from Azure IoT Hub.

### 3. `send_cloud_to_device_message.py`
- Sends a Cloud-to-Device (C2D) message from Azure IoT Hub to a specific IoT device.
- Uses a service connection string for authentication.
- **Usage**: Server-side command or alert delivery to IoT devices.

---

## Requirements
- Python 3.6+
- Azure IoT SDKs:
  - `azure-iot-device`
  - `azure-iot-hub`
- Environment variables or hardcoded values for connection strings.

---

