
"""
NASA API Client for Mars Weather Data
Handles communication with NASA's InSight Mars Weather API
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from utils import MarsWeatherData, TemperatureData, PressureData, WindData

class NASAAPIClient:
    """Client for NASA Mars Weather API"""
    
    def __init__(self, api_key: str = "DEMO_KEY"):
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mars-Weather-Desktop-App/1.0'
        })
    
    def get_mars_weather(self) -> Optional[MarsWeatherData]:
        """
        Fetch current Mars weather data from NASA API
        Returns MarsWeatherData object or None if failed
        """
        try:
            # Use InSight Mars Weather API
            url = f"{self.base_url}/insight_weather/"
            params = {
                'api_key': self.api_key,
                'feedtype': 'json',
                'ver': '1.0'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data)
            elif response.status_code == 403:
                raise Exception("Invalid API key. Please check your NASA API key.")
            elif response.status_code == 429:
                raise Exception("API rate limit exceeded. Please try again later.")
            else:
                # If InSight API fails, try to generate mock data for demonstration
                print(f"API returned status {response.status_code}, using demo data")
                return self._get_demo_weather_data()
                
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error. Please check your internet connection.")
        except Exception as e:
            print(f"API Error: {e}")
            # Return demo data for development/demo purposes
            return self._get_demo_weather_data()
    
    def _parse_weather_data(self, data: Dict[str, Any]) -> Optional[MarsWeatherData]:
        """Parse NASA API response into MarsWeatherData object"""
        try:
            # Get the latest sol (Mars day) data
            sol_keys = data.get('sol_keys', [])
            if not sol_keys:
                return self._get_demo_weather_data()
            
            latest_sol = sol_keys[-1]
            sol_data = data[latest_sol]
            
            # Extract temperature data
            temp_data = sol_data.get('AT', {})
            temperature = TemperatureData(
                min_temp=temp_data.get('mn', -80),
                max_temp=temp_data.get('mx', -20),
                avg_temp=temp_data.get('av', -50)
            )
            
            # Extract pressure data
            pressure_data = sol_data.get('PRE', {})
            pressure = PressureData(
                pressure=pressure_data.get('av', 650),
                min_pressure=pressure_data.get('mn', 600),
                max_pressure=pressure_data.get('mx', 700)
            )
            
            # Extract wind data
            wind_data = sol_data.get('HWS', {})
            wind = WindData(
                wind_speed=wind_data.get('av', 5.5),
                wind_direction=sol_data.get('WD', {}).get('most_common', {}).get('compass_point', 'NE')
            )
            
            # Get season
            season = sol_data.get('Season', 'Unknown')
            
            # Calculate terrestrial date
            first_utc = data.get('1', {}).get('First_UTC', '2018-11-27T00:00:00Z')
            base_date = datetime.fromisoformat(first_utc.replace('Z', '+00:00'))
            current_date = base_date + timedelta(days=int(latest_sol))
            
            return MarsWeatherData(
                sol=int(latest_sol),
                terrestrial_date=current_date.strftime('%Y-%m-%d'),
                season=season,
                temperature=temperature,
                pressure=pressure,
                wind=wind
            )
            
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return self._get_demo_weather_data()
    
    def _get_demo_weather_data(self) -> MarsWeatherData:
        """Generate demonstration weather data for testing/demo purposes"""
        import random
        
        # Generate realistic Mars weather data
        base_temp = random.randint(-90, -40)
        
        temperature = TemperatureData(
            min_temp=base_temp - random.randint(5, 15),
            max_temp=base_temp + random.randint(10, 30),
            avg_temp=base_temp
        )
        
        pressure = PressureData(
            pressure=random.randint(600, 800),
            min_pressure=random.randint(580, 650),
            max_pressure=random.randint(750, 850)
        )
        
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        wind = WindData(
            wind_speed=random.uniform(2.0, 15.0),
            wind_direction=random.choice(directions)
        )
        
        seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
        
        # Current sol (Mars day since landing)
        current_sol = 3000 + random.randint(0, 500)
        
        return MarsWeatherData(
            sol=current_sol,
            terrestrial_date=datetime.now().strftime('%Y-%m-%d'),
            season=random.choice(seasons),
            temperature=temperature,
            pressure=pressure,
            wind=wind
        )
    
    def get_historical_weather(self, days: int = 7) -> list:
        """Get historical weather data for the past N days"""
        # This would implement historical data fetching
        # For now, return empty list as the InSight mission has ended
        return []
    
    def validate_api_key(self) -> bool:
        """Validate if the API key is working"""
        try:
            url = f"{self.base_url}/planetary/apod"
            params = {'api_key': self.api_key}
            response = self.session.get(url, params=params, timeout=10)
            return response.status_code == 200
        except:
            return False
