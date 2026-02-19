#!/usr/bin/env python3
"""
porTman.Ai Defence Security
Main application for packet monitoring, attack detection, and honeypot redirection
"""

import socket
import threading
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Set
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('portman_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('porTman.Ai')


class AttackDetector:
    """Detects potential security threats based on patterns and behavior"""
    
    def __init__(self):
        self.attack_patterns = {
            'port_scan': {'rapid_connections': 10, 'time_window': 5},
            'brute_force': {'failed_attempts': 5, 'time_window': 10},
            'ddos': {'connection_rate': 50, 'time_window': 1}
        }
        self.connection_tracker: Dict[str, List[float]] = {}
        self.blocked_ips: Set[str] = set()
        
    def track_connection(self, ip_address: str, port: int) -> bool:
        """Track connection and detect suspicious patterns"""
        current_time = time.time()
        
        if ip_address not in self.connection_tracker:
            self.connection_tracker[ip_address] = []
        
        # Clean old entries
        self.connection_tracker[ip_address] = [
            t for t in self.connection_tracker[ip_address] 
            if current_time - t < 60
        ]
        
        self.connection_tracker[ip_address].append(current_time)
        
        # Detect port scanning
        recent_connections = len([
            t for t in self.connection_tracker[ip_address]
            if current_time - t < self.attack_patterns['port_scan']['time_window']
        ])
        
        if recent_connections > self.attack_patterns['port_scan']['rapid_connections']:
            logger.warning(f"Port scan detected from {ip_address}")
            self.blocked_ips.add(ip_address)
            return True
        
        return False
    
    def is_blocked(self, ip_address: str) -> bool:
        """Check if IP is blocked"""
        return ip_address in self.blocked_ips


class HoneypotMirror:
    """Implements recursive room of mirrors for attackers"""
    
    def __init__(self):
        self.mirror_paths = []
        self.redirect_depth = 0
        self.max_depth = 5
        
    def generate_mirror_path(self, attacker_ip: str) -> str:
        """Generate a unique mirror path for attacker"""
        timestamp = int(time.time())
        random_id = random.randint(1000, 9999)
        mirror_id = f"{attacker_ip.replace('.', '_')}_{timestamp}_{random_id}"
        
        self.mirror_paths.append(mirror_id)
        logger.info(f"Generated mirror path {mirror_id} for {attacker_ip}")
        
        return mirror_id
    
    def get_recursive_redirect(self, depth: int) -> str:
        """Create recursive redirects to confuse attackers"""
        if depth >= self.max_depth:
            return self.get_silent_line_redirect()
        
        # Create a loop that redirects to itself with increasing depth
        redirect_url = f"/mirror/{depth + 1}/redirect"
        logger.info(f"Redirecting to mirror level {depth + 1}")
        
        return redirect_url
    
    def get_silent_line_redirect(self) -> str:
        """Final redirect to legitimate site (silent line handoff)"""
        legitimate_sites = [
            "https://www.google.com",
            "https://www.bing.com",
            "https://www.wikipedia.org",
            "https://www.github.com"
        ]
        selected = random.choice(legitimate_sites)
        logger.info(f"Silent line redirect to {selected}")
        return selected


class AttackLogger:
    """Logs attacks to database and generates reports"""
    
    def __init__(self, db_file: str = 'attack_log.json'):
        self.db_file = db_file
        self.attacks = []
        self.load_database()
    
    def load_database(self):
        """Load existing attack database"""
        try:
            with open(self.db_file, 'r') as f:
                self.attacks = json.load(f)
            logger.info(f"Loaded {len(self.attacks)} attack records")
        except FileNotFoundError:
            self.attacks = []
            logger.info("Created new attack database")
    
    def log_attack(self, attack_data: Dict):
        """Log an attack to the database"""
        attack_record = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': attack_data.get('ip_address'),
            'attack_type': attack_data.get('attack_type'),
            'port': attack_data.get('port'),
            'details': attack_data.get('details', {}),
            'action_taken': attack_data.get('action_taken')
        }
        
        self.attacks.append(attack_record)
        self.save_database()
        
        logger.info(f"Logged attack: {attack_record['attack_type']} from {attack_record['ip_address']}")
    
    def save_database(self):
        """Save attack database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.attacks, f, indent=2)
    
    def get_attack_statistics(self) -> Dict:
        """Generate attack statistics"""
        stats = {
            'total_attacks': len(self.attacks),
            'attack_types': {},
            'top_attackers': {}
        }
        
        for attack in self.attacks:
            attack_type = attack.get('attack_type', 'unknown')
            stats['attack_types'][attack_type] = stats['attack_types'].get(attack_type, 0) + 1
            
            ip = attack.get('ip_address', 'unknown')
            stats['top_attackers'][ip] = stats['top_attackers'].get(ip, 0) + 1
        
        return stats


class PortManager:
    """Main port manager that monitors network traffic"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.detector = AttackDetector()
        self.honeypot = HoneypotMirror()
        self.attack_logger = AttackLogger()
        self.monitored_ports = config.get('monitored_ports', [80, 443, 22, 21])
        # Bind address - use '0.0.0.0' for monitoring all interfaces (security tool requirement)
        # Can be restricted to specific interface (e.g., '127.0.0.1') in production if needed
        self.bind_address = config.get('bind_address', '0.0.0.0')
        self.running = False
        
    def start(self):
        """Start the port manager"""
        self.running = True
        logger.info("porTman.Ai Defence Security started")
        logger.info(f"Monitoring ports: {self.monitored_ports}")
        
        # Start monitoring threads for each port
        threads = []
        for port in self.monitored_ports:
            thread = threading.Thread(target=self.monitor_port, args=(port,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down porTman.Ai")
            self.stop()
    
    def stop(self):
        """Stop the port manager"""
        self.running = False
        logger.info("porTman.Ai stopped")
        
        # Print statistics
        stats = self.attack_logger.get_attack_statistics()
        logger.info(f"Session statistics: {json.dumps(stats, indent=2)}")
    
    def monitor_port(self, port: int):
        """Monitor a specific port for connections"""
        logger.info(f"Starting monitor on port {port}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Intentionally binds to all interfaces for network monitoring
            # This is required for a security monitoring tool to detect attacks from any source
            # Configure bind_address in config.json to restrict if needed (e.g., '127.0.0.1')
            sock.bind((self.bind_address, port))
            sock.listen(5)
            sock.settimeout(1.0)
            
            while self.running:
                try:
                    client_socket, address = sock.accept()
                    threading.Thread(
                        target=self.handle_connection,
                        args=(client_socket, address, port)
                    ).start()
                except socket.timeout:
                    continue
                    
        except PermissionError:
            logger.error(f"Permission denied to bind port {port}. Run with elevated privileges.")
        except OSError as e:
            logger.error(f"Error binding port {port}: {e}")
        finally:
            sock.close()
    
    def handle_connection(self, client_socket, address, port):
        """Handle incoming connection"""
        ip_address = address[0]
        logger.info(f"Connection from {ip_address}:{address[1]} to port {port}")
        
        # Check if attack detected
        is_attack = self.detector.track_connection(ip_address, port)
        
        if is_attack or self.detector.is_blocked(ip_address):
            # Log the attack
            self.attack_logger.log_attack({
                'ip_address': ip_address,
                'attack_type': 'port_scan',
                'port': port,
                'details': {'source_port': address[1]},
                'action_taken': 'honeypot_redirect'
            })
            
            # Send to honeypot (room of mirrors)
            self.honeypot_response(client_socket, ip_address)
        else:
            # Normal connection - could forward or respond
            self.normal_response(client_socket, port)
        
        client_socket.close()
    
    def honeypot_response(self, client_socket, ip_address: str):
        """Send honeypot response to suspected attacker"""
        mirror_path = self.honeypot.generate_mirror_path(ip_address)
        
        # Start recursive mirror redirects
        response = "HTTP/1.1 302 Found\r\n"
        redirect_url = self.honeypot.get_recursive_redirect(0)
        response += f"Location: {redirect_url}\r\n"
        response += "Content-Type: text/html\r\n"
        response += "\r\n"
        response += f"<html><body><h1>Redirecting...</h1></body></html>"
        
        try:
            client_socket.sendall(response.encode())
            logger.info(f"Sent honeypot response to {ip_address}")
        except Exception as e:
            logger.error(f"Error sending honeypot response: {e}")
    
    def normal_response(self, client_socket, port: int):
        """Send normal response for legitimate traffic"""
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += "\r\n"
        response += "<html><body><h1>porTman.Ai Defence Security Active</h1></body></html>"
        
        try:
            client_socket.sendall(response.encode())
        except Exception as e:
            logger.error(f"Error sending response: {e}")


def main():
    """Main entry point"""
    # Load configuration
    config = {
        'monitored_ports': [8080, 8443],  # Use non-privileged ports for testing
        'bind_address': '0.0.0.0',  # Bind to all interfaces (required for network monitoring)
        'enable_honeypot': True,
        'enable_silent_redirect': True,
        'log_attacks': True
    }
    
    logger.info("=" * 60)
    logger.info("porTman.Ai Defence Security System")
    logger.info("Packet Distribution Port Manager with Attack Detection")
    logger.info("=" * 60)
    
    # Create and start port manager
    port_manager = PortManager(config)
    port_manager.start()


if __name__ == '__main__':
    main()
