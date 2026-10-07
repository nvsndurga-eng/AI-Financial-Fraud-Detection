"""
Fingerprint integration boundary.

A normal Python web application cannot safely assume access to laptop fingerprint
hardware. Real integration depends on the operating system, sensor vendor,
driver and/or platform authentication API.

The application therefore exposes a clearly labelled DEMO MODE status only.
No raw fingerprint data is stored.
"""

def fingerprint_status():
    return {
        "mode": "DEMO MODE",
        "hardware_connected": False,
        "note": "No raw fingerprint data is stored. Connect a supported hardware/API integration for real verification."
    }
