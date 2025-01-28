import time
import base64
import hmac
import hashlib
import urllib.parse
from azure.iot.device import ProvisioningDeviceClient, IoTHubDeviceClient, Message

# 🔹 Constants (Replace with your values)
ID_SCOPE = "0ne00E8DE11"
PRIMARY_KEY = "hwNRVJjGdSXvljynTDGaaU8inAQgwktTpoSOLK6gVYEQD9ShL6qO10IW9ZZGoLoVjDq+RrTuTU+NAIoT3UNkmg=="
DEVICE_ID = "dev-group-1"
GLOBAL_ENDPOINT = "global.azure-devices-provisioning.net"
HUB_HOSTNAME = "your-iot-hub-hostname.azure-devices.net"  # Replace with your IoT Hub hostname

# 🔹 Function to Compute Derived Symmetric Key
def compute_derived_symmetric_key(master_key: str, registration_id: str) -> str:
    """Computes a derived symmetric key using HMAC-SHA256."""
    master_key_bytes = base64.b64decode(master_key)
    message_bytes = registration_id.encode('utf-8')
    hmac_key = hmac.new(master_key_bytes, message_bytes, hashlib.sha256).digest()
    return base64.b64encode(hmac_key).decode('utf-8')

# 🔹 Function to Generate a SAS Token
def generate_sas_token(resource_uri: str, key: str, expiry_in_seconds: int = 3600) -> str:
    """Generates a SAS token."""
    expiry = int(time.time()) + expiry_in_seconds
    to_sign = f"{resource_uri}\n{expiry}"
    key_bytes = base64.b64decode(key)
    signature = hmac.new(key_bytes, to_sign.encode('utf-8'), hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    signature_escaped = urllib.parse.quote(signature_b64, safe='')

    sas_token = f"SharedAccessSignature sr={resource_uri}&sig={signature_escaped}&se={expiry}"
    return sas_token

# 🔹 Function to Run Device Telemetry
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

    # Register the device
    print("📡 Registering with the device provisioning service...")
    registration_result = prov_client.register()

    # Check Registration Status
    if registration_result.status != "assigned":
        print(f"❌ Registration failed: {registration_result.registration_state}")
        return

    print(f"✅ Device {registration_result.registration_state.device_id} registered to {registration_result.registration_state.assigned_hub}")

    # Create IoT Hub Client
    print("🔐 Creating IoT Hub client...")
    resource_uri = f"{HUB_HOSTNAME}/devices/{DEVICE_ID}"
    iot_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=derived_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id
    )

    # Send Telemetry Every 5 Minutes
    print("📨 Starting to send telemetry every 1 minutes...")
    while True:
        sas_token = generate_sas_token(resource_uri, derived_key, expiry_in_seconds=60)  # 5 minutes token
        print(f"🔑 New SAS Token Generated: {sas_token}")

        msg = Message("TestMessage with new SAS token")
        iot_client.send_message(msg)
        print("✅ Telemetry message sent successfully!")
        time.sleep(60)  # Wait 5 minutes

# Run the function
run_sample()
