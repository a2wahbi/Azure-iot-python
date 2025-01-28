"""
File: receive_cloud_to_device_messages.py
Description: This script listens for Cloud-to-Device (C2D) messages from Azure IoT Hub using the IoTHubDeviceClient class. 
It is designed to simulate an IoT device that receives commands or notifications sent by the cloud.

Author: Wahbi
Date: 28/01/2025

Key Features:
- Connects to Azure IoT Hub using a device connection string stored in the environment variable `IOTHUB_DEVICE_CONNECTION_STRING`.
- Listens continuously for Cloud-to-Device (C2D) messages from the IoT Hub.
- Decodes and displays the message content and custom properties in the console.
- Allows the user to terminate the message listening process by typing "Q" in the console.
- Implements proper resource management by shutting down the IoT client gracefully.

Requirements:
- Install the `azure-iot-device` library using `pip install azure-iot-device`.
- Python 3.6+ is required.
- Set the IoT device connection string in the environment variable `IOTHUB_DEVICE_CONNECTION_STRING`.

Usage:
1. Ensure that the Azure IoT Hub is set up and the IoT device is registered to receive messages.
2. Set the device connection string in the `IOTHUB_DEVICE_CONNECTION_STRING` environment variable.
3. Run the script: `python receive_cloud_to_device_messages.py`.
4. Send a Cloud-to-Device (C2D) message from Azure IoT Hub to the registered device to test the functionality.
5. Press "Q" to stop the script and disconnect the IoT client.
"""


import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient


async def receive_messages_from_cloud(device_client):
    """
    Écoute les messages Cloud-to-Device (C2D) depuis Azure IoT Hub.
    """
    print("\n🔵 Écoute des messages Cloud-to-Device (C2D) en cours...")

    # Gestionnaire de réception des messages
    def message_received_handler(message):
        print("\n🟡 Message reçu : " + message.data.decode("utf-8"))
        print("📌 Propriétés : ", message.custom_properties)

    # Attacher le gestionnaire au client
    device_client.on_message_received = message_received_handler

    # Bloquer l'exécution jusqu'à ce que l'utilisateur quitte
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection.lower() == "q":
                print("Quitting...")
                break

    # Écoute des messages jusqu'à l'arrêt par l'utilisateur
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, stdin_listener)


async def main():
    """
    Point d'entrée principal de l'application IoT.
    """
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # Vérification de la variable d'environnement
    if not conn_str:
        print("❌ Erreur : La variable d'environnement IOTHUB_DEVICE_CONNECTION_STRING n'est pas définie.")
        return
    
    print(f"🔹 Connexion utilisée : {conn_str}")  # Debugging
    
    try:
        # Création du client IoT Hub
        device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        await device_client.connect()

        # Appeler la fonction pour écouter les messages
        await receive_messages_from_cloud(device_client)

    except Exception as e:
        print(f"❌ Erreur : {e}")
    
    finally:
        # Arrêter le client proprement
        await device_client.shutdown()
        print("🛑 Connexion fermée.")


if __name__ == "__main__":
    asyncio.run(main())
