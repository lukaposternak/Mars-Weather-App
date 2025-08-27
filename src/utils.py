
"""
Data Models and Utilities for Mars Weather App
Contains data classes and utility functions
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class TemperatureData:
    """Temperature data for Mars weather"""
    min_temp: float
    max_temp: float
    avg_temp: float
    
    def to_fahrenheit(self):
        """Convert Celsius to Fahrenheit"""
        return TemperatureData(
            min_temp=self.min_temp * 9/5 + 32,
            max_temp=self.max_temp * 9/5 + 32,
            avg_temp=self.avg_temp * 9/5 + 32
        )
    
    def format_temp(self, unit: str = "Celsius") -> Dict[str, str]:
        """Format temperature values with proper units"""
        if unit.lower() == "fahrenheit":
            temp_data = self.to_fahrenheit()
            unit_symbol = "°F"
        else:
            temp_data = self
            unit_symbol = "°C"
        
        return {
            'min': f"{temp_data.min_temp:.1f}{unit_symbol}",
            'max': f"{temp_data.max_temp:.1f}{unit_symbol}",
            'avg': f"{temp_data.avg_temp:.1f}{unit_symbol}"
        }

@dataclass
class PressureData:
    """Atmospheric pressure data for Mars weather"""
    pressure: float  # Average pressure
    min_pressure: Optional[float] = None
    max_pressure: Optional[float] = None
    
    def format_pressure(self) -> Dict[str, str]:
        """Format pressure values with proper units"""
        result = {'avg': f"{self.pressure:.0f} Pa"}
        
        if self.min_pressure is not None:
            result['min'] = f"{self.min_pressure:.0f} Pa"
        if self.max_pressure is not None:
            result['max'] = f"{self.max_pressure:.0f} Pa"
            
        return result

@dataclass
class WindData:
    """Wind data for Mars weather"""
    wind_speed: float  # m/s
    wind_direction: Optional[str] = None
    
    def format_wind(self) -> Dict[str, str]:
        """Format wind data with proper units"""
        return {
            'speed': f"{self.wind_speed:.1f} m/s",
            'direction': self.wind_direction or "Unknown"
        }
    
    def get_wind_direction_degrees(self) -> Optional[float]:
        """Convert compass direction to degrees"""
        direction_map = {
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
            'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
            'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
            'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }
        return direction_map.get(self.wind_direction)

@dataclass
class MarsWeatherData:
    """Complete Mars weather data"""
    sol: int  # Mars sol (day)
    terrestrial_date: str
    season: str
    temperature: TemperatureData
    pressure: PressureData
    wind: WindData
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarsWeatherData':
        """Create instance from dictionary"""
        return cls(
            sol=data['sol'],
            terrestrial_date=data['terrestrial_date'],
            season=data['season'],
            temperature=TemperatureData(**data['temperature']),
            pressure=PressureData(**data['pressure']),
            wind=WindData(**data['wind'])
        )
    
    def get_summary(self, temp_unit: str = "Celsius") -> str:
        """Get a human-readable summary of the weather"""
        temp = self.temperature.format_temp(temp_unit)
        pressure = self.pressure.format_pressure()
        wind = self.wind.format_wind()
        
        return (f"Sol {self.sol} ({self.terrestrial_date})\n"
                f"Season: {self.season}\n"
                f"Temperature: {temp['min']} to {temp['max']} (avg {temp['avg']})\n"
                f"Pressure: {pressure['avg']}\n"
                f"Wind: {wind['speed']} from {wind['direction']}")

def get_config_path() -> str:
    """Get the path to the configuration file"""
    # Create config directory in user's home folder
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".mars_weather")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    return os.path.join(config_dir, "config.json")

def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    config_path = get_config_path()
    
    default_config = {
        'api_key': 'DEMO_KEY',
        'temperature_unit': 'Celsius',
        'auto_refresh': True,
        'refresh_interval': 300,  # 5 minutes
        'notifications_enabled': True
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**default_config, **config}
    except Exception as e:
        print(f"Error loading config: {e}")
    
    return default_config

def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file"""
    try:
        config_path = get_config_path()
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_cache_path() -> str:
    """Get the path to the cache directory"""
    home_dir = os.path.expanduser("~")
    cache_dir = os.path.join(home_dir, ".mars_weather", "cache")
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    return cache_dir

def cache_weather_data(data: MarsWeatherData) -> bool:
    """Cache weather data to file"""
    try:
        cache_path = os.path.join(get_cache_path(), f"weather_sol_{data.sol}.json")
        with open(cache_path, 'w') as f:
            json.dump(data.to_dict(), f, indent=2)
        return True
    except Exception as e:
        print(f"Error caching data: {e}")
        return False

def load_cached_weather_data(sol: int) -> Optional[MarsWeatherData]:
    """Load cached weather data for a specific sol"""
    try:
        cache_path = os.path.join(get_cache_path(), f"weather_sol_{sol}.json")
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                data = json.load(f)
                return MarsWeatherData.from_dict(data)
    except Exception as e:
        print(f"Error loading cached data: {e}")
    
    return None

def format_sol_date(sol: int, terrestrial_date: str) -> str:
    """Format sol and terrestrial date for display"""
    return f"Sol {sol:,} • {terrestrial_date}"

def get_season_emoji(season: str) -> str:
    """Get emoji representation of Mars season"""
    season_emojis = {
        'Spring': '🌱',
        'Summer': '☀️',
        'Autumn': '🍂',
        'Winter': '❄️',
        'Unknown': '🌍'
    }
    return season_emojis.get(season, '🌍')

def validate_temperature_unit(unit: str) -> str:
    """Validate and normalize temperature unit"""
    unit = unit.lower()
    if unit in ['celsius', 'c']:
        return 'Celsius'
    elif unit in ['fahrenheit', 'f']:
        return 'Fahrenheit'
    else:
        return 'Celsius'  # Default
