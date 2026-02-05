"""
PDF Filler - Utility to fill in the FGAR Build Sheet PDF template with computer data.
Uses PyPDF2 and reportlab to overlay text onto the existing PDF template.

This version is specifically tailored to the FGAR Build Sheet template with correct coordinates.
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
import os
import datetime


class BuildSheetPDFFiller:
    """Fills in the FGAR Build Sheet PDF template with computer specifications and pricing."""
    
    def __init__(self, template_path="FGAR_BuildSheet.pdf"):
        self.template_path = template_path
        # PDF is standard letter size: 612 x 792 points
        # Origin (0,0) is at bottom-left
        self.page_width = 612
        self.page_height = 792
        
    def create_overlay(self, data):
        """
        Create a PDF overlay with the data to be filled in.
        Uses coordinates from pdf_coordinates.py configuration file.
        """
        from pdf_coordinates import FIELD_COORDINATES, FONT_NAME, FONT_SIZE, CHECKBOX_YES
        
        # Optional: larger font size for price (default to 3x normal if not defined)
        try:
            from pdf_coordinates import FONT_SIZE_PRICE
        except ImportError:
            FONT_SIZE_PRICE = FONT_SIZE * 2.5
        
        try:
            from pdf_coordinates import FONT_SIZE_MODEL
        except ImportError:
            FONT_SIZE_MODEL = FONT_SIZE * 1.5
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Set default font
        can.setFont(FONT_NAME, FONT_SIZE)
        
        # === TOP SECTION ===
        if data.get('model'):
            can.setFont(FONT_NAME, FONT_SIZE_MODEL)
            coords = FIELD_COORDINATES["description"]
            can.drawString(coords["x"], coords["y"], data['model'])
            can.setFont(FONT_NAME, FONT_SIZE)
        
        if data.get('serial'):
            coords = FIELD_COORDINATES["serial"]
            can.drawString(coords["x"], coords["y"], data['serial'])
        
        # === HARDWARE SECTION ===
        if data.get('price'):
            coords = FIELD_COORDINATES["price"]
            # Use larger font for price
            can.setFont(FONT_NAME, FONT_SIZE_PRICE)
            can.drawString(coords["x"], coords["y"], f"${data['price']:.0f}")
            can.setFont(FONT_NAME, FONT_SIZE)  # Reset to normal font
        
        # === CPU SECTION ===
        if data.get('cpu_name'):
            coords = FIELD_COORDINATES["cpu_model"]
            can.drawString(coords["x"], coords["y"], data['cpu_name'][:45])
        
        if data.get('cpu_cores'):
            coords = FIELD_COORDINATES["cpu_cores"]
            can.drawString(coords["x"], coords["y"], str(data['cpu_cores']))
        
        if data.get('cpu_threads'):
            coords = FIELD_COORDINATES["cpu_threads"]
            can.drawString(coords["x"], coords["y"], str(data['cpu_threads']))
        
        if data.get('cpu_speed'):
            coords = FIELD_COORDINATES["cpu_speed"]
            can.drawString(coords["x"], coords["y"], str(data['cpu_speed']))
        
        # === MEMORY & STORAGE ===
        # RAM - just the number
        if data.get('ram_gb'):
            coords = FIELD_COORDINATES["ram"]
            can.drawString(coords["x"], coords["y"], str(data['ram_gb']))
        
        # RAM Type - DDR3/DDR4/DDR5 (separate field)
        if data.get('ram_type'):
            coords = FIELD_COORDINATES["ram_type"]
            can.drawString(coords["x"], coords["y"], data['ram_type'])
        
        drives = data.get('drives', [])
        if drives:
            drive = drives[0]
            coords = FIELD_COORDINATES["storage_capacity"]
            can.drawString(coords["x"], coords["y"], f"{drive['capacity_gb']}")
            
            # HDD/SSD indicator - draw circle around the text (text already on template)
            drive_type = drive.get('type', 'SSD').upper()
            if 'HDD' in drive_type:
                coords = FIELD_COORDINATES["storage_type_hdd"]
                # Draw a circle at the position (radius 12 points)
                can.circle(coords["x"] + 15, coords["y"] + 5, 12, stroke=1, fill=0)
            elif 'SSD' in drive_type or 'NVME' in drive_type:
                coords = FIELD_COORDINATES["storage_type_ssd"]
                # Draw a circle at the position (radius 12 points)
                can.circle(coords["x"] + 15, coords["y"] + 5, 12, stroke=1, fill=0)
        
        # === LAPTOP-SPECIFIC FIELDS ===
        is_laptop = data.get('is_laptop', False)
        
        # Battery Health - without % symbol
        if is_laptop and data.get('battery_health'):
            coords = FIELD_COORDINATES["battery_health"]
            health_str = str(data['battery_health']).replace('%', '').strip()
            can.drawString(coords["x"], coords["y"], health_str)
        
        if is_laptop and data.get('screen_size'):
            coords = FIELD_COORDINATES["screen_size"]
            can.drawString(coords["x"], coords["y"], str(data['screen_size']))
        
        if is_laptop and data.get('battery_duration'):
            coords = FIELD_COORDINATES["battery_duration"]
            can.drawString(coords["x"], coords["y"], str(data['battery_duration']))
        
        # === FEATURES ===
        features = data.get('features', {})
        
        if features.get('wifi'):
            coords = FIELD_COORDINATES["wifi"]
            can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        if features.get('webcam'):
            coords = FIELD_COORDINATES["webcam"]
            can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        if features.get('sound'):
            coords = FIELD_COORDINATES["speakers"]
            can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        if features.get('microphone'):
            coords = FIELD_COORDINATES["microphone"]
            can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        # === SOFTWARE SECTION ===
        if data.get('os_name'):
            os_parts = data['os_name'].split()
            if len(os_parts) >= 2:
                os_base = ' '.join(os_parts[:2])
                os_version = ' '.join(os_parts[2:]) if len(os_parts) > 2 else ""
                
                coords = FIELD_COORDINATES["os_name"]
                can.drawString(coords["x"], coords["y"], os_base)
                
                if os_version:
                    coords = FIELD_COORDINATES["os_version"]
                    can.drawString(coords["x"], coords["y"], os_version)
            else:
                coords = FIELD_COORDINATES["os_name"]
                can.drawString(coords["x"], coords["y"], data['os_name'])
        
        # Software checkboxes - use checkmarks
        coords = FIELD_COORDINATES["vlc"]
        can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        coords = FIELD_COORDINATES["chrome"]
        can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        coords = FIELD_COORDINATES["firefox"]
        can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        coords = FIELD_COORDINATES["libreoffice"]
        can.drawString(coords["x"], coords["y"], CHECKBOX_YES)
        
        # === BUILD INFO ===
        if data.get('builder_name'):
            coords = FIELD_COORDINATES["built_by"]
            can.drawString(coords["x"], coords["y"], data['builder_name'])
        
        build_date = data.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
        coords = FIELD_COORDINATES["build_date"]
        can.drawString(coords["x"], coords["y"], build_date)
        
        # Approved By - Y ~265
        # Leave blank - filled manually
        
        # Approved Date - Y ~265 (same row, right side)
        # Leave blank
        
        can.save()
        packet.seek(0)
        return packet
    
    def fill_template(self, data, output_path="filled_buildsheet.pdf"):
        """
        Fill the template PDF with data and save to output_path.
        
        Args:
            data (dict): Computer specs and pricing data
            output_path (str): Path to save the filled PDF
        
        Returns:
            str: Path to the generated PDF
        """
        # Check if template exists
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template PDF not found: {self.template_path}")
        
        # Create overlay
        overlay_pdf = self.create_overlay(data)
        
        # Read template
        template = PdfReader(self.template_path)
        overlay = PdfReader(overlay_pdf)
        
        # Create output
        output = PdfWriter()
        
        # Merge overlay onto template
        template_page = template.pages[0]
        overlay_page = overlay.pages[0]
        
        # Merge the overlay onto the template
        template_page.merge_page(overlay_page)
        output.add_page(template_page)
        
        # Write to file
        with open(output_path, 'wb') as output_file:
            output.write(output_file)
        
        return output_path


# Test function
if __name__ == "__main__":
    # Test data
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
        'builder_name': 'John Doe',
        'is_laptop': True,
        'screen_size': '14',
        'battery_health': '85',
        'battery_duration': '3.5',
        'features': {
            'wifi': True,
            'bluetooth': True,
            'webcam': True,
            'sound': True,
            'microphone': True
        }
    }
    
    filler = BuildSheetPDFFiller()
    try:
        output = filler.fill_template(test_data, "test_filled_v2.pdf")
        print(f"Successfully created: {output}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
