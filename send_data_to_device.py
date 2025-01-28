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
