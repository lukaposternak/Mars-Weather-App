
"""
Setup script for Mars Weather Desktop App
Handles installation, packaging, and distribution
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+ is being used"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or newer is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version.split()[0]} detected")

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    requirements = [
        "requests>=2.28.0",
        "pillow>=9.0.0"
    ]
    
    for requirement in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✅ Installed {requirement}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {requirement}: {e}")
            return False
    
    return True

def create_project_structure():
    """Create the recommended project structure"""
    print("\n📁 Creating project structure...")
    
    directories = [
        "src",
        "assets/images", 
        "assets/icons",
        "tests"
    ]
    
    files = [
        "src/__init__.py",
        "tests/__init__.py",
        "requirements.txt"
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create empty files
    for file_path in files:
        Path(file_path).touch(exist_ok=True)
        print(f"✅ Created file: {file_path}")
    
    # Create requirements.txt content
    with open("requirements.txt", "w") as f:
        f.write("requests>=2.28.0\n")
        f.write("pillow>=9.0.0\n")
        f.write("# tkinter is included with Python standard library\n")

def create_executable():
    """Create executable using PyInstaller"""
    print("\n🔨 Creating executable...")
    
    try:
        # Install PyInstaller if not present
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Create executable
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MarsWeather",
            "src/main.py"
        ]
        
        subprocess.check_call(cmd)
        print("✅ Executable created successfully!")
        print("📍 Check the 'dist' folder for your executable")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create executable: {e}")
        print("💡 You can still run the app directly with: python src/main.py")

def setup_nasa_api():
    """Guide user through NASA API setup"""
    print("\n🚀 NASA API Setup")
    print("=" * 50)
    print("To get real Mars weather data, you need a NASA API key:")
    print("1. Visit: https://api.nasa.gov/")
    print("2. Fill out the simple form (takes 30 seconds)")
    print("3. Copy your API key")
    print("4. Run the app and go to Settings to enter your key")
    print("\n💡 The app will work with demo data without an API key!")

def main():
    """Main setup function"""
    print("🔴 Mars Weather Desktop App Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        sys.exit(1)
    
    # Create project structure
    create_project_structure()
    
    # Guide for NASA API
    setup_nasa_api()
    
    # Ask about executable creation
    print(f"\n🔨 Create executable? (y/n): ", end="")
    if input().lower().startswith('y'):
        create_executable()
    
    print("\n✅ Setup complete!")
    print("\n🚀 To run the app:")
    print("   python src/main.py")
    print("\n📚 Project structure created:")
    print("   src/        - Source code")
    print("   assets/     - Images and icons") 
    print("   tests/      - Test files")
    
if __name__ == "__main__":
    main()
