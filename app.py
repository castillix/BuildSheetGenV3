"""
Build Sheet Generator V3 - Web Application
Flask app for generating computer build sheets with automated pricing.
"""

from flask import Flask, render_template, request, jsonify, send_file
import pricing
import pdf_filler
import os
import datetime
from werkzeug.utils import secure_filename
from calibration_routes import calibration_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'freegeek-buildsheet-secret-key-2026'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register blueprints
app.register_blueprint(calibration_bp)

# Initialize PDF filler
pdf_generator = pdf_filler.BuildSheetPDFFiller()


@app.route('/')
def index():
    """Main form page."""
    return render_template('index.html')


@app.route('/api/search_cpu', methods=['GET'])
def search_cpu():
    """
    Search for CPUs in the database.
    Query parameter: q (search query)
    Returns: JSON list of CPU candidates
    """
    query = request.args.get('q', '')
    
    if not query or len(query) < 2:
        return jsonify([])
    
    try:
        candidates = pricing.get_cpu_candidates(query, db_path='cpus.db', limit=10)
        
        # Format for autocomplete
        results = []
        for cpu in candidates:
            results.append({
                'name': cpu['name'],
                'year': cpu.get('year', '?'),
                'cores': cpu.get('cores', '?'),
                'threads': cpu.get('threads', '?'),
                'clock': cpu.get('clock', '?'),
                'turbo': cpu.get('turbo', '?'),
                'passmark': cpu.get('passmark', '?'),
                'score': cpu.get('score', 0)
            })
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate_price', methods=['POST'])
def calculate_price():
    """
    Calculate the price based on submitted specs.
    Expects JSON with computer specifications.
    Returns: JSON with price breakdown
    """
    try:
        data = request.json
        
        # Parse drives
        drives = []
        if 'drives' in data:
            for drive_data in data['drives']:
                drives.append({
                    'capacity_gb': float(drive_data.get('capacity', 0)),
                    'type': drive_data.get('type', 'SSD')
                })
        
        # Build specs dict for pricing engine
        specs = {
            'cpu_name': data.get('cpu_name', ''),
            'cpu_model_name': data.get('cpu_model_name'),  # If selected from DB
            'ram_gb': float(data.get('ram_gb', 0)),
            'ram_type': data.get('ram_type', 'DDR4'),
            'drives': drives,
            'gpu_price': float(data.get('gpu_price', 0)),
            'os_name': data.get('os_name', 'Windows'),
            'is_laptop': data.get('is_laptop', False)
        }
        
        # Manual passmark if provided
        manual_passmark = None
        if data.get('manual_passmark'):
            manual_passmark = float(data['manual_passmark'])
        
        # Calculate price
        price_data = pricing.calculate_price(specs, db_path='cpus.db', manual_passmark=manual_passmark)
        
        return jsonify({
            'success': True,
            'final_price': price_data['final_price'],
            'breakdown': price_data['breakdown'],
            'specs_used': price_data['specs_used']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/generate_buildsheet', methods=['POST'])
def generate_buildsheet():
    """
    Generate a filled PDF build sheet.
    Expects JSON with complete computer data.
    Returns: PDF file download
    """
    try:
        data = request.json
        
        # Parse drives for display
        drives = []
        if 'drives' in data:
            for drive_data in data['drives']:
                drives.append({
                    'capacity_gb': int(drive_data.get('capacity', 0)),
                    'type': drive_data.get('type', 'SSD')
                })
        
        # Build specs for pricing (needed for final price)
        specs_for_pricing = {
            'cpu_name': data.get('cpu_name', ''),
            'cpu_model_name': data.get('cpu_model_name'),
            'ram_gb': float(data.get('ram_gb', 0)),
            'ram_type': data.get('ram_type', 'DDR4'),
            'drives': drives,
            'gpu_price': float(data.get('gpu_price', 0)),
            'os_name': data.get('os_name', 'Windows'),
            'is_laptop': data.get('is_laptop', False)
        }
        
        # Calculate price
        manual_passmark = None
        if data.get('manual_passmark'):
            manual_passmark = float(data['manual_passmark'])
        
        price_data = pricing.calculate_price(specs_for_pricing, db_path='cpus.db', manual_passmark=manual_passmark)
        
        # Build data dict for PDF
        pdf_data = {
            'model': data.get('model', 'Unknown Model'),
            'serial': data.get('serial', 'N/A'),
            'cpu_name': data.get('cpu_name', 'Unknown CPU').split('@')[0].strip(),  # Remove @ and clock speed
            'cpu_cores': data.get('cpu_cores', price_data['specs_used'].get('cores', '?')),
            'cpu_threads': data.get('cpu_threads', price_data['specs_used'].get('threads', '?')),
            'cpu_speed': data.get('cpu_speed', '0.00'),  # Use cpu_speed from form data
            'ram_gb': data.get('ram_gb', 0),
            'ram_type': data.get('ram_type', 'DDR4'),
            'drives': drives,
            'gpu_name': data.get('gpu_name', ''),
            'os_name': data.get('os_name', 'Unknown'),
            'price': float(data.get('price', price_data['final_price'])),  # Use actual price from form, fallback to calculated
            'builder_name': data.get('builder_name', ''),
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'is_laptop': data.get('is_laptop', False),
            'screen_size': data.get('screen_size', ''),
            'battery_health': data.get('battery_health', ''),
            'battery_duration': data.get('battery_duration', ''),
            'features': {
                'wifi': data.get('wifi', False),
                'bluetooth': data.get('bluetooth', False),
                'webcam': data.get('webcam', False),
                'touchscreen': data.get('touchscreen', False),
                'sound': data.get('sound', False),
                'microphone': data.get('microphone', False)
            }
        }
        
        # Generate PDF
        model_safe = secure_filename(data.get('model', 'buildsheet')).replace(' ', '_')
        serial_safe = secure_filename(data.get('serial', 'NA')).replace(' ', '_')
        output_filename = f"BuildSheet_{model_safe}_{serial_safe}.pdf"
        output_path = os.path.join('generated', output_filename)
        
        # Create generated folder if it doesn't exist
        os.makedirs('generated', exist_ok=True)
        
        # Fill the PDF
        pdf_generator.fill_template(pdf_data, output_path)
        
        # Send file for download
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})


if __name__ == '__main__':
    # Run on all network interfaces so it's accessible from other computers
    # Port 5000 is default Flask port
    print("=" * 60)
    print("Build Sheet Generator V3 - Starting Server")
    print("=" * 60)
    print(f"Access locally at: http://localhost:5000")
    print(f"Access from network at: http://<your-ip-address>:5000")
    print("Press CTRL+C to stop")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
