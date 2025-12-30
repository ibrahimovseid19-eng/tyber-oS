import time
import random
import threading

class MetasploitSession:
    def __init__(self, shell):
        self.shell = shell
        self.state = "main" # main, module_selected
        self.current_module = None
        self.target_ip = None
        
        # ASCII Art Banner
        banner = """
      .:okOOOkdc'           'cdkOOOko:.
    .xOOOOOOOOOOOOc       cOOOOOOOOOOOOx.
   :OOOOOOOOOOOOOOOk,   ,kOOOOOOOOOOOOOOO:
  'OOOOOOOOOkkkkOOOOO: :OOOOOOOOOOOOOOOOOO'
  oOOOOOOOO.    .oOOOOoOOOOl.    ,OOOOOOOOo
  dOOOOOOOO.      .cOOOOOc.      ,OOOOOOOOx
  lOOOOOOOO.         ;d;         ,OOOOOOOOl
  .OOOOOOOO.         .;.         ,OOOOOOOO.
   cOOOOOOO.                     ,OOOOOOOc
    oOOOOOO.                     ,OOOOOOo
     lOOOOO.                     ,OOOOOl
      ;OOOO'                     ,OOOO;
       .dOOo                     ,OOd.
         .lc                     ,l.
        """
        self.print(banner, "blue")
        self.print("       =[ metasploit v6.3.4-dev ]", "white")
        self.print("+ -- --=[ 2345 exploits - 1230 auxiliary - 421 post ]", "white")
        self.print("+ -- --=[ 986 payloads - 46 encoders - 11 nops      ]", "white")
        self.print(" ", "white")
        self.print("Tip: Type 'search <term>' to find modules.", "grey")

    def get_prompt(self):
        if self.state == "meterpreter":
            return "meterpreter > "
        if self.current_module:
            return f"msf6 exploit({self.current_module.split('/')[-1]}) > "
        return "msf6 > "

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def handle_input(self, cmd):
        response = []
        cmd = cmd.strip()
        parts = cmd.split()
        base_cmd = parts[0].lower() if parts else ""
        
        # Handle Meterpreter State
        if self.state == "meterpreter":
            if base_cmd == "exit" or base_cmd == "background":
                 self.state = "module_selected"
                 self.print("[*] Backgrounding session 1...", "cyan")
                 return []
            else:
                 self.run_meterpreter_cmd(base_cmd)
                 return []
        
        # Command Handling
        if base_cmd == "exit":
            self.shell.active_session = None
            return [{"text": "Exiting Metasploit...", "color": "yellow"}]
            return [{"text": "Exiting Metasploit...", "color": "yellow"}]
            
        elif base_cmd == "help":
            self.print("Core Commands", "cyan")
            self.print("=============", "cyan")
            self.print("    Command       Description", "white")
            self.print("    -------       -----------", "white")
            self.print("    search        Search for modules (e.g., 'search windows')", "white")
            self.print("    use           Select a module by name", "white")
            self.print("    set           Set a variable (e.g., 'set RHOSTS 10.0.0.1')", "white")
            self.print("    exploit       Launch the exploit", "white")
            self.print("    exit          Exit the console", "white")

        elif base_cmd == "search":
            if len(parts) < 2:
                self.print("Usage: search <term>", "red")
            else:
                term = parts[1]
                self.print(f"Matching Modules for '{term}'", "cyan")
                self.print("================================", "cyan")
                self.print("   #  Name                                   Disclosure Date  Rank    Check  Description", "white")
                self.print("   -  ----                                   ---------------  ----    -----  -----------", "white")
                
                # Mock Results
                results = [
                    f"exploit/windows/smb/{term}_overflow",
                    f"exploit/{term}/remote_code_exec",
                    f"auxiliary/scanner/{term}/version",
                    f"exploit/multi/{term}/handler"
                ]
                
                for i, res in enumerate(results):
                     self.print(f"   {i}  {res:<38} 2024-05-12       excellent  Yes    {term.capitalize()} Exploit Logic", "green")
                     
        elif base_cmd == "use":
             if len(parts) < 2:
                 self.print("Usage: use <module_name>", "red")
             else:
                 self.current_module = parts[1]
                 self.state = "module_selected"
                 
                 # Hacky way to update prompt in UI (since UI handles prompt internally usually, 
                 # but TerminalWidget sends 'root@teybr' prompt. 
                 # We can simulate the prompt by printing it here for next line? 
                 # Actually, TerminalWidget might not support custom dynamic prompts easily.
                 # We will simulate prompt by just printing confirmation.)
                 self.print(f"[*] Using configured module: {self.current_module}", "red")
                 self.print(f"payload => windows/meterpreter/reverse_tcp", "grey")

        elif base_cmd == "set":
             if len(parts) < 3:
                 self.print("Usage: set <OPTION> <VALUE>", "red")
             else:
                 opt = parts[1].upper()
                 val = parts[2]
                 if opt == "RHOSTS" or opt == "RHOST":
                     self.target_ip = val
                 self.print(f"{opt} => {val}", "cyan")

        elif base_cmd == "exploit" or base_cmd == "run":
             if not self.current_module:
                 self.print("[-] No module selected. Use 'use <module>' first.", "red")
             elif not self.target_ip:
                 self.print("[-] RHOSTS not set. Use 'set RHOSTS <ip>' first.", "red")
             else:
                 self.run_exploit_sim()

        else:
            self.print(f"Unknown command: {base_cmd}", "red")

        return []

    def run_exploit_sim(self):
        # Simulation of exploitation
        self.print(f"[*] Started reverse TCP handler on 192.168.1.105:4444", "cyan")
        self.print(f"[*] {self.target_ip}:80 - Connecting to target...", "cyan")
        time.sleep(1)
        self.print(f"[*] {self.target_ip}:80 - Sending stage (179779 bytes) to {self.target_ip}", "cyan")
        time.sleep(1.5)
        
        # Always succeed for demo purposes
        self.print(f"[+] {self.target_ip}:445 - Exploiting SMB...", "green")
        time.sleep(1)
        self.print(f"[+] {self.target_ip}:445 - Targeted successfully!", "green")
        time.sleep(0.5)
        self.print(f"[*] Meterpreter session 1 opened (192.168.1.105:4444 -> {self.target_ip}:49215)", "white")
        
        # Change prompt logic to meterpreter
        self.state = "meterpreter"
        self.print("meterpreter > ", "white")
        self.print("(Interactive shell active. Type 'sysinfo', 'shell', or 'exit')", "grey")

    def run_meterpreter_cmd(self, cmd):
        if cmd == "sysinfo":
            self.print("Computer        : TARGET-PC", "white")
            self.print("OS              : Windows 10 (10.0 Build 19041)", "white")
            self.print("Architecture    : x64", "white")
            self.print("System Language : en_US", "white")
            self.print("Meterpreter     : x64/windows", "white")
        elif cmd == "shell":
            self.print("Process 3421 created.", "white")
            self.print("Channel 1 created.", "white")
            self.print("Microsoft Windows [Version 10.0.19041.1]", "white")
            self.print("(c) 2020 Microsoft Corporation. All rights reserved.", "white")
            self.print("", "white")
            self.print("C:\\Windows\\system32>", "white")
        else:
            self.print(f"Unknown command: {cmd}", "red")


def register(shell):
    def start_msf(args):
        session = MetasploitSession(shell)
        shell.active_session = session
        return []
    
    shell.register_command("msfconsole", start_msf)
    shell.register_command("msf", start_msf)
