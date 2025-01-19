
![그림16 (1)](https://github.com/user-attachments/assets/dd7cc69c-8cbb-4ca4-adb3-7e9d7ab17606)

# Description
**andro-hunting** is an automated tool designed to analyze **Android's Deeplink Webview Hijacking Vulnerability**.

# Installation
1. `python3 -m venv venv` -> Create a virtual environment.
2. `source venv/bin/activate` -> Activate the virtual environment.
3. `pip install -r requirements.txt` -> Install required packages.
4. `cp .env.example .env` -> Create a `.env` file and set your URL.
5. `cp applist.txt.example applist.txt` -> Write the app's package names in `applist.txt`.
6. Now You can run the script!

**System Requirements:**
- Python 3
- ADB (must be connected to only one ADB server)
- Rooted device or emulator (for `sub.py`)
- Logged in to Play Store
- Frida (for `sub.py`)


![image](https://github.com/user-attachments/assets/af572d40-fbe1-4e44-962a-9a37822bbf89)

# Usage
Refer to our [wiki page](https://github.com/WHS-Andromeda/andro_hunting.wiki.git) for detailed usage instructions.

## Demos:
- MAIN
- SUB
- CHEATSHEET

## Using main.py
The primary purpose of **Andro-Hunting** is to automate the WebView hijacking Proof of Concept (PoC) through large-scale Android app analysis. It is highly effective for mobile bug hunting. You can modify deep link URL parameters to include webhooks site, Discord server addresses, etc., to receive automatic alerts.

- Parse and analyze APK files
- Extract deeplink information and create various URL combinations
- Automate WebView hijacking PoC

## Using sub.py
sub.py is a tool designed to research attack vector expansion based on the app information analyzed by `main.py`. It allows automatic deeplink testing, bypassing XSS filters, and provides functionality for log analysis and method hooking for deeplink, WebView and JavaScript Interface methods.

- Automatic XSS testing
- Save dumpsys and logcat logs on deeplink invocation
- Automatic deeplink, WebView and JavaScript Interface methods hooking

# Screenshots

 **XSS Testing**
  
![xss_test](https://github.com/user-attachments/assets/de6172d0-6b79-4903-9625-24cb16845394)

 **DeepLink/WebView/JSI Monitoring**
  
![frida_hook](https://github.com/user-attachments/assets/928d95d8-38ba-44c8-8c73-4e536a731483)


