import subprocess
import tkinter as tk
from tkinter import ttk
from threading import Thread

def parse_netsh_output(output):
    networks = []
    curr_ssid = None
    curr_encryption = None
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("SSID") and "BSSID" not in line:
            parts = line.split(" : ", 1)
            curr_ssid = parts[1].strip() if len(parts) > 1 else ""
            curr_encryption = None
        elif line.startswith("Encryption"):
            parts = line.split(" : ", 1)
            curr_encryption = parts[1].strip() if len(parts) > 1 else ""
            if curr_encryption.lower() == "none":
                curr_encryption = "Open"
        elif line.startswith("BSSID"):
            parts = line.split(" : ", 1)
            bssid = parts[1].strip() if len(parts) > 1 else ""
            networks.append({
                "SSID": curr_ssid,
                "BSSID": bssid,
                "Signal": "",
                "Frequency": "",
                "Encryption": curr_encryption
            })
        elif line.startswith("Signal"):
            parts = line.split(" : ", 1)
            networks[-1]["Signal"] = parts[1].strip() if len(parts) > 1 else ""
        elif line.startswith("Band"):
            parts = line.split(" : ", 1)
            networks[-1]["Frequency"] = parts[1].strip() if len(parts) > 1 else ""
    return networks

def scan_networks():
    scan_button.config(state=tk.DISABLED)
    status_label.config(text="🔍 Scanning for Wi-Fi networks...")
    progress.start()
    
    def worker():
        try:
            output = subprocess.check_output(
                "netsh wlan show networks mode=bssid", 
                shell=True, text=True, encoding='cp1252', errors='ignore'
            )
            networks = parse_netsh_output(output)
        except Exception as e:
            status_label.config(text="❌ Error scanning for networks.")
            scan_button.config(state=tk.NORMAL)
            progress.stop()
            return

        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        # Insert new rows
        for net in networks:
            signal_strength = net["Signal"].replace('%', '')
            signal_emoji = "📶" if int(signal_strength) > 70 else "📡"
            tree.insert("", "end", values=(
                signal_emoji + " " + net["SSID"], net["Signal"], net["BSSID"], net["Frequency"], net["Encryption"]
            ))

        status_label.config(text=f"✅ Found {len(networks)} network(s).")
        scan_button.config(state=tk.NORMAL)
        progress.stop()

    Thread(target=worker).start()

# Create main window
root = tk.Tk()
root.title("📡 Wi-Fi Network Scanner (Windows)")
root.geometry("740x450")

style = ttk.Style(root)
style.theme_use('clam')
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

scan_button = ttk.Button(frame, text="🔄 Scan Wi-Fi Networks", command=scan_networks)
scan_button.pack(pady=10)

progress = ttk.Progressbar(frame, mode='indeterminate')
progress.pack(fill='x', padx=5, pady=5)

columns = ("SSID 📶", "Signal Strength", "MAC Address 🔒", "Frequency 📡", "Encryption")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

status_label = ttk.Label(root, text="🟡 Click 'Scan' to begin.", font=("Segoe UI", 10))
status_label.pack(pady=5)

root.mainloop()

