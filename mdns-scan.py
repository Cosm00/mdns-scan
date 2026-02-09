#!/usr/bin/env python3
"""
mdns-scan - Elegant mDNS/Bonjour network scanner
Discover devices and services on your local network with style.

Usage:
    python3 mdns-scan.py [--timeout SECONDS] [--services SERVICE1,SERVICE2] [--json]
    
Options:
    --timeout N       Scan timeout in seconds (default: 5)
    --services S      Comma-separated list of services to scan (default: all common)
    --json            Output results as JSON
    --no-banner       Hide ASCII art banner
    --verbose         Show detailed scanning progress
    --help            Show this help message

Author: cosm00
License: MIT
"""

import sys
import json
import socket
import argparse
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
from datetime import datetime
from typing import List, Dict, Set
import time


# ASCII Art Banner
BANNER = """
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
"""


# Common mDNS service types
COMMON_SERVICES = [
    "_http._tcp.local.",           # HTTP servers
    "_https._tcp.local.",          # HTTPS servers
    "_ssh._tcp.local.",            # SSH servers
    "_sftp-ssh._tcp.local.",       # SFTP servers
    "_airplay._tcp.local.",        # AirPlay devices
    "_raop._tcp.local.",           # Remote Audio Output Protocol (AirPlay)
    "_homekit._tcp.local.",        # HomeKit devices
    "_hap._tcp.local.",            # HomeKit Accessory Protocol
    "_printer._tcp.local.",        # Printers
    "_ipp._tcp.local.",            # Internet Printing Protocol
    "_scanner._tcp.local.",        # Scanners
    "_smb._tcp.local.",            # SMB/CIFS file sharing
    "_afpovertcp._tcp.local.",     # Apple File Protocol
    "_ftp._tcp.local.",            # FTP servers
    "_daap._tcp.local.",           # iTunes music sharing
    "_spotify-connect._tcp.local.", # Spotify Connect
    "_googlecast._tcp.local.",     # Google Cast (Chromecast)
    "_companion-link._tcp.local.", # Apple TV/HomePod
    "_sleep-proxy._udp.local.",    # Sleep Proxy
    "_device-info._tcp.local.",    # Device info
    "_workstation._tcp.local.",    # Workstations
    "_rdp._tcp.local.",            # Remote Desktop
    "_vnc._tcp.local.",            # VNC
    "_rfb._tcp.local.",            # VNC (alternative)
]


class DeviceInfo:
    """Container for discovered device information."""
    
    def __init__(self, name: str, service_type: str, address: str, port: int, properties: Dict):
        self.name = name
        self.service_type = service_type
        self.address = address
        self.port = port
        self.properties = properties
        self.discovered_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export."""
        return {
            'name': self.name,
            'service_type': self.service_type,
            'address': self.address,
            'port': self.port,
            'properties': self.properties,
            'discovered_at': self.discovered_at.isoformat()
        }


class MDNSListener(ServiceListener):
    """Custom listener for mDNS service discovery."""
    
    def __init__(self, verbose: bool = False):
        self.devices: List[DeviceInfo] = []
        self.verbose = verbose
        self.service_names: Set[str] = set()
    
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is discovered."""
        if name in self.service_names:
            return
        
        self.service_names.add(name)
        
        if self.verbose:
            print(f"  → Discovering: {name}", end='\r')
        
        info = zc.get_service_info(type_, name)
        
        if info:
            addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
            properties = {}
            
            if info.properties:
                for key, value in info.properties.items():
                    try:
                        properties[key.decode('utf-8')] = value.decode('utf-8')
                    except:
                        properties[key.decode('utf-8')] = str(value)
            
            for address in addresses:
                device = DeviceInfo(
                    name=info.server.rstrip('.'),
                    service_type=type_,
                    address=address,
                    port=info.port,
                    properties=properties
                )
                self.devices.append(device)
                
                if self.verbose:
                    print(f"  ✓ Found: {device.name} at {address}:{device.port}           ")
    
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is updated."""
        pass
    
    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is removed."""
        pass


class MDNSScanner:
    """mDNS network scanner."""
    
    def __init__(self, timeout: int = 5, services: List[str] = None, verbose: bool = False):
        self.timeout = timeout
        self.services = services or COMMON_SERVICES
        self.verbose = verbose
        self.listener = MDNSListener(verbose=verbose)
    
    def print_banner(self):
        """Print ASCII art banner."""
        print(BANNER)
        print(f"⏱  Scan timeout: {self.timeout}s")
        print(f"🔍 Services to scan: {len(self.services)}")
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
    
    def scan(self) -> List[DeviceInfo]:
        """Perform mDNS scan."""
        print("🔎 Scanning network for mDNS/Bonjour devices...\n")
        
        zeroconf = Zeroconf()
        browsers = []
        
        try:
            # Start browsers for each service type
            for service in self.services:
                browser = ServiceBrowser(zeroconf, service, self.listener)
                browsers.append(browser)
            
            # Wait for scan to complete
            if self.verbose:
                for i in range(self.timeout):
                    print(f"  Scanning... {i+1}/{self.timeout}s", end='\r')
                    time.sleep(1)
                print()
            else:
                # Show spinner
                spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
                start = time.time()
                i = 0
                while time.time() - start < self.timeout:
                    print(f"  {spinner[i % len(spinner)]} Scanning... ({len(self.listener.devices)} devices found)", end='\r')
                    time.sleep(0.1)
                    i += 1
                print()
            
        finally:
            zeroconf.close()
        
        return self.listener.devices
    
    def print_results(self, devices: List[DeviceInfo]):
        """Print scan results in a nice table format."""
        print()
        print("=" * 70)
        print(f"📊 Scan Results: {len(devices)} device(s) discovered")
        print("=" * 70)
        print()
        
        if not devices:
            print("  No devices found. Try increasing timeout with --timeout")
            print()
            return
        
        # Group devices by hostname
        by_host = {}
        for device in devices:
            if device.name not in by_host:
                by_host[device.name] = []
            by_host[device.name].append(device)
        
        # Print each host and its services
        for i, (hostname, host_devices) in enumerate(sorted(by_host.items()), 1):
            print(f"┌─ Device #{i}: {hostname}")
            
            # Get unique addresses
            addresses = list(set(d.address for d in host_devices))
            print(f"│  📍 IP: {', '.join(addresses)}")
            
            # List services
            print(f"│  🔌 Services:")
            for device in host_devices:
                service_name = device.service_type.replace('._tcp.local.', '').replace('._udp.local.', '').lstrip('_')
                print(f"│     • {service_name:<20} → {device.address}:{device.port}")
                
                # Show properties if any
                if device.properties:
                    for key, value in list(device.properties.items())[:3]:  # Show first 3 props
                        print(f"│       - {key}: {value}")
            
            print("│")
        
        print("=" * 70)
    
    def export_json(self, devices: List[DeviceInfo]) -> str:
        """Export results as JSON."""
        return json.dumps(
            {
                'scan_time': datetime.now().isoformat(),
                'timeout': self.timeout,
                'devices_found': len(devices),
                'devices': [d.to_dict() for d in devices]
            },
            indent=2
        )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='mdns-scan - Elegant mDNS/Bonjour network scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mdns-scan.py                              Scan with default settings
  mdns-scan.py --timeout 10                 Scan for 10 seconds
  mdns-scan.py --services _http._tcp        Scan only for HTTP services
  mdns-scan.py --json > results.json        Export to JSON
  mdns-scan.py --verbose                    Show detailed progress

Common service types:
  _http._tcp, _https._tcp, _ssh._tcp, _printer._tcp,
  _airplay._tcp, _homekit._tcp, _googlecast._tcp

For more information: https://github.com/cosm00/mdns-scan
        """
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=5,
        metavar='N',
        help='Scan timeout in seconds (default: 5)'
    )
    
    parser.add_argument(
        '--services',
        type=str,
        metavar='SERVICE1,SERVICE2',
        help='Comma-separated list of services to scan (e.g., _http._tcp.local.,_ssh._tcp.local.)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Hide ASCII art banner'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed scanning progress'
    )
    
    args = parser.parse_args()
    
    # Parse services if provided
    services = None
    if args.services:
        services = [s.strip() for s in args.services.split(',')]
        # Ensure proper format
        services = [s if s.endswith('.local.') else f"{s}.local." for s in services]
    
    try:
        scanner = MDNSScanner(
            timeout=args.timeout,
            services=services,
            verbose=args.verbose
        )
        
        if not args.no_banner and not args.json:
            scanner.print_banner()
        
        devices = scanner.scan()
        
        if args.json:
            print(scanner.export_json(devices))
        else:
            scanner.print_results(devices)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user.")
        sys.exit(1)
    except ImportError:
        print("\n❌ Error: 'zeroconf' library not installed.")
        print("\nInstall it with:")
        print("  pip3 install zeroconf")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during scan: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
