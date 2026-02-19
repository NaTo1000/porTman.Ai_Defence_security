# porTman.Ai Defence Security

A comprehensive network security application that functions as a packet distribution port manager with advanced attack detection, honeypot redirection, and silent line routing capabilities.

## Features

### 1. Packet Distribution Port Manager
- Monitors multiple network ports simultaneously
- Tracks incoming connections in real-time
- Distributes traffic handling across multiple threads

### 2. Attack Detection & Alerting System
The application identifies various types of attacks including:
- **Port Scanning**: Detects rapid connection attempts across multiple ports
- **Brute Force Attacks**: Identifies repeated failed authentication attempts
- **DDoS Attacks**: Recognizes abnormal connection rates

### 3. Honeypot with Recursive Room of Mirrors
When an attack is detected, the system:
- Redirects attackers into a "recursive room of mirrors"
- Creates multiple layers of redirects to confuse and delay attackers
- Generates unique mirror paths for each attacker
- Keeps attackers trapped in redirect loops

### 4. Silent Line Routing
After the honeypot cycle completes:
- Attackers are silently redirected to legitimate websites (Google, Bing, Wikipedia, GitHub)
- This handoff appears seamless to the attacker
- Protects the actual system while maintaining the illusion of access

### 5. Attack Logging & Database
All detected attacks are:
- Logged with timestamp, IP address, attack type, and port
- Stored in a JSON database (`attack_log.json`)
- Available for future analysis and public download
- Used to build security definition files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NaTo1000/porTman.Ai_Defence_security.git
cd porTman.Ai_Defence_security
```

2. No external dependencies required (uses Python standard library)

## Usage

### Basic Usage

Run the application with Python 3.7+:

```bash
python3 portman_ai.py
```

For production use with privileged ports (80, 443, etc.), run with sudo:

```bash
sudo python3 portman_ai.py
```

### Configuration

Edit `config.json` to customize:

```json
{
  "monitored_ports": [8080, 8443, 9090],
  "enable_honeypot": true,
  "enable_silent_redirect": true,
  "log_attacks": true,
  ...
}
```

Configuration options:
- `monitored_ports`: List of ports to monitor
- `enable_honeypot`: Enable/disable honeypot redirection
- `enable_silent_redirect`: Enable/disable silent line routing
- `log_attacks`: Enable/disable attack logging
- `attack_detection`: Thresholds for different attack types
- `honeypot.max_redirect_depth`: Number of mirror redirects
- `silent_line.legitimate_sites`: List of sites for final redirect

## How It Works

### Attack Detection Flow

1. **Connection Monitoring**: Application listens on configured ports
2. **Pattern Analysis**: Tracks connection frequency and patterns
3. **Threat Detection**: Identifies suspicious behavior based on thresholds
4. **Classification**: Categorizes attack type (port scan, brute force, DDoS)

### Honeypot Response Flow

1. **Attack Detected**: System identifies malicious connection
2. **Mirror Generation**: Creates unique mirror path for attacker
3. **Recursive Redirects**: Sends attacker through multiple redirect levels
4. **Silent Handoff**: Final redirect to legitimate site (Google, etc.)
5. **Attack Logging**: Records full attack details to database

### Example Attack Response

```
Connection from 192.168.1.100 → Port 8080
↓
Port scan detected (10 connections in 5 seconds)
↓
Generate mirror path: 192_168_1_100_1645123456_7890
↓
Redirect Level 1 → /mirror/1/redirect
Redirect Level 2 → /mirror/2/redirect
Redirect Level 3 → /mirror/3/redirect
Redirect Level 4 → /mirror/4/redirect
Redirect Level 5 → /mirror/5/redirect
↓
Silent line handoff → https://www.google.com
↓
Attack logged to database
```

## Output Files

### attack_log.json
Database of all detected attacks:
```json
[
  {
    "timestamp": "2026-02-19T13:20:15.123456",
    "ip_address": "192.168.1.100",
    "attack_type": "port_scan",
    "port": 8080,
    "details": {"source_port": 54321},
    "action_taken": "honeypot_redirect"
  }
]
```

### portman_ai.log
Detailed application logs:
```
2026-02-19 13:20:15 - porTman.Ai - INFO - porTman.Ai Defence Security started
2026-02-19 13:20:15 - porTman.Ai - INFO - Monitoring ports: [8080, 8443, 9090]
2026-02-19 13:20:16 - porTman.Ai - WARNING - Port scan detected from 192.168.1.100
2026-02-19 13:20:16 - porTman.Ai - INFO - Generated mirror path for 192.168.1.100
2026-02-19 13:20:16 - porTman.Ai - INFO - Silent line redirect to https://www.google.com
```

## Security Definitions

The attack database serves as a growing repository of:
- Attack patterns and signatures
- Malicious IP addresses
- Attack techniques and methodologies
- Response effectiveness data

This data can be:
- Exported for public download
- Shared with security communities
- Used to improve detection algorithms
- Integrated into other security tools

## Testing

To test the system:

1. Start the application:
```bash
python3 portman_ai.py
```

2. In another terminal, simulate connections:
```bash
# Single connection test
curl http://localhost:8080

# Simulate port scan (rapid connections)
for i in {1..15}; do curl http://localhost:8080 & done
```

3. Check the logs and attack database

## Future Enhancements

- Web dashboard for real-time monitoring
- Integration with WiFi Pineapple Nano/Tetra
- Advanced ML-based attack detection
- API for external security tools
- Automated threat intelligence sharing

## License

Open source security tool for defensive purposes only.

## Warning

This tool is for legitimate security testing and defense only. Unauthorized use against systems you don't own or have permission to test is illegal.
