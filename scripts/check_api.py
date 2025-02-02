import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("GOOGLE_MAPS_API_KEY")
test_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name&key={api_key}"

response = requests.get(test_url)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")