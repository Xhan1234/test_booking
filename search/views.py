# search/views.py
from django.shortcuts import render
from django.contrib import messages
from .services.amadeus_service import search_flights


def search_flights_view(request):
    context = {}
    if request.method == 'POST':
        origin = request.POST.get("origin")
        destination = request.POST.get("destination")
        departure_date = request.POST.get("departure_date")
        return_date = request.POST.get("return_date")

        if origin and destination and departure_date:
            try:
                raw_flights = search_flights(origin, destination, departure_date, return_date)

                                # Extract flight offers
                flights = []
                for offer in raw_flights:
                    flight = {
                        'id': offer.get('id'),
                        'price': offer.get('price', {}).get('total'),
                        'currency': offer.get('price', {}).get('currency'),
                        'itineraries': []
                    }

                    for itinerary in offer.get('itineraries', []):
                        segments = []
                        for segment in itinerary.get('segments', []):
                            segments.append({
                                'departure': segment.get('departure', {}).get('at'),
                                'arrival': segment.get('arrival', {}).get('at'),
                                'duration': segment.get('duration'),
                                'carrier': segment.get('carrierCode'),
                                'flight_number': segment.get('number')
                            })

                        flight['itineraries'].append({
                            'duration': itinerary.get('duration'),
                            'segments': segments
                        })

                    flights.append(flight)

                context['flights'] = flights
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Please provide all required fields.")

    return render(request, 'flight/index.html', context)
