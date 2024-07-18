import requests
from config import geo_token


def geocoder(latitude, longitude):
    headers = {"Accept-Language": "ru"}
    address = requests.get(
        f'https://eu1.locationiq.com/v1/reverse.php?key={geo_token}&lat={latitude}&lon={longitude}&format=json',
        headers=headers).json()
    actual_address = f'{address["address"].get("city")}, {address["address"].get("road")}'
    try:
        actual_address += f', {address["house_number"]}'
    except Exception:
        pass
    return actual_address
