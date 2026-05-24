import requests_cache
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Conserve requests and preserve your free plan ====================
# This caches standard requests for 1 hour (3600 seconds) so you don't burn through your SerpAPI quota.
# It explicitly tells the script DO_NOT_CACHE for Sheety, ensuring you always get real-time spreadsheet updates.
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

# ==================== Setup ====================
# Instantiate the helper classes
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Fetch the list of desired destinations and current lowest prices from Google Sheets
sheet_data = data_manager.get_destination_data()

# ==================== Set the Dates and Origin Airport ====================
# We want to search for flights from tomorrow, up to 6 months (180 days) from today
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
ORIGIN_CITY_IATA = "LHR"  # London Heathrow

# ==================== Find Cheap Flights ====================
# Iterate through every row (destination) in the Google Sheet
for destination in sheet_data:
    print(f"\nGetting flights for {destination['city']}...")

    # Ask SerpAPI for flights to this specific destination
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    # Parse the returned data to find the absolute cheapest flight
    cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))
    print(f"{destination['city']}: GBP {cheapest_flight.price}")

    # Check if the cheapest flight is valid AND cheaper than our historical lowest price
    # The short-circuit '!=' check prevents a TypeError when comparing "N/A" to an integer.
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}! Sending alert...")

        # Update the Google Sheet with the new historical low
        data_manager.update_lowest_price(destination["id"], cheapest_flight.price)

        # Build the alert message string
        alert_message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")

        # Send the notification via WhatsApp (uncomment send_sms if you prefer standard texting)
        notification_manager.send_whatsapp(message_body=alert_message)