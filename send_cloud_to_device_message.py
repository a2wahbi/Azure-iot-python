"""
File: send_cloud_to_device_message.py
Description: This script demonstrates how to send a Cloud-to-Device (C2D) message from Azure IoT Hub to a specific IoT device using the IoTHubRegistryManager class from the Azure IoT SDK.

Author: Wahbi
Date: 27/01/2025

Key Features:
- Authenticates with Azure IoT Hub using a Service Connection String.
- Sends a Cloud-to-Device (C2D) message to a specific IoT device.
- Provides success and error feedback in the console for the message delivery process.

Requirements:
- Install the `azure-iot-hub` library using `pip install azure-iot-hub`.
- Python 3.6+ is required.
- A valid Azure IoT Hub service connection string is required in the `SERVICE_CONNECTION_STRING` variable.

Usage:
- Replace `SERVICE_CONNECTION_STRING` with your Azure IoT Hub service connection string.
- Replace `TARGET_DEVICE` with the name of the IoT device you want to target.
"""


from azure.iot.hub import IoTHubRegistryManager

# Chaîne de connexion pour le service Azure IoT Hub (Service Connection String)
SERVICE_CONNECTION_STRING = "HostName=exchangeDataWithVscode-Iothub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=dyCR+/cyRGJIKjEtsovkbVsU4Tuez2YLWAIoTCusmU0="
# Nom du device cible
TARGET_DEVICE = "iotdev1"

def send_cloud_to_device_message():
    """
    Envoie un message Cloud-to-Device (C2D) à un appareil spécifique via Azure IoT Hub.
    """
    print("🔵 Connexion au IoT Hub...")
    # Créer une instance de IoTHubRegistryManager
    registry_manager = IoTHubRegistryManager(SERVICE_CONNECTION_STRING)

    try:
        # Message à envoyer
        message = "This is a test message from Python"
        print(f"📤 Envoi du message C2D au device '{TARGET_DEVICE}' : {message}")

        # Envoi du message au device cible
        registry_manager.send_c2d_message(TARGET_DEVICE, message)
        print("✅ Message envoyé avec succès.")

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du message : {e}")

if __name__ == "__main__":
    print("🌍 Azure IoT Hub - Envoi d'un Message Cloud-to-Device (C2D)")
    send_cloud_to_device_message()
