# Wi-Fi-Network-Scanner
This is a **Python-based Wi-Fi Network Scanner for Windows**, built with **Tkinter GUI**.  
It scans nearby Wi-Fi networks using the Windows `netsh` command and displays:

-  SSID (Network Name)
-  MAC Address (BSSID)
-  Signal Strength (with emoji indicators)
-  Frequency Band (e.g. 2.4 GHz, 5 GHz)
-  Encryption Type (WPA2, Open, etc.)

>  Built for **personal & educational use** to analyze nearby networks and pick the best one for connectivity.

---

## Features

-  **One-click Scan:** Scans available Wi-Fi networks on demand.
-  **Threaded scanning:** Keeps the GUI responsive during scanning.
-  **Signal icons:** Emoji indicators show signal strength visually.
-  **Detailed info:** Shows SSID, MAC, signal %, band, encryption.
-  **Tkinter GUI:** Simple, clean interface with a progress bar and status updates.
-  **Runs on Windows** using built-in `netsh` (no external Wi-Fi drivers needed).

---
Install required Python packages:
pip install -r requirements.txt

 How It Works
Uses subprocess to run
Parses the output to extract:

 SSID: Network name
 BSSID: MAC address
 Signal: Wi-Fi strength %
 Band: Frequency (2.4 / 5 GHz)
 Encryption: WPA2, Open, etc.

Displays data in a ttk.Treeview table with neat columns and emojis for quick visual cues.

Requirements
Windows 10/11
Python 3.8+

tkinter (usually comes bundled with Python on Windows)

Uses built-in subprocess, threading libraries.
