
def register(shell):
    shell.register_command("phish", cmd_phish)
    shell.register_command("brute-force", cmd_brute)

def cmd_phish(args):
    target = args[0] if args else "Generic"
    return [
       {"text": f"[*] Generating phishing page for '{target}'...", "color": "yellow"},
       {"text": " -> http://secure-login-verify.com/auth?token=x992", "color": "cyan"},
       {"text": "[!] Waiting for victim input...", "color": "grey"}
    ]

def cmd_brute(args):
    return [
        {"text": "[*] Loading password list: rockyou.txt", "color": "blue"},
        {"text": "[*] Target: 192.168.1.105 (SSH)", "color": "white"},
        {"text": "Trying root:123456... Failed", "color": "red"},
        {"text": "Trying root:password... Failed", "color": "red"},
        {"text": "Trying root:toor... [SUCCESS]", "color": "green"},
        {"text": "Access Granted.", "color": "green"}
    ]
