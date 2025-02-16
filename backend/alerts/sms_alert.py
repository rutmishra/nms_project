from twilio.rest import Client

TWILIO_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_NUMBER = "+1234567890"

def send_sms_alert(device_name, recipient):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=f"{device_name} is DOWN!", from_=TWILIO_NUMBER, to=recipient)
