import random
import time
import socket

def register(shell):
    shell.register_command("netmon", cmd_netmon)
    shell.register_command("scan", cmd_scan)

def cmd_netmon(args):
    """
    Simulates a live network traffic monitor.
    In a real scenario, this would interface with a packet sniffer.
    Here strictly for simulation/educational purposes in Teybr OS.
    """
    output = []
    
    # Get local IP simulation
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "192.168.1.5"

    output.append({"text": f"[*] Initializing promiscuous mode on interface eth0 ({local_ip})...", "color": "yellow"})
    output.append({"text": "[*] Capture started. Filtering: ALL", "color": "cyan"})
    
    protocols = ["TCP", "UDP", "HTTP", "HTTPS", "ICMP", "ARP"]
    external_ips = [
        "104.21.55.2", "172.67.132.89", "142.250.185.78", "157.240.22.35",
        "40.114.177.156", "13.107.42.12", "192.168.1.1", "192.168.1.102"
    ]
    
    # Simulate a batch of traffic
    for i in range(15):
        proto = random.choice(protocols)
        src = local_ip if random.random() > 0.5 else random.choice(external_ips)
        dst = random.choice(external_ips) if src == local_ip else local_ip
        port = random.choice([80, 443, 22, 53, 445, 8080])
        length = random.randint(40, 1500)
        
        color = "white"
        if proto == "HTTP" or proto == "HTTPS": color = "green"
        elif proto == "TCP": color = "blue"
        elif proto == "ICMP" or proto == "ARP": color = "grey"
        elif proto == "UDP": color = "orange" # Orange might not be valid in standard logic, defaulting to white usually
        
        # Adjust color for Flet
        if color == "orange": color = "amber"

        output.append({
            "text": f"[{time.strftime('%H:%M:%S')}] {proto:<5} {src}:{random.randint(1024, 65535)} -> {dst}:{port}  Len={length}",
            "color": color
        })
        
    output.append({"text": "[!] Capture stopped. Buffer full.", "color": "red"})
    return output

def cmd_scan(args):
    """
    REAL Port Scanner using python socket.
    Usage: scan <ip>
    Note: Threaded to be faster, but kept simple here.
    """
    target = args.strip()
    if not target:
        return [{"text": "Usage: scan <ip> (e.g. scan 192.168.1.1)", "color": "red"}]
    
    output = []
    output.append({"text": f"[*] Starting REAL port scan on {target}...", "color": "blue"})
    output.append({"text": f"[*] Scanning common ports (21, 22, 80, 443, 3306, 8080)...", "color": "grey"})

    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8080, 8000]
    
    open_ports = []
    
    # We use a simple loop. For a real app, use threading/asyncio to avoid UI freeze.
    # Since this is a demo, we will set a very short timeout.
    
    try:
        start_time = time.time()
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5) # 500ms timeout per port
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                # output.append({"text": f"[+] Port {port}/tcp OPEN", "color": "green"}) # If we want real-time logging
            sock.close()
        
        duration = round(time.time() - start_time, 2)
        
        if open_ports:
            for p in open_ports:
                service = "UNKNOWN"
                if p == 80: service = "HTTP"
                elif p == 443: service = "HTTPS"
                elif p == 22: service = "SSH"
                elif p == 21: service = "FTP"
                elif p == 3306: service = "MYSQL"
                
                output.append({"text": f"[+] {target}:{p} ({service}) is OPEN", "color": "green", "weight": "bold"})
        else:
             output.append({"text": f"[-] No open common ports found on {target}.", "color": "orange"})
             
        output.append({"text": f"[*] Scan completed in {duration}s", "color": "blue"})
        
    except Exception as e:
        output.append({"text": f"[!] Scan Error: {e}", "color": "red"})

    return output
