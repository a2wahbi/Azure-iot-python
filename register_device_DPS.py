import time
import base64
import hmac
import hashlib
from azure.iot.device import ProvisioningDeviceClient, IoTHubDeviceClient, Message

# 🔹 Constants (Replace with your values)
ID_SCOPE = "0ne00E8DE11"
PRIMARY_KEY = "hwNRVJjGdSXvljynTDGaaU8inAQgwktTpoSOLK6gVYEQD9ShL6qO10IW9ZZGoLoVjDq+RrTuTU+NAIoT3UNkmg=="
DEVICE_ID = "dev-group-2"
GLOBAL_ENDPOINT = "global.azure-devices-provisioning.net"

# 🔹 Function to Compute Derived Symmetric Key
def compute_derived_symmetric_key(master_key: str, registration_id: str) -> str:
    """Computes a derived symmetric key using HMAC-SHA256."""
    master_key_bytes = base64.b64decode(master_key)
    message_bytes = registration_id.encode('utf-8')
    hmac_key = hmac.new(master_key_bytes, message_bytes, hashlib.sha256).digest()
    return base64.b64encode(hmac_key).decode('utf-8')

# 🔹 Function to Run Device Provisioning & Telemetry
def run_sample():
    print("🚀 Initializing the device provisioning client...")

    # Compute the derived key
    derived_key = compute_derived_symmetric_key(PRIMARY_KEY, DEVICE_ID)

    # Create Provisioning Client
    prov_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=GLOBAL_ENDPOINT,
        registration_id=DEVICE_ID,
        id_scope=ID_SCOPE,
        symmetric_key=derived_key
    )

    # Register the device (REMOVED `await`)
    print("📡 Registering with the device provisioning service...")
    registration_result = prov_client.register()

    # Check Registration Status
    if registration_result.status != "assigned":
        print(f"❌ Registration failed: {registration_result.registration_state}")
        return

    print(f"✅ Device {registration_result.registration_state.device_id} registered to {registration_result.registration_state.assigned_hub}")

    # Create IoT Hub Client
    print("🔐 Creating symmetric key authentication for IoT Hub...")
    iot_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=derived_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id
    )

    # Send Telemetry
    print("📨 Sending a telemetry message...")
    msg = Message("TestMessage")
    iot_client.send_message(msg)

    print("✅ Telemetry message sent successfully!")

    # Close the connection
    iot_client.shutdown()
    print("🏁 Finished.")

# Run the function
run_sample()
