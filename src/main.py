
"""
Mars Weather Desktop App - Main Entry Point
A desktop application that displays current Mars weather data from NASA's API
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
from datetime import datetime
from api_client import NASAAPIClient
from weather_ui import MarsWeatherUI
from utils import MarsWeatherData, save_config, load_config

class MarsWeatherApp:
    """Main application class that coordinates the Mars Weather Desktop App"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mars Weather Monitor")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap('assets/icons/mars.ico')
        except:
            pass
        
        # Load configuration
        self.config = load_config()
        
        # Initialize API client
        api_key = self.config.get('api_key', 'DEMO_KEY')
        self.api_client = NASAAPIClient(api_key)
        
        # Initialize UI
        self.ui = MarsWeatherUI(self.root, self.on_refresh_clicked, self.on_settings_clicked)
        
        # Current weather data
        self.current_weather = None
        
        # Start with initial data fetch
        self.refresh_weather_data()
    
    def on_refresh_clicked(self):
        """Handle refresh button click"""
        self.refresh_weather_data()
    
    def on_settings_clicked(self):
        """Handle settings button click"""
        self.show_settings_dialog()
    
    def refresh_weather_data(self):
        """Fetch new weather data from NASA API in a background thread"""
        self.ui.show_loading(True)
        self.ui.update_status("Fetching Mars weather data...")
        
        # Run API call in background thread to prevent UI freezing
        thread = threading.Thread(target=self._fetch_weather_data)
        thread.daemon = True
        thread.start()
    
    def _fetch_weather_data(self):
        """Background thread function to fetch weather data"""
        try:
            weather_data = self.api_client.get_mars_weather()
            
            if weather_data:
                # Update UI in main thread
                self.root.after(0, self._update_ui_with_weather, weather_data)
            else:
                self.root.after(0, self._show_error, "No weather data available")
                
        except Exception as e:
            error_msg = f"Failed to fetch weather data: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
    
    def _update_ui_with_weather(self, weather_data):
        """Update UI with new weather data (called from main thread)"""
        self.current_weather = weather_data
        self.ui.update_weather_display(weather_data)
        self.ui.show_loading(False)
        self.ui.update_status(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def _show_error(self, error_msg):
        """Show error message (called from main thread)"""
        self.ui.show_loading(False)
        self.ui.update_status(f"Error: {error_msg}")
        messagebox.showerror("Error", error_msg)
    
    def show_settings_dialog(self):
        """Show settings configuration dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#1a1a2e')
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the dialog
        settings_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 200,
            self.root.winfo_rooty() + 150
        ))
        
        # API Key section
        api_frame = ttk.LabelFrame(settings_window, text="NASA API Configuration", padding="10")
        api_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(api_frame, text="API Key:").pack(anchor="w")
        api_key_var = tk.StringVar(value=self.config.get('api_key', 'DEMO_KEY'))
        api_entry = ttk.Entry(api_frame, textvariable=api_key_var, width=50, show="*")
        api_entry.pack(fill="x", pady=5)
        
        # Units section
        units_frame = ttk.LabelFrame(settings_window, text="Display Units", padding="10")
        units_frame.pack(fill="x", padx=20, pady=10)
        
        temp_unit_var = tk.StringVar(value=self.config.get('temperature_unit', 'Celsius'))
        ttk.Radiobutton(units_frame, text="Celsius", variable=temp_unit_var, value="Celsius").pack(anchor="w")
        ttk.Radiobutton(units_frame, text="Fahrenheit", variable=temp_unit_var, value="Fahrenheit").pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        def save_settings():
            self.config['api_key'] = api_key_var.get()
            self.config['temperature_unit'] = temp_unit_var.get()
            save_config(self.config)
            
            # Update API client with new key
            self.api_client.api_key = api_key_var.get()
            
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings saved successfully!")
        
        def get_api_key():
            import webbrowser
            webbrowser.open("https://api.nasa.gov/")
        
        ttk.Button(button_frame, text="Get API Key", command=get_api_key).pack(side="left")
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side="right")
    
    def run(self):
        """Start the application main loop"""
        # Set up window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the GUI event loop
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        self.root.quit()
        self.root.destroy()

def main():
    """Main function to start the Mars Weather App"""
    try:
        app = MarsWeatherApp()
        app.run()
    except Exception as e:
        print(f"Failed to start Mars Weather App: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
