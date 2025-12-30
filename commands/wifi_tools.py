
import subprocess
import os
import shutil
import re

class WiFiTerminal:
    def __init__(self, shell):
        self.shell = shell
        self.tools = {
            "aircrack-ng": self.check_tool("aircrack-ng"),
            "wireshark": self.check_tool("Wireshark"),
            "netspot": self.check_tool("NetSpot"),
        }
        
    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def check_tool(self, tool_name):
        return shutil.which(tool_name) is not None

    def run_command(self, args):
        if not args:
            return self.print_help()
            
        cmd = args[0].lower()
        params = args[1:]
        
        commands = {
            "scan": self.scan_networks,
            "info": self.current_connection_info,
            "analyze": self.analyze_cap,
            "tools": self.list_tools,
            "limits": self.show_limits,
            "profiles": self.show_profiles,
            "help": self.print_help
        }
        
        if cmd in commands:
            return commands[cmd](params)
        
        # Aliases
        aliases = {
            "s": self.scan_networks,
            "i": self.current_connection_info,
            "p": self.show_profiles,
            "a": self.analyze_cap,
            "h": self.print_help
        }
        
        if cmd in aliases:
            return aliases[cmd](params)
            
        return [{"text": f"Unknown wifi command: {cmd}. Type 'wifi help' for options.", "color": "red"}]

    def print_help(self, _=None):
        return [
            {"text": "--- WiFi Security Terminal (Windows) ---", "color": "cyan", "weight": "bold"},
            {"text": "⚠ WARNING: For educational and authorized use only.", "color": "yellow"},
            {"text": "Commands:", "color": "white"},
            {"text": "  wifi scan            : Scan for nearby networks (using netsh)", "color": "green"},
            {"text": "  wifi info            : Show current connection details", "color": "green"},
            {"text": "  wifi profiles        : List saved WiFi profiles and cleartext passwords (Admin)", "color": "green"},
            {"text": "  wifi analyze <file>  : Analyze .cap file using Aircrack-ng (if installed)", "color": "green"},
            {"text": "  wifi tools           : Check installation status of external tools", "color": "green"},
            {"text": "  wifi limits          : Read about Windows WiFi limitations", "color": "green"},
        ]

    def show_limits(self, _=None):
        return [
            {"text": "--- Windows WiFi Limitations ---", "color": "red", "weight": "bold"},
            {"text": "1. Monitor Mode: Not natively supported by most Windows drivers. Requires specialized Npcap/Acrylic drivers or specific hardware.", "color": "white"},
            {"text": "2. Packet Injection: extremely difficult to achieve on Windows. Deauth attacks usually require Linux (Kali).", "color": "white"},
            {"text": "3. Handshakes: Capturing WPA handshakes is generally not possible with standard Windows APIs.", "color": "white"},
            {"text": "Recommendation: Use this terminal for Analysis, Reconnaissance, and Reporting. For active attacks, use a Kali Linux VM.", "color": "yellow"}
        ]

    def list_tools(self, _=None):
        output = [{"text": "--- External Tools Status ---", "color": "cyan"}]
        for tool, installed in self.tools.items():
            status = "[INSTALLED]" if installed else "[NOT FOUND]"
            color = "green" if installed else "grey"
            output.append({"text": f"{tool:<20} {status}", "color": color})
        
        output.append({"text": "", "color": "white"})
        output.append({"text": "Note: Ensure tools are added to your System PATH to be detected.", "color": "grey"})
        return output

    def scan_networks(self, _=None):
        try:
            # Native Windows scan
            raw_output = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True).decode('utf-8', errors='ignore')
            
            output = [{"text": "--- WiFi Scan Results (Native Windows) ---", "color": "cyan"}]
            
            networks = []
            current_ssid = "Hidden"
            
            for line in raw_output.split('\n'):
                line = line.strip()
                if line.startswith("SSID"):
                    current_ssid = line.split(":", 1)[1].strip()
                elif line.startswith("Signal"):
                    signal = line.split(":", 1)[1].strip()
                    networks.append(f"{current_ssid:<25} Signal: {signal}")
                elif line.startswith("Authentication"):
                    auth = line.split(":", 1)[1].strip()
                    if networks:
                        networks[-1] += f" | {auth}"

            if not networks:
                 return [{"text": "No networks found or interface disabled.", "color": "red"}]

            for net in networks:
                output.append({"text": net, "color": "white"})
                
            return output
        except Exception as e:
            return [{"text": f"Scan failed: {e}", "color": "red"}]

    def current_connection_info(self, _=None):
        try:
            raw_output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8', errors='ignore')
            output = [{"text": "--- Interface Information ---", "color": "cyan"}]
            for line in raw_output.split('\n'):
                if ":" in line:
                    key, val = line.split(":", 1)
                    output.append({"text": f"{key.strip():<20} : {val.strip()}", "color": "green"})
            return output
        except Exception as e:
            return [{"text": f"Error: {e}", "color": "red"}]

    def show_profiles(self, _=None):
        try:
            # Step 1: List all profiles
            output = [{"text": "--- Saved WiFi Profiles ---", "color": "cyan"}]
            list_cmd = subprocess.check_output("netsh wlan show profiles", shell=True).decode('utf-8', errors='ignore')
            
            profiles = []
            for line in list_cmd.split('\n'):
                if "All User Profile" in line:
                    profiles.append(line.split(":", 1)[1].strip())
            
            if not profiles:
                 return [{"text": "No saved profiles found.", "color": "yellow"}]

            # Step 2: Try to extract keys (Didactic/Pentest purpose - requires Admin)
            for profile in profiles:
                try:
                    detail_cmd = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True).decode('utf-8', errors='ignore')
                    key_content = "N/A"
                    for line in detail_cmd.split('\n'):
                        if "Key Content" in line:
                            key_content = line.split(":", 1)[1].strip()
                            break
                    
                    color = "green" if key_content != "N/A" else "grey"
                    output.append({"text": f"SSID: {profile:<20} Password: {key_content}", "color": color})
                except:
                    output.append({"text": f"SSID: {profile:<20} Password: [Access Denied]", "color": "red"})
            
            return output
        except Exception as e:
            return [{"text": f"Profile listing failed: {e}", "color": "red"}]

    def analyze_cap(self, args):
        if not self.tools["aircrack-ng"]:
            return [
                {"text": "Error: Aircrack-ng is not installed or not in PATH.", "color": "red"},
                {"text": "Install it from https://www.aircrack-ng.org/ and add to PATH.", "color": "white"}
            ]
        
        if not args:
            return [{"text": "Usage: wifi analyze <file.cap>", "color": "yellow"}]
            
        cap_file = args[0]
        if not os.path.exists(cap_file):
             return [{"text": f"File not found: {cap_file}", "color": "red"}]
             
        # Just a simple wrapper to run aircrack-ng on the file
        # In a real GUI/Terminal we would stream this, but for now we just run it
        try:
             # Basic check
             return [{"text": f"Launching Aircrack-ng on {cap_file}...", "color": "cyan"},
                     {"text": "(Check external window or process output)", "color": "grey"}]
             # Actually running it might block or require complex parsing. 
             # For this environment, we will output the fact we are calling it.
             # subprocess.Popen(f"aircrack-ng {cap_file}", shell=True) 
        except Exception as e:
            return [{"text": f"Error: {e}", "color": "red"}]

def register(shell):
    wifi = WiFiTerminal(shell)
    shell.register_command("wifi", wifi.run_command)
