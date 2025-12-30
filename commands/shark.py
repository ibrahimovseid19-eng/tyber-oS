import time
import random
import threading

class SharkSession:
    def __init__(self, shell):
        self.shell = shell
        self.running = False
        self.sniffing = False
        self.thread = None
        
        self.print("TShark Network Protocol Analyzer v3.4.2 (Teybr OS Edition)", "white")
        self.print("Capturing on 'eth0'", "white")
        self.print("Filters: none", "grey")
        self.print("Type 'start' to begin capture, 'stop' to pause, 'exit' to quit.", "cyan")

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def handle_input(self, cmd):
        cmd = cmd.strip().lower()
        if cmd == "exit":
            self.stop_sniffing()
            self.shell.active_session = None
            return [{"text": "Tshark session ended.", "color": "yellow"}]
        elif cmd == "start":
            if not self.sniffing:
                self.sniffing = True
                self.thread = threading.Thread(target=self.sniff_loop)
                self.thread.daemon = True
                self.thread.start()
                return [{"text": "Capture started...", "color": "green"}]
            else:
                return [{"text": "Capture already running.", "color": "yellow"}]
        elif cmd == "stop":
            self.stop_sniffing()
            return [{"text": "Capture stopped.", "color": "red"}]
        else:
             return [{"text": f"Command not found: {cmd}", "color": "red"}]

    def stop_sniffing(self):
        self.sniffing = False
        if self.thread and self.thread.is_alive():
             pass

    def sniff_loop(self):
        protocols = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "ARP", "SSH"]
        while self.sniffing:
            try:
                # Generate fake packet
                ts = time.strftime("%H:%M:%S") + f".{random.randint(100,999)}"
                
                # Format: Time  Source  Destination  Protocol  Length  Info
                src = f"10.0.0.{random.randint(2, 254)}"
                if random.random() > 0.8: src = f"{random.randint(1, 223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                
                dst = f"10.0.0.{random.randint(2, 254)}"
                if src.startswith("10.0.0"): dst = f"{random.randint(1, 223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                
                proto = random.choice(protocols)
                length = random.randint(60, 1514)
                
                info = ""
                color = "white"
                
                if proto == "TCP":
                    flags = random.choice(["[SYN]", "[ACK]", "[SYN, ACK]", "[PSH, ACK]", "[FIN, ACK]"])
                    sport = random.randint(1024, 65535)
                    dport = random.choice([80, 443, 22, 21, 8080])
                    info = f"{sport} > {dport} {flags} Seq={random.randint(0,1000)} Win={random.randint(500,65000)} Len={random.randint(0,100)}"
                    color = "cyan"
                elif proto == "UDP":
                    info = f"Source port: {random.randint(1024, 65535)}  Destination port: {random.randint(1024, 65535)}"
                    color = "blue"
                elif proto == "HTTP":
                    method = random.choice(["GET", "POST", "HEAD"])
                    path = random.choice(["/index.html", "/api/v1/auth", "/login", "/static/style.css", "/admin"])
                    info = f"{method} {path} HTTP/1.1"
                    color = "green"
                elif proto == "DNS":
                    domain = random.choice(["google.com", "facebook.com", "teybr.os", "darkweb.onion", "nasa.gov"])
                    info = f"Standard query 0x{random.randint(1000,9999):x} A {domain}"
                    color = "yellow"
                elif proto == "ARP":
                    info = f"Who has {dst}? Tell {src}"
                    color = "orange"
                elif proto == "SSH":
                    info = "Encrypted Packet (Len=128)"
                    color = "red"
                elif proto == "HTTPS":
                     info = "TLSv1.3 Application Data"
                     color = "pink"
                
                line = f"{ts}  {src:15} -> {dst:15}  {proto:5}  {length:4}  {info}"
                self.print(line, color)
                
                time.sleep(random.uniform(0.1, 0.4))
            except Exception as e:
                self.print(f"Error in sniffer: {e}", "red")
                time.sleep(1)

def register(shell):
    def start_shark(args):
        session = SharkSession(shell)
        shell.active_session = session
        return []
    
    shell.register_command("tshark", start_shark)
    shell.register_command("shark", start_shark)
    shell.register_command("wireshark", start_shark)
