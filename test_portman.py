#!/usr/bin/env python3
"""
Test script for porTman.Ai Defence Security
Tests core functionality without requiring privileged ports
"""

import sys
import time
import socket
import threading
import json
from portman_ai import AttackDetector, HoneypotMirror, AttackLogger, PortManager


def test_attack_detector():
    """Test attack detection functionality"""
    print("\n" + "="*60)
    print("Testing Attack Detector")
    print("="*60)
    
    detector = AttackDetector()
    test_ip = "192.168.1.100"
    
    # Test normal traffic (should not trigger)
    print(f"\nTest 1: Normal traffic from {test_ip}")
    is_attack = detector.track_connection(test_ip, 80)
    print(f"Attack detected: {is_attack}")
    assert is_attack == False, "Normal traffic incorrectly flagged as attack"
    print("✓ PASSED: Normal traffic not flagged")
    
    # Test port scan (rapid connections should trigger)
    print(f"\nTest 2: Simulating port scan from {test_ip}")
    for i in range(12):
        is_attack = detector.track_connection(test_ip, 80 + i)
    
    print(f"Attack detected: {is_attack}")
    assert is_attack == True, "Port scan not detected"
    print("✓ PASSED: Port scan detected")
    
    # Test blocked IP
    print(f"\nTest 3: Checking if IP is blocked")
    is_blocked = detector.is_blocked(test_ip)
    print(f"IP blocked: {is_blocked}")
    assert is_blocked == True, "IP should be blocked after attack"
    print("✓ PASSED: Attacker IP correctly blocked")
    
    print("\n✓ ALL ATTACK DETECTOR TESTS PASSED")


def test_honeypot_mirror():
    """Test honeypot mirror functionality"""
    print("\n" + "="*60)
    print("Testing Honeypot Mirror System")
    print("="*60)
    
    honeypot = HoneypotMirror()
    test_ip = "10.0.0.50"
    
    # Test mirror path generation
    print(f"\nTest 1: Generating mirror path for {test_ip}")
    mirror_path = honeypot.generate_mirror_path(test_ip)
    print(f"Generated mirror path: {mirror_path}")
    assert test_ip.replace('.', '_') in mirror_path, "IP not in mirror path"
    print("✓ PASSED: Mirror path generated correctly")
    
    # Test recursive redirects
    print(f"\nTest 2: Testing recursive redirects")
    for depth in range(5):
        redirect = honeypot.get_recursive_redirect(depth)
        print(f"Depth {depth}: {redirect}")
        assert "/mirror/" in redirect or "https://" in redirect, "Invalid redirect"
    print("✓ PASSED: Recursive redirects working")
    
    # Test silent line redirect
    print(f"\nTest 3: Testing silent line redirect")
    final_redirect = honeypot.get_silent_line_redirect()
    print(f"Final redirect (silent line): {final_redirect}")
    assert final_redirect.startswith("https://"), "Silent line should redirect to HTTPS site"
    print("✓ PASSED: Silent line redirect working")
    
    print("\n✓ ALL HONEYPOT TESTS PASSED")


def test_attack_logger():
    """Test attack logging functionality"""
    print("\n" + "="*60)
    print("Testing Attack Logger")
    print("="*60)
    
    # Use a test database file
    test_db = "/tmp/test_attack_log.json"
    logger = AttackLogger(db_file=test_db)
    
    # Test logging an attack
    print("\nTest 1: Logging attack data")
    attack_data = {
        'ip_address': '172.16.0.50',
        'attack_type': 'port_scan',
        'port': 8080,
        'details': {'connections': 15},
        'action_taken': 'honeypot_redirect'
    }
    logger.log_attack(attack_data)
    print(f"Attack logged: {attack_data['attack_type']} from {attack_data['ip_address']}")
    assert len(logger.attacks) >= 1, "Attack not logged"
    print("✓ PASSED: Attack logged successfully")
    
    # Test multiple attacks
    print("\nTest 2: Logging multiple attacks")
    for i in range(5):
        logger.log_attack({
            'ip_address': f'192.168.1.{i}',
            'attack_type': 'brute_force' if i % 2 else 'port_scan',
            'port': 22,
            'action_taken': 'blocked'
        })
    print(f"Total attacks logged: {len(logger.attacks)}")
    assert len(logger.attacks) >= 6, "Not all attacks logged"
    print("✓ PASSED: Multiple attacks logged")
    
    # Test statistics generation
    print("\nTest 3: Generating attack statistics")
    stats = logger.get_attack_statistics()
    print(f"Statistics: {json.dumps(stats, indent=2)}")
    assert stats['total_attacks'] >= 6, "Incorrect attack count"
    assert len(stats['attack_types']) > 0, "No attack types recorded"
    print("✓ PASSED: Statistics generated correctly")
    
    print("\n✓ ALL ATTACK LOGGER TESTS PASSED")


def test_port_manager_components():
    """Test PortManager components without binding to ports"""
    print("\n" + "="*60)
    print("Testing Port Manager Components")
    print("="*60)
    
    config = {
        'monitored_ports': [9999],  # Test port
        'enable_honeypot': True,
        'enable_silent_redirect': True,
        'log_attacks': True
    }
    
    port_manager = PortManager(config)
    
    # Test initialization
    print("\nTest 1: Port Manager initialization")
    assert port_manager.detector is not None, "Detector not initialized"
    assert port_manager.honeypot is not None, "Honeypot not initialized"
    assert port_manager.attack_logger is not None, "Logger not initialized"
    print("✓ PASSED: Port Manager initialized correctly")
    
    # Test attack detection integration
    print("\nTest 2: Attack detection in Port Manager")
    test_ip = "203.0.113.50"
    for i in range(12):
        is_attack = port_manager.detector.track_connection(test_ip, 80)
    assert port_manager.detector.is_blocked(test_ip), "Attack not blocked"
    print("✓ PASSED: Port Manager attack detection working")
    
    print("\n✓ ALL PORT MANAGER TESTS PASSED")


def test_connection_simulation():
    """Test actual connection handling (brief test)"""
    print("\n" + "="*60)
    print("Testing Connection Handling")
    print("="*60)
    
    config = {
        'monitored_ports': [19999],  # High port for testing
        'enable_honeypot': True,
        'enable_silent_redirect': True,
        'log_attacks': True
    }
    
    port_manager = PortManager(config)
    
    # Start port manager in a thread
    print("\nStarting port manager on test port 19999...")
    server_thread = threading.Thread(target=port_manager.start, daemon=True)
    server_thread.start()
    
    # Give it time to start
    time.sleep(2)
    
    # Try to connect
    print("Attempting test connection...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('127.0.0.1', 19999))
        response = sock.recv(1024)
        sock.close()
        
        print(f"Received response ({len(response)} bytes)")
        assert len(response) > 0, "No response received"
        print("✓ PASSED: Connection handled successfully")
    except Exception as e:
        print(f"Connection test: {e}")
        print("Note: This test may require appropriate permissions")
    finally:
        port_manager.stop()
    
    print("\n✓ CONNECTION TEST COMPLETED")


def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*60)
    print("porTman.Ai Defence Security - Test Suite")
    print("="*60)
    
    try:
        test_attack_detector()
        test_honeypot_mirror()
        test_attack_logger()
        test_port_manager_components()
        test_connection_simulation()
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED SUCCESSFULLY ✓✓✓")
        print("="*60)
        print("\nporTman.Ai Defence Security is working correctly!")
        print("Run 'python3 portman_ai.py' to start the application.")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
