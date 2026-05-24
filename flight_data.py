class FlightData:
    """Structure to hold the details of a specific flight."""
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data, return_date):
    """Parses SerpAPI flight data to find and return the cheapest FlightData object."""
    
    # Handle missing or empty data gracefully
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data available for this route.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    # Combine 'best_flights' and 'other_flights' arrays into a single list to iterate through
    all_flights = data.get("best_flights", []) + data.get("other_flights", [])

    # Set the first flight in the list as the baseline cheapest flight
    first_flight = all_flights[0]
    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0]

    # Initialize the baseline FlightData object
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    # Loop through all available flights to see if we can find a lower price
    for flight in all_flights:
        try:
            # Attempt to extract the price (some SerpAPI results might omit this)
            price = flight["price"]
        except KeyError:
            print("--- No price available for this specific flight block. Skipping. ---")
            continue
            
        # If we find a lower price, update our cheapest_flight object
        if price < lowest_price:
            lowest_price = price
            origin = flight["flights"][0]["departure_airport"]["id"]
            destination = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"New lowest price to {destination} found: GBP {lowest_price}")

    return cheapest_flight