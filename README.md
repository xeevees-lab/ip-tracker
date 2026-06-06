# 🌍 IP Tracker — IP Geolocation & Intelligence Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Use-Ethical%20Only-red?style=for-the-badge" />
</p>

> **⚠️ DISCLAIMER: This tool is intended for educational and ethical use only. See [Disclaimer](#-disclaimer) section below.**

---

## 📖 About

**IP Tracker** is a terminal-based IP Geolocation and Intelligence tool built with Python, designed for Kali Linux. It uses the free [ip-api.com](http://ip-api.com) API to retrieve detailed information about any IP address or domain — no API key required.

Built as a learning project to understand networking, OSINT concepts, and Python scripting.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌐 Single IP Lookup | Get full geolocation info for any IP address |
| 🌍 Domain Lookup | Automatically resolves domains to IP before lookup |
| 📍 Your Own IP | Detect and geolocate your own public IP address |
| 🔍 Port Scanning | Run a basic Nmap scan on the target IP |
| 📄 Save Reports | Export results to a `.txt` report file |
| 📋 Bulk Lookup | Lookup multiple IPs/domains from a file at once |
| 🖥️ Interactive Mode | Guided prompts when run without arguments |
| 🗺️ Google Maps Link | Auto-generates a Maps link from lat/lon coordinates |
| 🔒 Proxy/VPN Detection | Flags if the target IP is a known proxy or VPN |
| 🔁 Reverse DNS | Shows the hostname associated with the IP |

---

## 📦 Requirements

- Python 3.x
- Kali Linux (or any Debian-based Linux)
- Internet connection

### Python Libraries

```bash
pip3 install requests colorama tabulate dnspython python-nmap --break-system-packages
```

### System Tools

```bash
sudo apt install nmap git -y
```

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ip-tracker.git

# 2. Move into the directory
cd ip-tracker

# 3. Install dependencies
pip3 install requests colorama tabulate dnspython python-nmap --break-system-packages

# 4. Make the script executable
chmod +x ip_tracker.py
```

---

## 🛠️ Usage

### Basic Lookup
```bash
python3 ip_tracker.py -t 8.8.8.8
```

### Domain Lookup
```bash
python3 ip_tracker.py -t google.com
```

### Your Own Public IP
```bash
python3 ip_tracker.py --myip
```

### Lookup + Port Scan
```bash
sudo python3 ip_tracker.py -t 8.8.8.8 --scan
```

### Lookup + Save Report
```bash
python3 ip_tracker.py -t 8.8.8.8 --save
```

### Bulk Lookup from File
```bash
# targets.txt — one IP or domain per line
python3 ip_tracker.py --bulk targets.txt
```

### Bulk + Save All Reports
```bash
python3 ip_tracker.py --bulk targets.txt --scan --save
```

### Interactive Mode (no arguments)
```bash
python3 ip_tracker.py
```

---

## 📊 Sample Output

```
╒══════════════════╤══════════════════════════════════════════════════╕
│ Field            │ Value                                            │
╞══════════════════╪══════════════════════════════════════════════════╡
│ 🌐 IP Address    │ 8.8.8.8                                          │
│ 🏳️  Country       │ United States (US)                              │
│ 🗺️  Region        │ Virginia                                        │
│ 🏙️  City          │ Ashburn                                         │
│ 📮 ZIP Code      │ 20149                                            │
│ 📍 Latitude      │ 39.03                                            │
│ 📍 Longitude     │ -77.5                                            │
│ ⏰ Timezone      │ America/New_York                                 │
│ 📡 ISP           │ Google LLC                                       │
│ 🏢 Organization  │ AS15169 Google LLC                               │
│ 🔢 AS Number     │ AS15169 Google LLC                               │
│ 🔁 Reverse DNS   │ dns.google                                       │
│ 📱 Mobile        │ No                                               │
│ 🔒 Proxy/VPN     │ No                                               │
│ 🖥️  Hosting/DC   │ Yes                                              │
│ 🗺️  Google Maps   │ https://www.google.com/maps?q=39.03,-77.5       │
╘══════════════════╧══════════════════════════════════════════════════╛
```

---

## 📁 Project Structure

```
ip-tracker/
├── ip_tracker.py       # Main script
├── README.md           # This file
├── DISCLAIMER.md       # Legal disclaimer
├── .gitignore          # Ignore report files and cache
└── targets.txt         # (Example) Bulk lookup input file
```

---

## ⚙️ All Arguments

| Argument | Description |
|---|---|
| `-t`, `--target` | Target IP address or domain |
| `--scan` | Run a port scan using Nmap |
| `--save` | Save the results to a report file |
| `--myip` | Look up your own public IP |
| `--bulk FILE` | Bulk lookup from a file (one IP/domain per line) |

---

## 🛡️ Disclaimer

This tool is built **strictly for educational purposes**, cybersecurity learning, and ethical network analysis on systems you own or have explicit permission to test.

- ❌ Do NOT use this tool to track, surveil, or investigate people without consent.
- ❌ Do NOT use this tool for any illegal activity.
- ✅ Only use on IP addresses you own or have written permission to analyze.

The author takes **no responsibility** for any misuse of this tool. By using this software, you agree to use it legally and ethically.

See [DISCLAIMER.md](DISCLAIMER.md) for the full legal notice.

---

## 📡 API Used

- **[ip-api.com](http://ip-api.com)** — Free IP geolocation API, no key required (45 req/min limit on free tier)
- **[api.ipify.org](https://api.ipify.org)** — Used for detecting your own public IP

---

## 🧑‍💻 Author

Built for learning Python, networking, and ethical OSINT concepts on Kali Linux.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) — free to use, modify, and distribute with attribution.
