import requests
from googlemaps import convert
from flask import json

def distance_matrix(origin, destination):
    """Return dictionary as trip_id: distance pairs."""
    # Google Distance Matrix API set up
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    payload = {
        "origins": convert.location_list(origin),
        "destinations": convert.location_list(destination),
        "units": "imperial"
    }

    distance_meters = None
    distance_miles = None

    try:
        r = requests.get(base_url, params=payload)
        r.raise_for_status()  # Raise an HTTPError for bad responses

        response_dict = r.json()

        # Check if 'rows' and 'elements' are present and non-empty
        if 'rows' in response_dict and response_dict['rows']:
            first_row = response_dict['rows'][0]
            if 'elements' in first_row and first_row['elements']:
                first_element = first_row['elements'][0]
                # Check if 'distance' is present
                if 'distance' in first_element:
                    distance_meters = first_element['distance'].get('value')
                    distance_miles = first_element['distance'].get('text')

    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON decoding error occurred: {err}")

    return (distance_meters, distance_miles)
