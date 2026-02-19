#!/usr/bin/env python3
"""
Demonstration script for porTman.Ai Defence Security
Shows how the system detects and responds to attacks
"""

import socket
import time
import threading


def demonstrate_attack_detection():
    """Demonstrate attack detection and honeypot response"""
    print("\n" + "="*70)
    print("porTman.Ai Defence Security - DEMONSTRATION")
    print("="*70)
    
    print("\nThis demonstration shows how porTman.Ai works:")
    print("1. Monitors network ports for connections")
    print("2. Detects suspicious patterns (port scans, etc.)")
    print("3. Redirects attackers to honeypot 'room of mirrors'")
    print("4. Performs silent line handoff to legitimate sites")
    print("5. Logs all attacks to database")
    
    print("\n" + "-"*70)
    print("SCENARIO: Simulating a Port Scan Attack")
    print("-"*70)
    
    from portman_ai import AttackDetector, HoneypotMirror, AttackLogger
    
    # Initialize components
    detector = AttackDetector()
    honeypot = HoneypotMirror()
    logger = AttackLogger(db_file="/tmp/demo_attack_log.json")
    
    attacker_ip = "203.0.113.100"  # Example IP from TEST-NET-3
    
    print(f"\n[1] Attacker {attacker_ip} begins scanning ports...")
    time.sleep(0.5)
    
    # Simulate normal connection first
    print(f"\n[2] Connection 1 to port 80 - Normal traffic")
    detector.track_connection(attacker_ip, 80)
    print("    → No attack detected")
    time.sleep(0.3)
    
    # Simulate rapid connections (port scan)
    print(f"\n[3] Rapid connections detected (Port Scan in progress):")
    for i in range(2, 13):
        port = 80 + i
        is_attack = detector.track_connection(attacker_ip, port)
        print(f"    Connection {i} to port {port}...", end=" ")
        time.sleep(0.1)
        
        if is_attack:
            print("⚠️  ATTACK DETECTED!")
            break
        else:
            print("✓")
    
    print(f"\n[4] Attack identified: PORT SCAN")
    print(f"    IP {attacker_ip} has been flagged as malicious")
    
    # Generate honeypot response
    print(f"\n[5] Activating Honeypot Defense...")
    mirror_path = honeypot.generate_mirror_path(attacker_ip)
    print(f"    → Generated unique mirror path: {mirror_path}")
    
    print(f"\n[6] Recursive Room of Mirrors activated:")
    for depth in range(5):
        redirect = honeypot.get_recursive_redirect(depth)
        print(f"    Level {depth + 1}: {redirect}")
        time.sleep(0.2)
    
    print(f"\n[7] Maximum depth reached - Activating Silent Line...")
    final_redirect = honeypot.get_silent_line_redirect()
    print(f"    → Silent handoff to: {final_redirect}")
    print(f"    → Attacker thinks they succeeded but is redirected away")
    
    # Log the attack
    print(f"\n[8] Logging attack to database...")
    logger.log_attack({
        'ip_address': attacker_ip,
        'attack_type': 'port_scan',
        'port': 80,
        'details': {
            'connections': 12,
            'time_span': '5 seconds',
            'mirror_path': mirror_path
        },
        'action_taken': 'honeypot_redirect_with_silent_line'
    })
    print(f"    ✓ Attack logged successfully")
    
    # Show statistics
    print(f"\n[9] Attack Statistics:")
    stats = logger.get_attack_statistics()
    print(f"    Total Attacks Logged: {stats['total_attacks']}")
    print(f"    Attack Types: {stats['attack_types']}")
    print(f"    Top Attackers: {stats['top_attackers']}")
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    
    print("\n📊 Result Summary:")
    print(f"   • Attack detected and classified")
    print(f"   • Attacker trapped in recursive honeypot")
    print(f"   • Silent redirect to legitimate site performed")
    print(f"   • Full attack details logged to database")
    print(f"   • System remains protected and operational")
    
    print("\n💡 What happens in production:")
    print("   1. Real attackers are similarly detected and redirected")
    print("   2. Attack patterns are logged for analysis")
    print("   3. Database can be shared publicly as threat intelligence")
    print("   4. Future attacks from same IPs are automatically blocked")
    print("   5. System learns and adapts to new attack patterns")
    
    print("\n🚀 To run the full application:")
    print("   python3 portman_ai.py")
    
    print("\n🧪 To run the test suite:")
    print("   python3 test_portman.py")
    
    print("\n📖 For more information:")
    print("   See DOCUMENTATION.md for complete details")
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    demonstrate_attack_detection()
