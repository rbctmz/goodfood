import requests
import json
from typing import Dict, Any
import os
from time import sleep
import logging
from dotenv import load_dotenv

# Константы
DEFAULT_TIMEOUT = 10
DEFAULT_RADIUS = 5000
MIN_DELAY = 0.1

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('google_maps.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoogleMapsAPI:
    BASE_URL = "https://maps.googleapis.com/maps/api"
    
    def __init__(self, api_key: str):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("Invalid API key format")
        self.api_key = api_key
        self.last_request_time = 0
        logger.info("GoogleMapsAPI initialized")

    def _rate_limit(self):
        """Простой rate limiting"""
        sleep(MIN_DELAY)
        
    def search_places(self, query: str, location: str = None, radius: int = DEFAULT_RADIUS) -> Dict[str, Any]:
        """
        Search for places using Google Maps Text Search API
        
        Args:
            query: Search query string
            location: Optional coordinates string "lat,lng"
            radius: Search radius in meters, must be positive
            
        Returns:
            Dict with search results and status
        """
        if radius <= 0:
            raise ValueError("Radius must be positive")
            
        self._rate_limit()
        
        params = {
            "query": query,
            "key": self.api_key
        }
        if location:
            params.update({"location": location, "radius": radius})
            
        response = requests.get(
            f"{self.BASE_URL}/place/textsearch/json",
            params=params,
            timeout=DEFAULT_TIMEOUT
        )
        
        return self._process_response(response)
        
    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """Process API response with error handling"""
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "OK":
            logger.info(f"Found {len(result.get('results', []))} places")
        else:
            logger.warning(f"API returned status: {result.get('status')}")
            
        return result

    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific place"""
        try:
            logger.info(f"Getting details for place_id: {place_id}")
            endpoint = f"{self.BASE_URL}/place/details/json"
            params = {
                "place_id": place_id,
                "key": self.api_key
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Successfully retrieved details for place_id: {place_id}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting place details: {str(e)}")
            raise

    def geocode(self, address: str) -> Dict[str, Any]:
        """Поиск координат по адресу"""
        try:
            logger.info(f"Geocoding address: {address}")
            endpoint = f"{self.BASE_URL}/geocode/json"
            params = {
                "address": address,
                "key": self.api_key
            }
            
            response = requests.get(endpoint, params=params, timeout=DEFAULT_TIMEOUT)
            result = response.json()
            
            logger.info(f"Geocoding status: {result.get('status')}")
            return result
            
        except Exception as e:
            logger.error(f"Geocoding error: {str(e)}")
            raise

def validate_api_key(api_key: str) -> bool:
    """Расширенная проверка валидности API ключа"""
    try:
        test_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
            "fields": "name",  # Минимальный набор полей
            "key": api_key
        }
        response = requests.get(test_endpoint, params=params)
        result = response.json()
        
        if response.status_code != 200:
            logger.error(f"HTTP error: {response.status_code}")
            return False
            
        if result.get("status") != "OK":
            logger.error(f"API error: {result.get('status')} - {result.get('error_message', 'Unknown error')}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Exception during API key validation: {str(e)}")
        return False

def main():
    try:
        load_dotenv()
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        
        if not api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in .env")
            
        if not validate_api_key(api_key):
            raise ValueError("Invalid API key")
            
        maps_api = GoogleMapsAPI(api_key)
        results = maps_api.search_places("restaurants in London")
        
        if results.get("status") == "OK":
            os.makedirs("data/raw", exist_ok=True)
            with open("data/raw/test_search.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        # Тестовый запрос геокодирования
        result = maps_api.geocode("London")
        
        if result.get("status") == "OK":
            os.makedirs("data/raw", exist_ok=True)
            with open("data/raw/geocoding_test.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info("Geocoding results saved")
        else:
            logger.error(f"Geocoding failed: {result.get('status')}")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()