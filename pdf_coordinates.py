# PDF Field Coordinates Configuration
# 
# This file contains X,Y coordinates for each field in the FGAR Build Sheet PDF.
# PDF coordinate system: Origin (0,0) is at BOTTOM-LEFT
# Page size: 612 x 792 points (standard letter size)
# Y-axis: 0 = bottom, 792 = top
#
# IMPORTANT: To adjust alignment, modify the Y values:
# - INCREASE Y to move text UP on the page
# - DECREASE Y to move text DOWN on the page
# - INCREASE X to move text RIGHT
# - DECREASE X to move text LEFT

FIELD_COORDINATES = {
    "battery_duration": {"x": 238, "y": 471},  # Battery Duration
    "battery_health": {"x": 147, "y": 495},  # Battery Health
    "build_date": {"x": 356, "y": 199},  # Build Date
    "built_by": {"x": 128, "y": 200},  # Built By
    "chrome": {"x": 219, "y": 295},  # Chrome
    "cpu_cores": {"x": 111, "y": 550},  # Cpu Cores
    "cpu_model": {"x": 125, "y": 580},  # Cpu Model
    "cpu_speed": {"x": 383, "y": 550},  # Cpu Speed
    "cpu_threads": {"x": 231, "y": 550},  # Cpu Threads
    "description": {"x": 147, "y": 668},  # Description
    "firefox": {"x": 326, "y": 295},  # Firefox
    "libreoffice": {"x": 457, "y": 295},  # Libreoffice
    "microphone": {"x": 457, "y": 440},  # Microphone
    "os_name": {"x": 166, "y": 325},  # Os Name
    "os_version": {"x": 376, "y": 327},  # Os Version
    "price": {"x": 438, "y": 607},  # Price
    "ram": {"x": 115, "y": 523},  # Ram
    "ram_type": {"x": 166, "y": 522},  # Ram Type
    "screen_size": {"x": 352, "y": 495},  # Screen Size
    "serial": {"x": 105, "y": 639},  # Serial
    "speakers": {"x": 335, "y": 440},  # Speakers
    "storage_capacity": {"x": 336, "y": 525},  # Storage Capacity
    "storage_type_hdd": {"x": 386, "y": 520},  # Storage Type Hdd
    "storage_type_ssd": {"x": 421, "y": 520},  # Storage Type Ssd
    "vlc": {"x": 99, "y": 295},  # Vlc
    "webcam": {"x": 223, "y": 440},  # Webcam
    "wifi": {"x": 93, "y": 440},  # Wifi
}

# Font settings
FONT_NAME = "Helvetica"
FONT_SIZE = 10
FONT_SIZE_PRICE = 25
FONT_SIZE_MODEL = 15

# Checkbox text for features
CHECKBOX_YES = "✓"
