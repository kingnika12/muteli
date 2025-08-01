#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import threading
import time
import random
import json
import sys
from colorama import Fore, Style, init

init(autoreset=True)

class DiscordMassSpammer:
    def __init__(self):
        self.tokens = []
        self.channel_id = ""
        self.message = ""
        self.sent = 0
        self.errors = 0
        self.running = True
        self.proxies = None
        self.delay = 0.01
        self.max_threads = 50
        self.message_count = 0

    def get_input(self):
        print(Fore.YELLOW + r"""
   ____  _  _  ____  ____  ____  ____     ____  ____  ____  ____  ____  ____ 
  (  _ \( \/ )(  _ \( ___)(  _ \(  _ \   (  _ \( ___)(  _ \( ___)(  _ \( ___)
   )   / )  (  ) _ < )__)  )   / )(_) )   ) _ < )__)  )   / )__)  )   / )__) 
  (_)\_)(_/\_)(____/(____)(_)\_)(____/   (____/(____)(_)\_)(____)(_)\_)(____)
        """)
        print(Fore.CYAN + "\nNUKE SPAMMER v3.0 - MULTI-ACCOUNT MASS MESSENGER\n")

        # Get multiple tokens
        while len(self.tokens) < 2:
            token = input(Fore.WHITE + f"[?] Enter User Token {len(self.tokens)+1} (or leave blank if done): ").strip()
            if token:
                self.tokens.append(token)
            elif len(self.tokens) < 2:
                print(Fore.RED + "[!] You need at least 2 tokens for nuke spamming!")
            else:
                break

        self.channel_id = input(Fore.WHITE + "[?] Enter Target Channel ID: ").strip()
        self.message = input(Fore.WHITE + "[?] Enter Spam Message: ").strip()
        self.message_count = int(input(Fore.WHITE + "[?] Enter Number of Messages per Account: ").strip() or "100")

    def send_message(self, token, message_num):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI2MTYxOCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }

        payload = {
            "content": f"{self.message} | {message_num+1}/{self.message_count}",
            "tts": False,
            "nonce": str(random.randint(100000000000000000, 999999999999999999))
        }

        try:
            session = requests.Session()
            r = session.post(
                f"https://discord.com/api/v9/channels/{self.channel_id}/messages",
                json=payload,
                headers=headers,
                proxies=self.proxies,
                timeout=10
            )

            if r.status_code == 200:
                with threading.Lock():
                    self.sent += 1
                    print(Fore.GREEN + f"[✓] {token[:15]}... sent message {message_num+1}/{self.message_count} (Total: {self.sent})")
            elif r.status_code == 429:
                retry_after = r.json().get('retry_after', random.uniform(0.1, 0.5))
                time.sleep(retry_after)
                return self.send_message(token, message_num)  # Retry
            else:
                with threading.Lock():
                    self.errors += 1
                    print(Fore.RED + f"[✗] Error {r.status_code} on {token[:15]}...")
                    if r.status_code in [401, 403]:
                        try:
                            self.tokens.remove(token)
                        except ValueError:
                            pass

        except Exception as e:
            with threading.Lock():
                self.errors += 1
                print(Fore.RED + f"[!] Exception on {token[:15]}...: {str(e)}")

    def start_spamming(self):
        print(Fore.RED + "\n[!] NUKE SPAMMING INITIATED! (Ctrl+C to STOP)\n")
        print(Fore.CYAN + f"[!] Using {len(self.tokens)} tokens | Messages per account: {self.message_count}\n")

        try:
            threads = []
            for token in self.tokens:
                for i in range(self.message_count):
                    if not self.running:
                        break
                    while threading.active_count() > self.max_threads:
                        time.sleep(0.1)
                    t = threading.Thread(target=self.send_message, args=(token, i))
                    t.start()
                    threads.append(t)
                    time.sleep(self.delay)

            for t in threads:
                t.join()

        except KeyboardInterrupt:
            self.running = False
            print(Fore.RED + "\n[!] NUKE STOPPED BY USER!")

        print(Fore.CYAN + f"\n[RESULTS] Sent: {self.sent} | Errors: {self.errors}")
        print(Fore.YELLOW + f"[!] Remaining active tokens: {len(self.tokens)}")

    def run(self):
        self.get_input()
        self.start_spamming()

if __name__ == "__main__":
    spammer = DiscordMassSpammer()
    spammer.run()