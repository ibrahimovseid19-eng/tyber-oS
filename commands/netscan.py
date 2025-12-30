
import socket
import threading
import time
from datetime import datetime

class NetScan:
    def __init__(self, shell):
        self.shell = shell
        self.target = ""
        self.ports = []
        self.open_ports = []
        self.lock = threading.Lock()

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.target, port))
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    # Try to grab banner
                    try:
                        banner = s.recv(1024).decode().strip()
                        if not banner:
                            banner = "Unknown Service"
                    except:
                        banner = "Unknown Service"
                        
                    self.print(f"[+] Port {port:<5} OPEN  {banner}", "green")
            s.close()
        except:
            pass

    def run(self, target, start_port=1, end_port=1000):
        self.target = target
        self.print(f"[*] Starting NetScan on {target} (Ports {start_port}-{end_port})...", "cyan")
        self.print(f"[*] Time: {str(datetime.now())}", "grey")
        
        start_time = time.time()
        
        threads = []
        
        for port in range(start_port, end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()
            
            # Limit thread creation rate slightly to prevent killing the system/network
            if len(threads) % 100 == 0:
                time.sleep(0.1)

        for t in threads:
            t.join()
            
        end_time = time.time()
        duration = end_time - start_time
        
        self.print("", "white")
        if not self.open_ports:
            self.print("[-] No open ports found in range.", "red")
        else:
            self.print(f"[+] Scan Complete. Found {len(self.open_ports)} open ports.", "green")
            
        self.print(f"[*] Finished in {duration:.2f} seconds.", "grey")

def register(shell):
    def cmd_netscan(args):
        # usage: netscan <ip> [start_port] [end_port]
        if not args:
            return [{"text": "Usage: netscan <target_ip> [start_port] [end_port]\nExample: netscan 192.168.1.1 1 100", "color": "yellow"}]
        
        parts = args.split()
        target = parts[0]
        start_port = 1
        end_port = 100
        
        if len(parts) > 1:
            try:
                start_port = int(parts[1])
            except:
                pass
        
        if len(parts) > 2:
            try:
                end_port = int(parts[2])
            except:
                pass

        if start_port > end_port:
            start_port, end_port = end_port, start_port

        scanner = NetScan(shell)
        
        # Run in a separate thread to not block UI
        def run_thread():
            scanner.run(target, start_port, end_port)
            
        t = threading.Thread(target=run_thread)
        t.start()
        
        return [{"text": f"NetScan started for {target}...", "color": "cyan"}]

    shell.register_command("netscan", cmd_netscan)
