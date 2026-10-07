"""
Optional voice feature.

This module intentionally does NOT claim that speech-to-text is biometric
voice authentication. Browser speech input is a convenience feature only.
Real voice biometrics require a dedicated, securely designed biometric system.
"""
import importlib.util

def voice_status():
    return {
        "browser_speech": True,
        "python_speech_recognition_installed": importlib.util.find_spec("speech_recognition") is not None,
        "note": "Speech-to-text is not biometric identity verification."
    }
