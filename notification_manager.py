import os
from twilio.rest import Client

class NotificationManager:
    """Class responsible for sending notifications via Twilio."""

    def __init__(self):
        # Initialize the Twilio client using Account SID and Auth Token from environment variables
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])

    def send_sms(self, message_body):
        """Sends an SMS text message."""
        message = self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
            body=message_body,
            to=os.environ["TWILIO_VERIFIED_NUMBER"]
        )
        # Print the message SID to console to confirm successful delivery
        print(f"SMS Sent! SID: {message.sid}")

    def send_whatsapp(self, message_body):
        """Sends a WhatsApp message using the Twilio Sandbox."""
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body=message_body,
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'
        )
        # Print the message SID to console to confirm successful delivery
        print(f"WhatsApp Sent! SID: {message.sid}")