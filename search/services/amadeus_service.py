# search/services/amadeus_service.py
from amadeus import Client, ResponseError
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Amadeus client
amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY'),
    client_secret=os.getenv('AMADEUS_API_SECRET')
)


def search_flights(origin, destination, departure_date, return_date=None):
    try:
        kwargs = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": 1,
        }
        if return_date:
            kwargs["returnDate"] = return_date

        response = amadeus.shopping.flight_offers_search.get(**kwargs)
        logger.info(f"API Response: {response.data}")  # Log the API response
        return response.data
    except ResponseError as error:
        error_detail = error.response.data.get("errors", [{}])[0].get("detail", "Unknown error")
        raise Exception(f"Flight Search Error: {error_detail}")
