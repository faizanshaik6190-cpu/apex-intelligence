import googlemaps
from typing import List, Dict, Any
from app.config import settings

class GoogleMapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.google_maps_api_key)
    
    def find_businesses(self, city: str, keyword: str, radius: int = 50000) -> List[Dict[str, Any]]:
        """
        Find businesses on Google Maps by city and keyword.
        Returns a list of businesses with details.
        """
        try:
            places_result = self.client.places_nearby(
                location=self.get_city_coordinates(city),
                radius=radius,
                keyword=keyword,
                type='establishment'
            )
            
            businesses = []
            for place in places_result.get('results', []):
                business = self.extract_business_info(place)
                businesses.append(business)
            
            return businesses
        except Exception as e:
            print(f"Error finding businesses: {e}")
            return []
    
    def get_city_coordinates(self, city: str) -> tuple:
        """
        Get latitude and longitude for a city.
        """
        try:
            geocode_result = self.client.geocode(address=city)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return (location['lat'], location['lng'])
        except Exception as e:
            print(f"Error geocoding city: {e}")
        return (0, 0)
    
    def extract_business_info(self, place: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant business information from Google Maps place object.
        """
        return {
            'business_name': place.get('name', ''),
            'address': place.get('vicinity', ''),
            'rating': place.get('rating', 0.0),
            'review_count': place.get('user_ratings_total', 0),
            'phone': place.get('formatted_phone_number', ''),
            'website': place.get('website', ''),
            'types': place.get('types', []),
            'google_maps_url': place.get('url', ''),
            'place_id': place.get('place_id', ''),
            'open_now': place.get('opening_hours', {}).get('open_now', None)
        }
    
    def get_business_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific business.
        """
        try:
            details = self.client.place(place_id=place_id)
            return self.extract_business_info(details.get('result', {}))
        except Exception as e:
            print(f"Error getting business details: {e}")
            return {}
