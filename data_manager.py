import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from the .env file to keep credentials secure
load_dotenv()

# The endpoint URL for your Sheety project
SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"]

class DataManager:
    """Class responsible for talking to the Google Sheet API."""

    def __init__(self):
        # Retrieve Sheety basic authentication credentials
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        # Initialize the HTTP Basic Auth object
        self._authorization = HTTPBasicAuth(self._user, self._password)
        # Initialize an empty dictionary to hold the destination data
        self.destination_data = {}

    def get_destination_data(self):
        """Fetches the current data from the Google Sheet."""
        # Make a GET request to Sheety with Basic Auth
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()

        # Extract the 'prices' list from the JSON response
        self.destination_data = data["prices"]
        return self.destination_data

    def update_lowest_price(self, row_id, new_price):
        """Updates the lowest price in a specific row of the Google Sheet."""
        # Construct the JSON payload required by Sheety (root key matches the sheet name 'price')
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        # Make a PUT request to update the specific row ID
        response = requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization
        )
        response.raise_for_status() # Raises an exception if the HTTP request returned an error