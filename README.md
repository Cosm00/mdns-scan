## mdns-scan

> Elegant mDNS/Bonjour network scanner - Discover devices and services on your local network with style.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

Discover Apple TVs, HomePods, printers, smart home devices, servers, and more on your local network using mDNS/Bonjour discovery. Beautiful ASCII art, clean output, and JSON export support.

## Features

✨ **Beautiful** - Gorgeous ASCII art and clean table output  
🔍 **Comprehensive** - Scans 20+ common service types  
⚡ **Fast** - Parallel service discovery  
📊 **Informative** - Shows device names, IPs, ports, and properties  
💾 **Export** - JSON output for automation  
🎯 **Flexible** - Custom service types and timeouts  

## Quick Start

```bash
# Clone and install
git clone https://github.com/cosm00/mdns-scan.git
cd mdns-scan
pip3 install -r requirements.txt

# Run the scanner
python3 mdns-scan.py
```

## Example Output

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ███╗   ███╗██████╗ ███╗   ██╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
║   ████╗ ████║██╔══██╗████╗  ██║██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
║   ██╔████╔██║██║  ██║██╔██╗ ██║███████╗    ███████╗██║     ███████║██╔██╗ ██║
║   ██║╚██╔╝██║██║  ██║██║╚██╗██║╚════██║    ╚════██║██║     ██╔══██║██║╚██╗██║
║   ██║ ╚═╝ ██║██████╔╝██║ ╚████║███████║    ███████║╚██████╗██║  ██║██║ ╚████║
║   ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
║                                                                   ║
║              Discover devices and services on your network        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

⏱  Scan timeout: 5s
🔍 Services to scan: 24
🕐 Started: 2026-02-08 20:34:15
======================================================================

🔎 Scanning network for mDNS/Bonjour devices...

  ⠹ Scanning... (8 devices found)

======================================================================
📊 Scan Results: 8 device(s) discovered
======================================================================

┌─ Device #1: Cosmo-MacBook-Pro.local
│  📍 IP: 192.168.1.100
│  🔌 Services:
│     • ssh                → 192.168.1.100:22
│     • http               → 192.168.1.100:80
│     • smb                → 192.168.1.100:445
│

┌─ Device #2: Living-Room-Apple-TV.local
│  📍 IP: 192.168.1.101
│  🔌 Services:
│     • airplay            → 192.168.1.101:7000
│       - model: AppleTV11,1
│       - osvers: 17.3
│       - features: 0x5A7FFFF7
│     • companion-link     → 192.168.1.101:49152
│

┌─ Device #3: HP-LaserJet-M404.local
│  📍 IP: 192.168.1.102
│  🔌 Services:
│     • printer            → 192.168.1.102:631
│       - ty: HP LaserJet M404
│       - pdl: application/pdf
│     • ipp                → 192.168.1.102:631
│

┌─ Device #4: HomePod-Kitchen.local
│  📍 IP: 192.168.1.103
│  🔌 Services:
│     • airplay            → 192.168.1.103:7000
│     • homekit            → 192.168.1.103:8080
│       - pv: 1.0
│       - id: AA:BB:CC:DD:EE:FF
│

======================================================================
```

## Usage

### Basic Scanning

```bash
# Default scan (5 second timeout, all common services)
python3 mdns-scan.py

# Longer scan for more devices
python3 mdns-scan.py --timeout 10

# Show detailed discovery progress
python3 mdns-scan.py --verbose
```

### Targeted Service Discovery

```bash
# Scan only for HTTP servers
python3 mdns-scan.py --services _http._tcp.local.

# Scan for multiple specific services
python3 mdns-scan.py --services _airplay._tcp.local.,_homekit._tcp.local.,_printer._tcp.local.

# Find all SSH-enabled devices
python3 mdns-scan.py --services _ssh._tcp.local. --timeout 10
```

### Export and Automation

```bash
# Export to JSON
python3 mdns-scan.py --json > scan-results.json

# Quiet JSON output (no banner)
python3 mdns-scan.py --json --no-banner

# Pipe to jq for filtering
python3 mdns-scan.py --json | jq '.devices[] | select(.service_type | contains("airplay"))'
```

### Advanced Examples

```bash
# Find all Apple devices (10s timeout)
python3 mdns-scan.py --timeout 10 --services _airplay._tcp.local.,_homekit._tcp.local.,_companion-link._tcp.local.

# Find network storage
python3 mdns-scan.py --services _smb._tcp.local.,_afpovertcp._tcp.local.

# Find printers and scanners
python3 mdns-scan.py --services _printer._tcp.local.,_ipp._tcp.local.,_scanner._tcp.local.

# Find Chromecasts and smart speakers
python3 mdns-scan.py --services _googlecast._tcp.local.,_spotify-connect._tcp.local.
```

## Discovered Service Types

**mdns-scan** discovers these common mDNS/Bonjour service types by default:

### Media & Entertainment
- `_airplay._tcp` - AirPlay devices (Apple TV, HomePod, speakers)
- `_raop._tcp` - Remote Audio Output Protocol
- `_googlecast._tcp` - Google Cast devices (Chromecast)
- `_spotify-connect._tcp` - Spotify Connect devices
- `_daap._tcp` - iTunes music sharing

### Smart Home
- `_homekit._tcp` - HomeKit accessories
- `_hap._tcp` - HomeKit Accessory Protocol
- `_companion-link._tcp` - Apple TV/HomePod

### Network Services
- `_http._tcp` - HTTP web servers
- `_https._tcp` - HTTPS web servers
- `_ssh._tcp` - SSH servers
- `_sftp-ssh._tcp` - SFTP servers
- `_smb._tcp` - SMB/CIFS file sharing
- `_afpovertcp._tcp` - Apple File Protocol
- `_ftp._tcp` - FTP servers

### Printers & Scanners
- `_printer._tcp` - Network printers
- `_ipp._tcp` - Internet Printing Protocol
- `_scanner._tcp` - Network scanners

### Remote Access
- `_rdp._tcp` - Remote Desktop Protocol
- `_vnc._tcp` / `_rfb._tcp` - VNC servers

### System
- `_workstation._tcp` - Workstations
- `_device-info._tcp` - Device information
- `_sleep-proxy._udp` - Sleep Proxy servers

## Installation

### Option 1: Clone and Install

```bash
git clone https://github.com/cosm00/mdns-scan.git
cd mdns-scan
pip3 install -r requirements.txt
python3 mdns-scan.py
```

### Option 2: Direct Download

```bash
# Download script
curl -O https://raw.githubusercontent.com/cosm00/mdns-scan/main/mdns-scan.py

# Install dependency
pip3 install zeroconf

# Run
python3 mdns-scan.py
```

### Option 3: System-Wide Install

```bash
# Clone repository
git clone https://github.com/cosm00/mdns-scan.git
cd mdns-scan
pip3 install -r requirements.txt

# Make executable
chmod +x mdns-scan.py

# Create symlink (optional)
sudo ln -s $(pwd)/mdns-scan.py /usr/local/bin/mdns-scan

# Now run from anywhere
mdns-scan --help
```

## Requirements

- **Python 3.6+** - Usually pre-installed on macOS/Linux
- **zeroconf** - mDNS/Bonjour library (`pip3 install zeroconf`)
- **Network access** - Must be on the same local network as devices

## Command-Line Options

```
usage: mdns-scan.py [-h] [--timeout N] [--services SERVICE1,SERVICE2]
                    [--json] [--no-banner] [--verbose]

Options:
  --timeout N              Scan timeout in seconds (default: 5)
  --services S1,S2,...     Comma-separated service types to scan
  --json                   Output results as JSON
  --no-banner              Hide ASCII art banner
  --verbose                Show detailed scanning progress
  --help                   Show help message
```

## Use Cases

### Home Network Audit
Discover all devices on your home network:
```bash
python3 mdns-scan.py --timeout 10 --verbose
```

### Find Smart Home Devices
Locate all HomeKit and smart home devices:
```bash
python3 mdns-scan.py --services _homekit._tcp.local.,_hap._tcp.local.
```

### Network Printer Discovery
Find all network printers:
```bash
python3 mdns-scan.py --services _printer._tcp.local.,_ipp._tcp.local.
```

### Security Scanning
Find SSH-enabled devices:
```bash
python3 mdns-scan.py --services _ssh._tcp.local. --timeout 10
```

### Media Device Inventory
Find all AirPlay/Cast devices:
```bash
python3 mdns-scan.py --services _airplay._tcp.local.,_googlecast._tcp.local.,_raop._tcp.local.
```

### Automation & Monitoring
Export to JSON for processing:
```bash
python3 mdns-scan.py --json --no-banner > devices.json
```

## Troubleshooting

### No devices found

**Possible causes:**
- Not on the same local network as devices
- Firewall blocking mDNS (port 5353/UDP)
- Devices don't support mDNS/Bonjour
- Scan timeout too short

**Solutions:**
```bash
# Try longer timeout
python3 mdns-scan.py --timeout 15

# Check firewall settings (macOS)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Check network connectivity
ping 224.0.0.251  # mDNS multicast address
```

### "zeroconf not found" error

Install the required dependency:
```bash
pip3 install zeroconf
```

### Slow scanning

Large networks take time. Use `--verbose` to see progress:
```bash
python3 mdns-scan.py --verbose --timeout 10
```

### Duplicate devices

Some devices advertise multiple services and may appear multiple times. This is normal and shows all available services.

## Privacy & Security

⚠️ **mdns-scan is read-only** - It only listens for mDNS advertisements and never sends commands to devices.

⚠️ **Local network only** - mDNS works only on the local network (doesn't traverse routers).

⚠️ **Public devices** - Any device advertising mDNS services is publicly discoverable on the local network.

✅ **Safe to use** - No risk to devices or network.

## Technical Details

- **Protocol:** mDNS (Multicast DNS) / Bonjour / Avahi
- **Port:** 5353/UDP (multicast)
- **Address:** 224.0.0.251 (IPv4) / ff02::fb (IPv6)
- **Standard:** RFC 6762 (mDNS), RFC 6763 (DNS-SD)

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Request new features
- Submit pull requests
- Add more service types

## Related Tools

- **dns-sd** - macOS built-in mDNS browser (`dns-sd -B _services._dns-sd._udp`)
- **avahi-browse** - Linux mDNS browser
- **Discovery - DNS-SD Browser** - iOS/macOS GUI app

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Created by [cosm00](https://github.com/cosm00)

## Acknowledgments

Built with [python-zeroconf](https://github.com/jstasiak/python-zeroconf) - the excellent Python mDNS library.

Inspired by the need for a beautiful, modern mDNS scanner with style.

---

**Star this repo if it helped you discover your network!** ⭐
