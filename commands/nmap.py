import time
import random
import threading

class NmapSession:
    def __init__(self, shell):
        self.shell = shell
        self.print("Starting Nmap 7.94 ( https://nmap.org ) at " + time.strftime("%Y-%m-%d %H:%M %Z"), "white")

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def handle_input(self, cmd):
        # Nmap is usually a one-shot command tool, not a session. 
        # But simulation requires interactive feel or just running args.
        # If integrated as "nmap <args>", this session might just run and exit.
        return []

    def run_scan(self, target):
        self.print(f"Nmap scan report for {target}", "white")
        self.print(f"Host is up ({random.uniform(0.001, 0.05):.4f}s latency).", "white")
        self.print("Not shown: 998 closed ports", "grey")
        self.print("PORT     STATE SERVICE VERSION", "white")
        
        ports = [
            ("21/tcp", "open", "ftp", "vsftpd 3.0.3"),
            ("22/tcp", "open", "ssh", "OpenSSH 8.2p1 Ubuntu"),
            ("80/tcp", "open", "http", "Apache httpd 2.4.41"),
            ("443/tcp", "open", "ssl/http", "Apache/2.4.41"),
            ("3306/tcp", "open", "mysql", "MySQL 8.0.21"),
            ("8080/tcp", "open", "http-proxy", "Nginx"),
        ]
        
        # Randomize selection
        selected = random.sample(ports, k=random.randint(2, 5))
        selected.sort(key=lambda x: int(x[0].split('/')[0]))
        
        for port, state, service, version in selected:
            self.print(f"{port:<8} {state:<5} {service:<7} {version}", "green")
            
        self.print("", "white")
        self.print("Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .", "grey")
        self.print(f"Nmap done: 1 IP address (1 host up) scanned in {random.uniform(1.5, 4.0):.2f} seconds", "white")


def register(shell):
    def nmap_cmd(args):
        # Usage: nmap <target>
        target = "127.0.0.1"
        if len(args) > 0:
            target = args[0]
        
        session = NmapSession(shell)
        
        # Simulate scan delay
        shell.print_callback(f"Starting Nmap 7.94 ( https://nmap.org ) at {time.strftime('%Y-%m-%d %H:%M')}", "white")
        
        # We need to run this in a thread or async to avoid blocking UI if we want delays.
        # But shell.execute expects return.
        # We'll return a generator/list of simulated output with small delays?
        # Or better, launch a thread to simply stream output to callback.
        
        def run_async():
            session.run_scan(target)
            
        t = threading.Thread(target=run_async)
        t.start()
        
        return []

    shell.register_command("nmap", nmap_cmd)