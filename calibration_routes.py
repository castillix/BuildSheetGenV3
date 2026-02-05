"""
Visual PDF Calibration Tool - Flask Routes

Adds endpoints for the visual calibration interface.
"""

from flask import Blueprint, render_template, request, jsonify, send_file
import json
import os

calibration_bp = Blueprint('calibration', __name__)

@calibration_bp.route('/calibrate')
def calibration_page():
    """Render the visual calibration interface."""
    return render_template('calibrate.html')

@calibration_bp.route('/api/pdf_template')
def get_pdf_template():
    """Serve the PDF template file."""
    import os
    from flask import send_file
    pdf_path = os.path.join(os.getcwd(), 'FGAR_BuildSheet.pdf')
    return send_file(pdf_path, mimetype='application/pdf')

@calibration_bp.route('/api/get_coordinates', methods=['GET'])
def get_coordinates():
    """Get current field coordinates."""
    try:
        # Import the current coordinates
        import pdf_coordinates
        # Reload to get latest changes
        import importlib
        importlib.reload(pdf_coordinates)
        
        return jsonify({
            'success': True,
            'coordinates': pdf_coordinates.FIELD_COORDINATES
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@calibration_bp.route('/api/save_coordinates', methods=['POST'])
def save_coordinates():
    """Save updated field coordinates back to pdf_coordinates.py."""
    try:
        data = request.json
        new_coords = data.get('coordinates', {})
        
        # Read the current file
        coords_file = 'pdf_coordinates.py'
        
        # Generate new file content
        content = '''# PDF Field Coordinates Configuration
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
'''
        
        # Add each coordinate
        for field_name, coords in new_coords.items():
            x = int(coords['x'])
            y = int(coords['y'])
            comment = coords.get('comment', field_name.replace('_', ' ').title())
            content += f'    "{field_name}": {{"x": {x}, "y": {y}}},  # {comment}\n'
        
        content += '''}

# Font settings
FONT_NAME = "Helvetica"
FONT_SIZE = 10

# Checkbox text for features
CHECKBOX_YES = "Yes"
'''
        
        # Write to file
        with open(coords_file, 'w') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': 'Coordinates saved successfully!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@calibration_bp.route('/api/generate_test_pdf', methods=['POST'])
def generate_test_pdf():
    """Generate a test PDF with sample data and return it."""
    try:
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
        output_path = 'test_output.pdf'
        filler.fill_template(test_data, output_path)
        
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=False,
            download_name='test_output.pdf'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
