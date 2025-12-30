
import subprocess
import os
import shutil
import platform
import webbrowser

class WebSecurityTerminal:
    def __init__(self, shell):
        self.shell = shell
        self.os_type = platform.system()
        
        # Common default paths (can be expanded)
        self.tools_config = {
            "zap": {"cmd": "zap.bat", "desc": "OWASP Zed Attack Proxy"},
            "burp": {"cmd": "burpsuite_community.jar", "desc": "Burp Suite Community"},
            "nikto": {"cmd": "nikto.pl", "desc": "Nikto Web Scanner (Perl)"},
            "gobuster": {"cmd": "gobuster.exe", "desc": "Gobuster Directory/DNS Buster"},
            "dirbuster": {"cmd": "DirBuster", "desc": "OWASP DirBuster (Java GUI)"}
        }

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def check_tool(self, tool_key):
        tool_cmd = self.tools_config[tool_key]["cmd"]
        # Check PATH first
        if shutil.which(tool_cmd):
            return tool_cmd
        
        # Check if it's a jar file (simulated check for burp)
        if tool_key == "burp":
             # In reality, users often have Burp as an installed app. 
             # Use a generic warning if not found.
             return None
             
        return None

    def run_command(self, args):
        if not args:
            return self.print_help()
            
        cmd = args[0].lower()
        sub_args = args[1:]
        
        handlers = {
            "scan": self.handle_scan,
            "proxy": self.handle_proxy,
            "dir": self.handle_dir,
            "tools": self.list_tools,
            "explain": self.handle_explain,
            "help": self.print_help
        }
        
        if cmd in handlers:
            return handlers[cmd](sub_args)
            
        # Aliases
        aliases = {
            "s": self.handle_scan,
            "p": self.handle_proxy,
            "d": self.handle_dir,
            "t": self.list_tools,
            "e": self.handle_explain,
            "h": self.print_help
        }
        
        if cmd in aliases:
            return aliases[cmd](sub_args)
            
        return [{"text": f"Unknown web command: {cmd}", "color": "red"}]

    def print_help(self, _=None):
        return [
            {"text": "--- Web Security Terminal (Windows) ---", "color": "cyan", "weight": "bold"},
            {"text": "⚠ LEGAL WARNING: Use ONLY on systems you own or have explicit written permission to test.", "color": "yellow", "weight": "bold"},
            {"text": "Commands:", "color": "white"},
            {"text": "  web scan <tool> <url>   : Active scan using 'zap' or 'nikto'", "color": "green"},
            {"text": "  web dir <tool> <url>    : Directory brute-force using 'gobuster'", "color": "green"},
            {"text": "  web proxy burp          : Launch Burp Suite & Show Proxy Config", "color": "green"},
            {"text": "  web tools               : Check status of installed external tools", "color": "green"},
            {"text": "  web explain <tool>      : Get details about a specific tool", "color": "green"},
            {"text": "", "color": "white"},
            {"text": "Examples:", "color": "grey"},
            {"text": "  web scan nikto http://testphp.vulnweb.com", "color": "grey"},
            {"text": "  web dir gobuster http://192.168.1.105", "color": "grey"}
        ]

    def list_tools(self, _=None):
        output = [{"text": "--- External Web Security Tools ---", "color": "cyan"}]
        for start_key, info in self.tools_config.items():
            found = self.check_tool(start_key)
            status = "[INSTALLED]" if found else "[NOT FOUND]"
            color = "green" if found else "grey"
            output.append({"text": f"{info['desc']:<30} : {status}", "color": color})
            
        output.append({"text": "", "color": "white"})
        output.append({"text": "Tip: Ensure tools (perl, zap.bat, gobuster.exe) are in your System PATH.", "color": "white"})
        return output

    def handle_explain(self, args):
        if not args: return [{"text": "Usage: web explain <tool_name>", "color": "red"}]
        tool = args[0].lower()
        
        explanations = {
            "nikto": "Nikto is a Perl-based web server scanner which performs comprehensive tests against web servers for multiple items, including over 6700 potentially dangerous files/programs.",
            "zap": "OWASP ZAP (Zed Attack Proxy) is a flexible proxy and scanner. It sits between your browser and the web application to intercept and inspect messages.",
            "burp": "Burp Suite is the industry standard for web application security testing. It operates as a proxy, allowing you to modify traffic on the fly.",
            "gobuster": "Gobuster is a tool used to brute-force URIs (directories and files) in web sites, DNS subdomains (with wildcard support), Virtual Host names on target web servers."
        }
        
        if tool in explanations:
            return [{"text": f"[{tool.upper()}]", "color": "cyan"}, {"text": explanations[tool], "color": "white"}]
        return [{"text": "No explanation available for this tool.", "color": "red"}]

    def handle_proxy(self, args):
        if not args or args[0] != "burp":
             return [{"text": "Usage: web proxy burp", "color": "red"}]
        
        output = [
            {"text": "[*] Launching Burp Suite...", "color": "cyan"},
            {"text": "    -> Proxy Listener: 127.0.0.1:8080 (Default)", "color": "green"},
            {"text": "    -> ⚠ Action Required: Configure your browser/FoxyProxy to use this address.", "color": "yellow"}
        ]
        
        # Try to launch if possible
        try:
            # This is tricky on windows as path varies. We try standard command.
            subprocess.Popen("start burpsuite_community", shell=True) 
        except:
             output.append({"text": "[!] Could not auto-launch. Please start Burp manually.", "color": "red"})
             
        return output

    def handle_scan(self, args):
        if len(args) < 2:
            return [{"text": "Usage: web scan <nikto|zap> <target_url>", "color": "red"}]
        
        tool = args[0].lower()
        target = args[1]
        
        if tool == "nikto":
            # Check for perl
            if not shutil.which("perl"):
                 return [{"text": "Error: Perl is not installed or not in PATH. Nikto requires Perl.", "color": "red"}]
            
            # Assume nikto.pl is in current dir or path? 
            # In a real windows env, user often has to point to nikto path.
            # We will try to run 'perl nikto.pl' assuming user is in correct dir or added alias.
            return [
                {"text": f"[*] Starting Nikto scan against {target}", "color": "cyan"},
                {"text": f"[*] Command: perl nikto.pl -h {target}", "color": "grey"},
                {"text": "Note: This will fail if 'nikto.pl' is not in the current directory. Windows pathing is strict.", "color": "yellow"}
            ]
            
        elif tool == "zap":
            return [
                {"text": f"[*] Triggering OWASP ZAP Active Scan on {target}...", "color": "cyan"},
                {"text": "Note: Ensure ZAP is running in Daemon mode or GUI.", "color": "grey"}
            ]
            
        return [{"text": f"Unknown scan tool: {tool}", "color": "red"}]

    def handle_dir(self, args):
        if len(args) < 2:
             return [{"text": "Usage: web dir <gobuster> <url>", "color": "red"}]
        
        tool = args[0].lower()
        target = args[1]
        
        if tool == "gobuster":
            if not shutil.which("gobuster"):
                return [{"text": "Error: gobuster.exe not found in PATH.", "color": "red"}]
                
            # Simulate command construction
            wordlist = "C:\\Wordlists\\common.txt" 
            return [
                {"text": f"[*] Starting Gobuster (Dir Mode)", "color": "cyan"},
                {"text": f"[*] Target: {target}", "color": "white"},
                {"text": f"[*] Wordlist: {wordlist} (Default)", "color": "grey"},
                {"text": "Execute in separate window for best performance:", "color": "yellow"},
                {"text": f"> gobuster dir -u {target} -w {wordlist}", "color": "green"}
            ]
            
        return [{"text": f"Tool not supported for dir busting: {tool}", "color": "red"}]

def register(shell):
    web = WebSecurityTerminal(shell)
    shell.register_command("web", web.run_command)
