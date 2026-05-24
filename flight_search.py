import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SerpAPI endpoint for Google Flights
SERPAPI_ENDPOINT = "https://serpapi.com/search"

class FlightSearch:
    """Class responsible for talking to the Flight Search API."""

    def __init__(self):
        # Retrieve the SerpAPI key from environment variables
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """Queries SerpAPI for flights between two cities within a date range."""

        # Build the query dictionary based on SerpAPI's required parameters
        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",          # 1 = Round trip
            "adults": "1",        # Number of adult passengers
            "currency": "GBP",    # Desired currency for the prices
            "api_key": self._api_key,
        }

        # Make the GET request to SerpAPI
        response = requests.get(url=SERPAPI_ENDPOINT, params=query)

        # Handle non-200 status codes (e.g., unauthorized, bad request)
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            return None

        # Parse the JSON response
        data = response.json()

        # Check if SerpAPI returned a specific error message inside the JSON
        if "error" in data:
            print(f"API error: {data['error']}")
            return None

        return data