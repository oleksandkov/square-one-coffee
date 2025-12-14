"""
Comprehensive Cafe Fetcher for Edmonton, Alberta
Uses Google Places API with grid-based search to ensure complete coverage
"""

import os
import requests
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
import json
from typing import List, Dict, Set
import math

# Load environment variables
load_dotenv()
PLACES_API_KEY = os.getenv('PLACES_API_KEY')

# Edmonton boundaries (approximate)
EDMONTON_BOUNDS = {
    'north': 53.7,
    'south': 53.4,
    'east': -113.3,
    'west': -113.7
}

# Search configuration
GRID_SIZE = 0.05  # degrees (~5km grid cells)
SEARCH_RADIUS = 3500  # meters (to ensure overlap between grid cells)
SEARCH_TYPES = ['cafe', 'coffee_shop', 'bakery']
SEARCH_KEYWORDS = ['cafe', 'coffee', 'espresso', 'latte', 'tea house', 'bubble tea', 'boba']

class EdmontonCafeFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.found_places: Dict[str, Dict] = {}  # place_id -> place data
        self.search_count = 0
        self.api_calls = 0
        
    def generate_search_grid(self) -> List[Dict[str, float]]:
        """Generate grid of search points covering Edmonton"""
        points = []
        
        lat = EDMONTON_BOUNDS['south']
        while lat <= EDMONTON_BOUNDS['north']:
            lng = EDMONTON_BOUNDS['west']
            while lng <= EDMONTON_BOUNDS['east']:
                points.append({'lat': lat, 'lng': lng})
                lng += GRID_SIZE
            lat += GRID_SIZE
        
        print(f"Generated {len(points)} grid points to search")
        return points
    
    def search_nearby(self, location: Dict[str, float], search_type: str = None, keyword: str = None) -> List[Dict]:
        """Search for places near a specific location"""
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f"{location['lat']},{location['lng']}",
            'radius': SEARCH_RADIUS,
            'key': self.api_key
        }
        
        if search_type:
            params['type'] = search_type
        if keyword:
            params['keyword'] = keyword
            
        all_results = []
        
        while True:
            self.api_calls += 1
            print(f"  API Call #{self.api_calls}: {search_type or 'general'} / {keyword or 'no keyword'}")
            
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'ZERO_RESULTS':
                    break
                    
                if data.get('status') not in ['OK', 'ZERO_RESULTS']:
                    print(f"    Warning: API returned status {data.get('status')}")
                    if data.get('status') == 'OVER_QUERY_LIMIT':
                        print("    Hit API quota limit. Waiting 60 seconds...")
                        time.sleep(60)
                        continue
                    break
                
                results = data.get('results', [])
                all_results.extend(results)
                print(f"    Found {len(results)} results")
                
                # Check for next page
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                    
                # Wait before fetching next page (required by Google)
                time.sleep(2)
                params = {'pagetoken': next_page_token, 'key': self.api_key}
                
            except requests.exceptions.RequestException as e:
                print(f"    Error: {e}")
                break
        
        return all_results
    
    def get_place_details(self, place_id: str) -> Dict:
        """Get detailed information about a place"""
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,geometry,place_id,business_status,types,rating,user_ratings_total,opening_hours,formatted_phone_number,website,price_level,editorial_summary',
            'key': self.api_key
        }
        
        self.api_calls += 1
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
            else:
                print(f"    Details fetch failed for {place_id}: {data.get('status')}")
                return {}
                
        except requests.exceptions.RequestException as e:
            print(f"    Error fetching details: {e}")
            return {}
    
    def is_in_edmonton_area(self, lat: float, lng: float) -> bool:
        """Check if coordinates are within Edmonton area (with margin)"""
        margin = 0.1  # Allow some margin beyond strict boundaries
        return (EDMONTON_BOUNDS['south'] - margin <= lat <= EDMONTON_BOUNDS['north'] + margin and
                EDMONTON_BOUNDS['west'] - margin <= lng <= EDMONTON_BOUNDS['east'] + margin)
    
    def is_likely_cafe(self, place: Dict) -> bool:
        """Determine if a place is likely a cafe/coffee shop"""
        types = place.get('types', [])
        name = place.get('name', '').lower()
        
        # Type-based filtering
        cafe_types = ['cafe', 'coffee_shop', 'bakery', 'restaurant', 'food', 'bar']
        has_cafe_type = any(t in types for t in cafe_types)
        
        # Name-based filtering
        cafe_keywords = ['cafe', 'coffee', 'espresso', 'latte', 'cappuccino', 'tea', 'boba', 'bubble', 
                         'bakery', 'patisserie', 'bistro', 'beans', 'brew', 'roast', 'starbucks', 
                         'tim hortons', 'second cup', 'good earth', 'blenz']
        has_cafe_keyword = any(kw in name for kw in cafe_keywords)
        
        # Exclude clearly non-cafe places
        exclude_keywords = ['gas station', 'convenience store', 'hotel', 'hospital', 'school', 
                           'university', 'library', 'gym', 'bank', 'car wash']
        is_excluded = any(kw in name for kw in exclude_keywords)
        
        return (has_cafe_type or has_cafe_keyword) and not is_excluded
    
    def process_place(self, place: Dict) -> None:
        """Process and store a place if it's valid and in Edmonton"""
        place_id = place.get('place_id')
        if not place_id:
            return
        
        # Skip if already processed
        if place_id in self.found_places:
            return
        
        # Check location
        geometry = place.get('geometry', {})
        location = geometry.get('location', {})
        lat = location.get('lat')
        lng = location.get('lng')
        
        if not lat or not lng:
            return
            
        if not self.is_in_edmonton_area(lat, lng):
            return
        
        # Check if it's likely a cafe
        if not self.is_likely_cafe(place):
            return
        
        # Store basic info first
        self.found_places[place_id] = {
            'place_id': place_id,
            'name': place.get('name'),
            'address': place.get('vicinity') or place.get('formatted_address'),
            'lat': lat,
            'lng': lng,
            'types': ', '.join(place.get('types', [])),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            'business_status': place.get('business_status'),
            'price_level': place.get('price_level')
        }
        
        print(f"    ✓ Added: {place.get('name')}")
    
    def enrich_with_details(self) -> None:
        """Fetch detailed information for all found places"""
        print(f"\nEnriching {len(self.found_places)} places with detailed information...")
        
        for i, (place_id, place_data) in enumerate(self.found_places.items(), 1):
            print(f"  [{i}/{len(self.found_places)}] {place_data['name']}")
            
            details = self.get_place_details(place_id)
            if details:
                # Update with detailed info
                place_data['formatted_address'] = details.get('formatted_address', place_data['address'])
                place_data['phone'] = details.get('formatted_phone_number', '')
                place_data['website'] = details.get('website', '')
                
                # Opening hours
                opening_hours = details.get('opening_hours', {})
                place_data['hours'] = '; '.join(opening_hours.get('weekday_text', []))
                place_data['is_open_now'] = opening_hours.get('open_now', None)
                
                # Editorial summary
                editorial = details.get('editorial_summary', {})
                place_data['description'] = editorial.get('overview', '')
            
            # Rate limiting
            if i % 10 == 0:
                time.sleep(1)
    
    def search_all(self) -> pd.DataFrame:
        """Execute comprehensive search"""
        print("=" * 80)
        print("COMPREHENSIVE EDMONTON CAFE SEARCH")
        print("=" * 80)
        
        # Generate search grid
        grid_points = self.generate_search_grid()
        
        # Search each grid point with different types and keywords
        total_searches = len(grid_points) * (len(SEARCH_TYPES) + len(SEARCH_KEYWORDS))
        current = 0
        
        print(f"\nExecuting {total_searches} searches across {len(grid_points)} grid points...")
        print("This will take a while to ensure comprehensive coverage.\n")
        
        for i, point in enumerate(grid_points, 1):
            print(f"\nGrid Point {i}/{len(grid_points)}: ({point['lat']:.4f}, {point['lng']:.4f})")
            
            # Search by type
            for search_type in SEARCH_TYPES:
                current += 1
                print(f"  Search {current}/{total_searches}: type={search_type}")
                results = self.search_nearby(point, search_type=search_type)
                for place in results:
                    self.process_place(place)
                time.sleep(0.5)  # Rate limiting
            
            # Search by keyword
            for keyword in SEARCH_KEYWORDS:
                current += 1
                print(f"  Search {current}/{total_searches}: keyword={keyword}")
                results = self.search_nearby(point, keyword=keyword)
                for place in results:
                    self.process_place(place)
                time.sleep(0.5)  # Rate limiting
            
            print(f"  Total unique cafes found so far: {len(self.found_places)}")
        
        # Enrich with details
        self.enrich_with_details()
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(self.found_places, orient='index')
        
        # Sort by name
        df = df.sort_values('name')
        
        return df
    
    def save_results(self, df: pd.DataFrame, filename: str = None) -> None:
        """Save results to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data-private/derived/cafes/edmonton_cafes_comprehensive_{timestamp}.csv'
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n{'=' * 80}")
        print(f"Results saved to: {filename}")
        print(f"Total cafes found: {len(df)}")
        print(f"Total API calls made: {self.api_calls}")
        print(f"{'=' * 80}")


def main():
    if not PLACES_API_KEY:
        print("Error: PLACES_API_KEY not found in .env file")
        return
    
    print(f"Using Google Places API Key: {PLACES_API_KEY[:10]}...")
    
    fetcher = EdmontonCafeFetcher(PLACES_API_KEY)
    
    try:
        # Execute comprehensive search
        df = fetcher.search_all()
        
        # Save to default location
        fetcher.save_results(df)
        
        # Also save to the main file
        main_file = 'data-private/derived/cafes/edmonton_cafes_comprehensive.csv'
        fetcher.save_results(df, main_file)
        
        # Print summary statistics
        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)
        print(f"Total cafes: {len(df)}")
        print(f"With ratings: {df['rating'].notna().sum()}")
        print(f"Average rating: {df['rating'].mean():.2f}")
        print(f"With phone: {df['phone'].notna().sum()}")
        print(f"With website: {df['website'].notna().sum()}")
        print(f"Operational: {(df['business_status'] == 'OPERATIONAL').sum()}")
        print(f"Temporarily closed: {(df['business_status'] == 'CLOSED_TEMPORARILY').sum()}")
        print(f"Permanently closed: {(df['business_status'] == 'CLOSED_PERMANENTLY').sum()}")
        
        print("\nTop 10 highest rated cafes:")
        top_rated = df[df['user_ratings_total'] >= 20].nlargest(10, 'rating')
        for _, row in top_rated.iterrows():
            print(f"  {row['name']}: {row['rating']} ⭐ ({row['user_ratings_total']} reviews)")
        
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.")
        if fetcher.found_places:
            print(f"Saving {len(fetcher.found_places)} cafes found so far...")
            df = pd.DataFrame.from_dict(fetcher.found_places, orient='index')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data-private/derived/cafes/edmonton_cafes_partial_{timestamp}.csv'
            fetcher.save_results(df, filename)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
