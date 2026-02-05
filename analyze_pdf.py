"""
Analyze PDF template to understand layout and prepare for proper filling.
"""
from PyPDF2 import PdfReader

pdf = PdfReader('FGAR_BuildSheet.pdf')
page = pdf.pages[0]

print("=== PDF Template Analysis ===")
print(f"Pages: {len(pdf.pages)}")
print(f"Page size: {page.mediabox}")
print(f"Width: {float(page.mediabox.width)}, Height: {float(page.mediabox.height)}")

# Extract text to see field layout
text = page.extract_text()
print("\n=== Template Structure ===")
print(text)

# Check for form fields
fields = pdf.get_fields()
if fields:
    print(f"\n=== Form Fields Found: {len(fields)} ===")
    for name, field in fields.items():
        print(f"  {name}: {field}")
else:
    print("\n=== No fillable form fields found ===")
    print("This is a static PDF with text. We'll need to overlay text at specific coordinates.")

print("\n=== Field Mapping Needed ===")
print("Based on the extracted text, the template has these fields:")
print("  - Description (Computer model/name)")
print("  - S/N (Serial number)")
print("  - Price")
print("  - CPU Model")
print("  - Cores")
print("  - Threads")
print("  - Base Clock Speed (GHz)")
print("  - RAM (GB)")
print("  - Storage (GB, HDD/SSD)")
print("  - Battery Health (%)")
print("  - Screen Size (Inch)")
print("  - Approx. Use Time on Full Charge (Hrs)")
print("  - WiFi, Webcam, Speakers, Microphone (checkboxes)")
print("  - Notes (Hardware)")
print("  - Operating System")
print("  - Update Version")
print("  - VLC, Chrome, Firefox, LibreOffice (checkboxes)")
print("  - Notes (Software)")
print("  - Built By")
print("  - Build Date")
print("  - Approved By")
print("  - Approved Date")
