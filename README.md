# porTman.Ai Defence Security

A comprehensive network security application that functions as a packet distribution port manager with advanced attack detection, honeypot redirection, and silent line routing capabilities.

## Overview

porTman.Ai Defence Security is an intelligent alert and detection application that:
- **Acts as a packet distribution port manager** - Monitors and manages network traffic across multiple ports
- **Doubles as a security system** - Detects various types of attacks (port scans, brute force, DDoS)
- **Implements recursive "room of mirrors"** - Traps attackers in honeypot redirect loops
- **Uses silent line routing** - Seamlessly hands off attackers to legitimate sites (Google, etc.)
- **Logs attacks to database** - Creates security definitions for future protection and public download

## Key Features

### 1. Real-time Attack Detection
- Port scanning detection
- Brute force attempt identification
- DDoS pattern recognition
- IP blocking and tracking

### 2. Honeypot System with Recursive Mirrors
When attacks are detected:
- Generates unique mirror paths for each attacker
- Creates up to 5 levels of recursive redirects
- Confuses and delays attackers in redirect loops
- Logs all honeypot interactions

### 3. Silent Line Handoff
After honeypot cycles:
- Redirects attackers to legitimate websites
- Maintains illusion of successful access
- Protects actual system resources
- Seamless handoff to Google, Bing, Wikipedia, GitHub

### 4. Attack Database & Definitions
- All attacks logged with timestamps and details
- JSON database for easy access and sharing
- Can be published for public download
- Builds security definition files for future protection

## Quick Start

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses standard library)

### Installation

```bash
git clone https://github.com/NaTo1000/porTman.Ai_Defence_security.git
cd porTman.Ai_Defence_security
```

### Running the Application

```bash
# For testing (non-privileged ports)
python3 portman_ai.py

# For production (requires sudo for ports 80, 443, etc.)
sudo python3 portman_ai.py
```

### Testing

Run the test suite to verify functionality:

```bash
python3 test_portman.py
```

### Configuration

Edit `config.json` to customize settings:

```json
{
  "monitored_ports": [8080, 8443, 9090],
  "enable_honeypot": true,
  "enable_silent_redirect": true,
  "log_attacks": true,
  ...
}
```

## How It Works

### Attack Flow

1. **Monitor** → Application listens on configured ports
2. **Detect** → Identifies suspicious patterns (rapid connections, etc.)
3. **Classify** → Determines attack type (port scan, brute force, DDoS)
4. **Respond** → Redirects to honeypot or handles normally
5. **Log** → Records attack details to database

### Honeypot Response

```
Attacker → Port 8080
    ↓
Port Scan Detected
    ↓
Mirror Path: 192_168_1_100_1645123456_7890
    ↓
Redirect 1 → /mirror/1/redirect
Redirect 2 → /mirror/2/redirect
Redirect 3 → /mirror/3/redirect
Redirect 4 → /mirror/4/redirect
Redirect 5 → /mirror/5/redirect
    ↓
Silent Line → https://www.google.com
    ↓
Attack Logged
```

## Output Files

- **attack_log.json** - Database of all detected attacks
- **portman_ai.log** - Detailed application logs

## Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed information including:
- Complete feature descriptions
- Configuration options
- Advanced usage examples
- Security definitions
- Future enhancements

## Future Integration

Planned enhancements:
- WiFi Pineapple Nano/Tetra control panel integration
- Live database website for public downloads
- Advanced warning system
- Automated threat intelligence sharing

## Security Notice

This tool is designed for legitimate security testing and defense purposes only. Unauthorized use against systems you don't own or have permission to test is illegal.

## License

Open source security tool for defensive purposes.

## Contributing

Contributions welcome! This project aims to build a comprehensive defense security application with shared threat intelligence.
