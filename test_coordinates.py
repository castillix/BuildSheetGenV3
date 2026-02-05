"""
Quick Test Script for PDF Coordinate Adjustments

This script generates a test PDF with sample data after you modify coordinates in pdf_coordinates.py.
Just run this script to see your changes immediately!

Usage:
  python test_coordinates.py
"""

from pdf_filler import BuildSheetPDFFiller
import datetime

# Sample test data
test_data = {
    'model': 'Dell Latitude 5490',
    'serial': 'ABC123456789',
    'cpu_name': 'Intel Core i5-8350U',
    'cpu_cores': 4,
    'cpu_threads': 8,
    'cpu_speed': '3.60',
    'ram_gb': 16,
    'ram_type': 'DDR4',
    'drives': [{'capacity_gb': 512, 'type': 'NVMe SSD'}],
    'os_name': 'Windows 11 Pro 23H2',
    'price': 285,
    'builder_name': 'Test Technician',
    'is_laptop': True,
    'screen_size': '14',
    'battery_health': '85%',
    'battery_duration': '3.5',
    'features': {
        'wifi': True,
        'bluetooth': True,
        'webcam': True,
        'sound': True,
        'microphone': True
    }
}

print("=" * 60)
print("PDF COORDINATE TEST")
print("=" * 60)
print("\n1. Edit coordinates in: pdf_coordinates.py")
print("2. Run this script to generate: test_output.pdf")
print("3. Open test_output.pdf to check alignment")
print("4. Repeat until perfect!\n")
print("=" * 60)

filler = BuildSheetPDFFiller()
try:
    output = filler.fill_template(test_data, "test_output.pdf")
    print(f"\n[SUCCESS] Created: {output}")
    print("\nOpen 'test_output.pdf' to check the alignment.")
    print("\nTip: Compare with 'calibration_grid.pdf' to see coordinate markers.")
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
