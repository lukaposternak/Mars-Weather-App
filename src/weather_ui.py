
"""
User Interface Components for Mars Weather App
Implements the main UI layout and custom widgets
"""

import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime
from utils import MarsWeatherData, get_season_emoji

class MarsWeatherUI:
    """Main UI class for Mars Weather application"""
    
    def __init__(self, root, refresh_callback, settings_callback):
        self.root = root
        self.refresh_callback = refresh_callback
        self.settings_callback = settings_callback
        
        # Color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_accent': '#0f3460',
            'text_primary': '#ffffff',
            'text_secondary': '#b4b4b8',
            'accent': '#e94560',
            'success': '#00d4aa',
            'warning': '#ffae00',
            'mars_red': '#cd5c5c'
        }
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles for consistent theming"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_primary'],
                       font=('Helvetica', 16, 'bold'))
        
        style.configure('Header.TLabel', 
                       background=self.colors['bg_secondary'], 
                       foreground=self.colors['text_primary'],
                       font=('Helvetica', 12, 'bold'))
        
        style.configure('Data.TLabel', 
                       background=self.colors['bg_secondary'], 
                       foreground=self.colors['text_secondary'],
                       font=('Helvetica', 10))
        
        style.configure('Large.TLabel', 
                       background=self.colors['bg_secondary'], 
                       foreground=self.colors['accent'],
                       font=('Helvetica', 14, 'bold'))
    
    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header section
        self.create_header()
        
        # Main content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill='both', expand=True, pady=10)
        
        # Create weather display sections
        self.create_current_weather_section()
        self.create_details_section()
        
        # Status bar
        self.create_status_bar()
        
        # Loading overlay (initially hidden)
        self.create_loading_overlay()
    
    def create_header(self):
        """Create application header with title and controls"""
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_secondary'], relief='raised', bd=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Title and Mars emoji
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        title_frame.pack(side='left', padx=10, pady=10)
        
        title_label = tk.Label(title_frame, text="🔴 Mars Weather Monitor", 
                              bg=self.colors['bg_secondary'], 
                              fg=self.colors['text_primary'],
                              font=('Helvetica', 18, 'bold'))
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Historical Mars weather data from NASA's InSight mission (2018-2022)", 
                                 bg=self.colors['bg_secondary'], 
                                 fg=self.colors['text_secondary'],
                                 font=('Helvetica', 10))
        subtitle_label.pack()
        
        # Control buttons
        controls_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        controls_frame.pack(side='right', padx=10, pady=10)
        
        self.refresh_btn = tk.Button(controls_frame, text="🔄 Refresh", 
                                    command=self.refresh_callback,
                                    bg=self.colors['accent'], fg='white',
                                    font=('Helvetica', 10, 'bold'),
                                    relief='flat', padx=15, pady=5)
        self.refresh_btn.pack(side='right', padx=5)
        
        settings_btn = tk.Button(controls_frame, text="⚙️ Settings", 
                                command=self.settings_callback,
                                bg=self.colors['bg_accent'], fg='white',
                                font=('Helvetica', 10),
                                relief='flat', padx=15, pady=5)
        settings_btn.pack(side='right', padx=5)
    
    def create_current_weather_section(self):
        """Create the main weather display section"""
        # Current weather container
        weather_frame = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'], relief='raised', bd=1)
        weather_frame.pack(fill='x', pady=(0, 10))
        
        # Header
        header = tk.Label(weather_frame, text="Current Mars Weather", 
                         bg=self.colors['bg_secondary'], 
                         fg=self.colors['text_primary'],
                         font=('Helvetica', 14, 'bold'))
        header.pack(pady=10)
        
        # Main weather display
        main_weather_frame = tk.Frame(weather_frame, bg=self.colors['bg_secondary'])
        main_weather_frame.pack(fill='x', padx=20, pady=10)
        
        # Left side - Sol and Date info
        self.info_frame = tk.Frame(main_weather_frame, bg=self.colors['bg_secondary'])
        self.info_frame.pack(side='left', fill='both', expand=True)
        
        self.sol_label = tk.Label(self.info_frame, text="Sol: --", 
                                 bg=self.colors['bg_secondary'], 
                                 fg=self.colors['text_primary'],
                                 font=('Helvetica', 12, 'bold'))
        self.sol_label.pack(anchor='w')
        
        self.date_label = tk.Label(self.info_frame, text="Date: --", 
                                  bg=self.colors['bg_secondary'], 
                                  fg=self.colors['text_secondary'],
                                  font=('Helvetica', 10))
        self.date_label.pack(anchor='w')
        
        self.season_label = tk.Label(self.info_frame, text="Season: --", 
                                    bg=self.colors['bg_secondary'], 
                                    fg=self.colors['text_secondary'],
                                    font=('Helvetica', 10))
        self.season_label.pack(anchor='w', pady=(5, 0))
        
        # Right side - Temperature display
        temp_frame = tk.Frame(main_weather_frame, bg=self.colors['bg_secondary'])
        temp_frame.pack(side='right')
        
        temp_label = tk.Label(temp_frame, text="Temperature", 
                             bg=self.colors['bg_secondary'], 
                             fg=self.colors['text_primary'],
                             font=('Helvetica', 10, 'bold'))
        temp_label.pack()
        
        self.temp_display = tk.Label(temp_frame, text="--°C", 
                                    bg=self.colors['bg_secondary'], 
                                    fg=self.colors['mars_red'],
                                    font=('Helvetica', 24, 'bold'))
        self.temp_display.pack()
        
        self.temp_range = tk.Label(temp_frame, text="-- to --", 
                                  bg=self.colors['bg_secondary'], 
                                  fg=self.colors['text_secondary'],
                                  font=('Helvetica', 9))
        self.temp_range.pack()
    
    def create_details_section(self):
        """Create detailed weather metrics section"""
        details_frame = tk.Frame(self.content_frame, bg=self.colors['bg_secondary'], relief='raised', bd=1)
        details_frame.pack(fill='both', expand=True)
        
        # Header
        header = tk.Label(details_frame, text="Detailed Measurements", 
                         bg=self.colors['bg_secondary'], 
                         fg=self.colors['text_primary'],
                         font=('Helvetica', 12, 'bold'))
        header.pack(pady=10)
        
        # Metrics grid
        metrics_frame = tk.Frame(details_frame, bg=self.colors['bg_secondary'])
        metrics_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pressure section
        pressure_frame = tk.Frame(metrics_frame, bg=self.colors['bg_accent'], relief='raised', bd=1)
        pressure_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        tk.Label(pressure_frame, text="Atmospheric Pressure", 
                bg=self.colors['bg_accent'], fg=self.colors['text_primary'],
                font=('Helvetica', 10, 'bold')).pack(pady=5)
        
        self.pressure_display = tk.Label(pressure_frame, text="-- Pa", 
                                        bg=self.colors['bg_accent'], 
                                        fg=self.colors['success'],
                                        font=('Helvetica', 16, 'bold'))
        self.pressure_display.pack(pady=5)
        
        self.pressure_range = tk.Label(pressure_frame, text="Range: -- to --", 
                                      bg=self.colors['bg_accent'], 
                                      fg=self.colors['text_secondary'],
                                      font=('Helvetica', 8))
        self.pressure_range.pack(pady=(0, 10))
        
        # Wind section
        wind_frame = tk.Frame(metrics_frame, bg=self.colors['bg_accent'], relief='raised', bd=1)
        wind_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        tk.Label(wind_frame, text="Wind Conditions", 
                bg=self.colors['bg_accent'], fg=self.colors['text_primary'],
                font=('Helvetica', 10, 'bold')).pack(pady=5)
        
        # Wind compass
        self.wind_canvas = tk.Canvas(wind_frame, width=100, height=100, 
                                    bg=self.colors['bg_accent'], highlightthickness=0)
        self.wind_canvas.pack(pady=5)
        
        self.wind_speed_display = tk.Label(wind_frame, text="-- m/s", 
                                          bg=self.colors['bg_accent'], 
                                          fg=self.colors['warning'],
                                          font=('Helvetica', 12, 'bold'))
        self.wind_speed_display.pack()
        
        self.wind_dir_display = tk.Label(wind_frame, text="Direction: --", 
                                        bg=self.colors['bg_accent'], 
                                        fg=self.colors['text_secondary'],
                                        font=('Helvetica', 8))
        self.wind_dir_display.pack(pady=(0, 10))
    
    def create_status_bar(self):
        """Create status bar at bottom of window"""
        self.status_bar = tk.Label(self.main_frame, text="Ready", 
                                  bg=self.colors['bg_accent'], 
                                  fg=self.colors['text_secondary'],
                                  font=('Helvetica', 9),
                                  anchor='w', relief='sunken', bd=1)
        self.status_bar.pack(fill='x', side='bottom')
    
    def create_loading_overlay(self):
        """Create loading overlay (initially hidden)"""
        self.loading_frame = tk.Frame(self.root, bg='black')
        self.loading_label = tk.Label(self.loading_frame, text="🛰️ Connecting to Mars...", 
                                     bg='black', fg='white',
                                     font=('Helvetica', 14, 'bold'))
        self.loading_label.pack(expand=True)
    
    def show_loading(self, show: bool):
        """Show or hide loading overlay"""
        if show:
            self.loading_frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.refresh_btn.config(state='disabled', text="🔄 Loading...")
        else:
            self.loading_frame.place_forget()
            self.refresh_btn.config(state='normal', text="🔄 Refresh")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_bar.config(text=message)
    
    def update_weather_display(self, weather_data: MarsWeatherData, temp_unit: str = "Celsius"):
        """Update all weather displays with new data"""
        # Update sol and date info
        self.sol_label.config(text=f"Sol {weather_data.sol:,}")
        self.date_label.config(text=f"Earth Date: {weather_data.terrestrial_date}")
        
        season_emoji = get_season_emoji(weather_data.season)
        self.season_label.config(text=f"Season: {season_emoji} {weather_data.season}")
        
        # Update temperature display
        temp_formatted = weather_data.temperature.format_temp(temp_unit)
        self.temp_display.config(text=temp_formatted['avg'])
        self.temp_range.config(text=f"{temp_formatted['min']} to {temp_formatted['max']}")
        
        # Update pressure display
        pressure_formatted = weather_data.pressure.format_pressure()
        self.pressure_display.config(text=pressure_formatted['avg'])
        
        if 'min' in pressure_formatted and 'max' in pressure_formatted:
            self.pressure_range.config(text=f"Range: {pressure_formatted['min']} to {pressure_formatted['max']}")
        else:
            self.pressure_range.config(text="Range: Not available")
        
        # Update wind display
        wind_formatted = weather_data.wind.format_wind()
        self.wind_speed_display.config(text=wind_formatted['speed'])
        self.wind_dir_display.config(text=f"Direction: {wind_formatted['direction']}")
        
        # Update wind compass
        self.draw_wind_compass(weather_data.wind.wind_direction, weather_data.wind.wind_speed)
    
    def draw_wind_compass(self, direction: str, speed: float):
        """Draw wind direction compass"""
        self.wind_canvas.delete("all")
        
        # Draw compass circle
        cx, cy = 50, 50  # Center
        radius = 40
        
        # Draw outer circle
        self.wind_canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, 
                                   outline=self.colors['text_secondary'], width=2)
        
        # Draw cardinal direction labels
        directions = ['N', 'E', 'S', 'W']
        positions = [(cx, cy-radius-10), (cx+radius+10, cy), (cx, cy+radius+10), (cx-radius-10, cy)]
        
        for i, (dir_label, (x, y)) in enumerate(zip(directions, positions)):
            self.wind_canvas.create_text(x, y, text=dir_label, 
                                       fill=self.colors['text_secondary'], 
                                       font=('Helvetica', 8, 'bold'))
        
        # Draw wind direction arrow if direction is known
        if direction and direction != "Unknown":
            degrees = self.get_direction_degrees(direction)
            if degrees is not None:
                # Convert to radians and adjust for canvas coordinates
                radians = math.radians(degrees - 90)  # -90 to start from top
                
                # Calculate arrow end point
                arrow_length = min(radius - 5, max(10, speed * 3))  # Scale with wind speed
                end_x = cx + arrow_length * math.cos(radians)
                end_y = cy + arrow_length * math.sin(radians)
                
                # Draw arrow
                self.wind_canvas.create_line(cx, cy, end_x, end_y, 
                                           fill=self.colors['warning'], width=3, 
                                           arrow=tk.LAST, arrowshape=(8, 10, 3))
        
        # Draw center point
        self.wind_canvas.create_oval(cx-3, cy-3, cx+3, cy+3, 
                                   fill=self.colors['mars_red'], outline='')
    
    def get_direction_degrees(self, direction: str) -> float:
        """Convert compass direction to degrees"""
        direction_map = {
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
            'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
            'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
            'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }
        return direction_map.get(direction, 0)
