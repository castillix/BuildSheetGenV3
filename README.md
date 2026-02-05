# Build Sheet Generator V3

Web-based tool for automating computer build sheet generation and pricing at Free Geek Arkansas.

## Features

- **Automated Pricing**: Calculate computer prices based on hardware specifications using a proven pricing algorithm
- **CPU Database Search**: Search and select CPUs from a comprehensive database with Passmark scores
- **Manual Entry Option**: Enter custom CPU specifications if not found in database
- **PDF Build Sheets**: Generate professional build sheets by filling in an existing PDF template
- **Network Accessible**: Run on one computer and access from any device on the network
- **Real-time Price Preview**: See pricing updates as you fill out the form
- **Multiple Drives Support**: Handle computers with multiple storage devices

## Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection for initial setup

### Windows

1. Open the project folder in File Explorer
2. Double-click `run.bat`
3. The script will automatically:
   - Create a virtual environment
   - Install dependencies
   - Start the web server

### Linux/Mac

1. Open terminal in the project directory
2. Make the script executable: `chmod +x run.sh`
3. Run: `./run.sh`

## Usage

### Starting the Server

Run the appropriate script for your operating system:
- **Windows**: Double-click `run.bat`
- **Linux/Mac**: Run `./run.sh` in terminal

The server will start and display URLs for access.

### Accessing from Other Computers

1. Find the IP address of the computer running the server
   - Windows: Run `ipconfig` in Command Prompt
   - Linux/Mac: Run `ifconfig` or `ip addr` in terminal
2. On any other computer on the same network, open a web browser
3. Navigate to: `http://SERVER-IP-ADDRESS:5000`

### Filling Out the Form

1. **Computer Information**: Enter model, serial number, and select laptop/desktop
2. **Processor**: Either search the database or enter CPU specs manually
3. **Memory**: Enter RAM amount and type (DDR3/DDR4/DDR5)
4. **Storage**: Add one or more drives with capacity and type
5. **Graphics**: Optionally enter GPU information
6. **Operating System**: Enter the OS name and version
7. **Features**: Check applicable features (WiFi, Bluetooth, etc.)
8. **Price Preview**: Click "Recalculate Price" to see the calculated price
9. **Generate**: Click "Generate Build Sheet PDF" to create and download the PDF

## Configuration

### Modifying Pricing

Edit `prices.txt` to adjust pricing parameters:

```
BASE_FEE=40.0
RAM_DDR3_MULT=1.5
RAM_DDR4_MULT=2.5
RAM_DDR5_MULT=6.0
DRIVE_HDD_PER_GB=0.02
DRIVE_SSD_PER_GB=0.08
DRIVE_NVME_PER_GB=0.1
OS_LINUX_MULT=0.85
OS_MACOS_MULT=1.2
OS_WINDOWS_MULT=1.0
CPU_YEAR_BASE=2012
CPU_YEAR_LAPTOP_MULT=6
CPU_YEAR_DESKTOP_MULT=10
CPU_CORE_MULT=0.025
CPU_THREAD_EXCESS_PRICE=0.75
```

After making changes, restart the server.

### Updating the PDF Template

Replace `FGAR BuildSheet.docx.pdf` with your updated template. The coordinate system in `pdf_filler.py` may need adjustment if the template layout changes significantly.

## Project Structure

```
BuildSheetGenV3/
├── app.py                 # Main Flask application
├── pricing.py             # Pricing calculation engine
├── pdf_filler.py          # PDF template filling utility
├── cpus.db                # CPU database with specs
├── prices.txt             # Pricing configuration
├── FGAR BuildSheet.docx.pdf  # PDF template
├── requirements.txt       # Python dependencies
├── run.bat                # Windows launcher
├── run.sh                 # Linux/Mac launcher
├── templates/
│   └── index.html         # Main form template
├── static/
│   ├── styles.css         # Styling
│   └── app.js             # Frontend JavaScript
└── generated/             # Generated PDFs (created automatically)
```

## Troubleshooting

### Server Won't Start

- Ensure Python 3.7+ is installed: `python --version`
- Check that port 5000 is not in use by another application
- Try running with administrator/sudo privileges

### Cannot Access from Other Computers

- Verify both computers are on the same network
- Check firewall settings allow connections on port 5000
- Ensure you're using the correct IP address of the server computer

### CPU Not Found in Database

- Use the "Manual Entry" mode to input CPU specifications
- Enter the Passmark score from https://www.cpubenchmark.net/

### PDF Generation Fails

- Ensure `FGAR BuildSheet.docx.pdf` exists in the project directory
- Check file permissions on the `generated/` folder
- Verify PyPDF2 is installed: `pip list | grep PyPDF2`

## Dependencies

- Flask 3.0.0 - Web framework
- PyPDF2 3.0.1 - PDF manipulation
- reportlab 4.0.7 - PDF text overlay
- Werkzeug 3.0.1 - WSGI utilities

## Future Enhancements

The following features are planned for future versions:

- Square POS API integration for automatic inventory registration
- Barcode generation and printing
- Build sheet history and reporting
- Multi-user authentication
- Export to Excel/CSV

## Support

For issues or questions, contact the Free Geek Arkansas tech team.

## License

Internal use only - Free Geek Arkansas
