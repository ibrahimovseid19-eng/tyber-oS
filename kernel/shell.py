import subprocess
import os
import platform
import shutil
import urllib.request
import tarfile
import zipfile
import re

class Shell:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.print_callback = None
        self.active_session = None
        # Setup git directory
        self.git_dir = os.path.join(os.getcwd(), "git")
        if not os.path.exists(self.git_dir):
            os.makedirs(self.git_dir)

        self.commands = {
            "cd": self.cmd_cd,
            "cls": self.cmd_clear,
            "clear": self.cmd_clear,
            "mobile-mode": self.cmd_mobile_mode,
            "exit": self.cmd_exit,
            "wget": self.cmd_wget,
            "unzip": self.cmd_unzip,
            "tar": self.cmd_tar,
            "git": self.cmd_git,
            "backup": self.cmd_backup
        }
        self._load_plugins()

    # ... (rest of methods)

    def cmd_backup(self, args):
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_name = f"TeybrOS_Backup_{timestamp}.zip"
            base_dir = os.getcwd()
            
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(base_dir):
                    # Smart Exclude: Dont backup virtual envs, git history, or other backups
                    dirs[:] = [d for d in dirs if d not in ['.venv', '.git', '__pycache__', 'git', 'node_modules']]
                    
                    for file in files:
                        if file.startswith("TeybrOS_Backup"): continue
                        if file.endswith(".zip"): continue
                        
                        file_path = os.path.join(root, file)
                        arcname = os.path.join("TeybrOS", os.path.relpath(file_path, base_dir))
                        zipf.write(file_path, arcname)
            
            return [{"text": f"[+] Full System Backup Complete: {zip_name}", "color": "green", "weight": "bold"}]
        except Exception as e:
            return [{"text": f"[-] Backup failed: {e}", "color": "red"}]

    def register_command(self, name, func):
        self.commands[name] = func

    def _load_plugins(self):
        # Dynamically load command modules
        try:
            import commands.social_engineering as social
            social.register(self)
        except ImportError:
            pass

        try:
            import commands.network_monitor as netmon
            netmon.register(self)
        except ImportError:
            pass

        try:
            import commands.advanced_security as advsec
            advsec.register(self)
        except ImportError:
            pass

        try:
            import commands.nmap as real_nmap
            real_nmap.register(self)
        except ImportError:
            pass

        try:
            import commands.sqlmap as real_sqlmap
            real_sqlmap.register(self)
        except ImportError:
            pass

        try:
            import commands.gecon as gecon
            gecon.register(self)
        except ImportError:
            pass

        try:
            import commands.ptm4 as ptm4
            ptm4.register(self)
        except ImportError:
            pass

        try:
            import commands.shark as shark
            shark.register(self)
        except ImportError:
            pass

        try:
            import commands.metasploit as msf
            msf.register(self)
        except ImportError:
            pass

        try:
            import commands.pkg_manager as pkg
            pkg.register(self)
        except ImportError:
            pass

        try:
            import commands.netscan as netscan
            netscan.register(self)
        except ImportError:
            pass

        try:
            import commands.hot as hot
            hot.register(self)
        except ImportError:
            pass

        try:
            import commands.dirbust as dirbust
            dirbust.register(self)
        except ImportError:
            pass

        try:
             import commands.hot as hot
             hot.register(self)
        except ImportError:
             pass

        try:
            import commands.wifi_tools as wifi_tools
            wifi_tools.register(self)
        except ImportError:
            pass

        try:
            import commands.web_security as web_sec
            web_sec.register(self)
        except ImportError:
            pass

    def execute(self, command_str):
        if not command_str.strip():
            return []
            
        # Handle Active Session (Sub-shell)
        if hasattr(self, 'active_session') and self.active_session:
            if command_str.strip().lower() == "exit":
                self.active_session = None
                return [{"text": "Exiting session...", "color": "yellow"}]
            
            if hasattr(self.active_session, 'handle_input'):
                return self.active_session.handle_input(command_str)
            else:
                self.active_session = None
                return [{"text": "Session error: Handler missing. Terminating session.", "color": "red"}]

        parts = command_str.strip().split(" ", 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # 0. Smart Execution & Navigation Logic
        
        # A. Check if user typed a REPO NAME (Folder in ./git/)
        # Behavior: Auto-cd into that git repo
        potential_git_path = os.path.join(self.git_dir, cmd)
        if os.path.isdir(potential_git_path) and not cmd in self.commands:
             os.chdir(potential_git_path)
             return [{"text": f"Entering repository: {cmd}", "color": "cyan"},
                     {"text": f"path: {os.getcwd()}", "color": "grey"}]

        # B. Check if user typed a PYTHON SCRIPT name (e.g. 'tool.py' or 'tool' resolving to 'tool.py')
        # Behavior: Execute it directly
        script_args = ""
        target_script = None
        
        if os.path.isfile(cmd) and cmd.endswith(".py"):
            target_script = cmd
            script_args = args
        elif os.path.isfile(f"{cmd}.py"):
            target_script = f"{cmd}.py"
            script_args = args
            
        if target_script:
             return self.run_system_command(f"python {target_script} {script_args}")

        # 1. Handle Internal commands
        if cmd == "ls": return self.cmd_ls(args)
        if cmd in self.commands:
            return self.commands[cmd](args)

        # 2. Translate Linux -> Windows
        real_cmd = command_str
        if self.is_windows:
            real_cmd = self.translate_to_windows(cmd, args)
            
        return self.run_system_command(real_cmd)

    def cmd_git(self, args):
        if not args:
            # List cloned repos
            try:
                repos = [d for d in os.listdir(self.git_dir) if os.path.isdir(os.path.join(self.git_dir, d))]
                output = [{"text": "Cloned Repositories (in ./git/):", "color": "white", "weight": "bold"}]
                if not repos:
                     output.append({"text": "(No repositories found)", "color": "grey"})
                else:
                    for r in repos:
                        output.append({"text": f"  {r}", "color": "cyan"})
                return output
            except Exception as e:
                return [{"text": f"Error listing git dir: {e}", "color": "red"}]

        # Handle 'git clone' specially to enforce path
        if args.startswith("clone "):
             # Example: clone https://github.com/user/repo
             url = args.split()[1]
             # Run git clone inside self.git_dir with explicit CWD
             return self.run_system_command(f"git clone {url}", cwd=self.git_dir)
        
        # Pass other git commands through normally
        return self.run_system_command(f"git {args}")

    def run_system_command(self, real_cmd, cwd=None):
        """
        Executes a system command and streams the output in real-time (Generator).
        Supports long-running commands like 'npm run dev'.
        """
        try:
            process = subprocess.Popen(
                real_cmd,
                shell=True,
                cwd=cwd or os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Merge stderr into stdout
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1, # Line buffered
                universal_newlines=True
            )
            
            # Regex to strip ANSI escape codes
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            
            # Yield lines as they become available
            for line in process.stdout:
                clean_line = ansi_escape.sub('', line.strip())
                if clean_line:
                    yield {"text": clean_line, "color": "white"}
                
            process.wait()
            
            if process.returncode != 0:
                yield {"text": f"Command exited with code {process.returncode}", "color": "grey"}
                
        except Exception as e:
            yield {"text": f"Error executing command: {str(e)}", "color": "red"}

    def cmd_ls(self, args):
        try:
            path = args.strip() if args else "."
            if not os.path.exists(path):
                 return [{"text": f"ls: cannot access '{path}': No such file or directory", "color": "red"}]
            
            items = os.listdir(path)
            output = []
            
            # Sort: Directories first, then files
            dirs = []
            files = []
            
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append(item)
                else:
                    files.append(item)
            
            dirs.sort()
            files.sort()
            
            if not dirs and not files:
                return [{"text": "(empty)", "color": "grey"}]

            for d in dirs:
                output.append({"text": f"{d}/", "color": "blue", "weight": "bold"})
            
            for f in files:
                color = "white"
                if f.endswith(".py"): color = "yellow"
                elif f.endswith(".exe") or f.endswith(".bat") or f.endswith(".sh"): color = "green"
                elif f.endswith(".json") or f.endswith(".txt") or f.endswith(".md"): color = "grey"
                
                output.append({"text": f"{f}", "color": color})
                
            return output
        except Exception as e:
            return [{"text": f"ls error: {e}", "color": "red"}]

    def translate_to_windows(self, cmd, args):
        mappings = {
            "ls": "dir",
            "pwd": "echo %cd%",
            "cp": "copy",
            "mv": "move",
            "rm": "del",
            "whoami": "whoami",
            "cat": "type",
            "grep": "findstr",
            "ifconfig": "ipconfig",
            "ip": "ipconfig",
            "touch": "type nul >",
            "mkdir": "mkdir",
            "ps": "tasklist",
            "kill": "taskkill /F /PID",
            "pkg": "winget",
            "apt": "winget",
            "nano": "notepad",
            "vi": "notepad",
            "vim": "notepad",
            "python3": "python",
            "pip3": "pip"
        }
        
        if cmd in mappings:
            win_cmd = mappings[cmd]
            if args:
                return f"{win_cmd} {args}"
            return win_cmd
            
        return f"{cmd} {args}"

    def cmd_cd(self, args):
        try:
            target = args.strip()
            if not target:
                target = os.path.expanduser("~")
                
            # Priority 1: Current Path
            if os.path.isdir(target):
                 os.chdir(target)
                 return [{"text": f"Directory changed to: {os.getcwd()}", "color": "green"}]

            # Priority 2: Git Directory (Smart CD into repos)
            git_target = os.path.join(self.git_dir, target)
            if os.path.isdir(git_target):
                 os.chdir(git_target)
                 return [{"text": f"Entering Repository: {os.getcwd()}", "color": "cyan"}]

            # Priority 3: User Home Directory
            home_target = os.path.join(os.path.expanduser("~"), target)
            if os.path.isdir(home_target):
                 os.chdir(home_target)
                 return [{"text": f"Directory changed to: {os.getcwd()}", "color": "green"}]

            return [{"text": f"cd: {target}: No such directory", "color": "red"}]
        except Exception as e:
            return [{"text": f"cd error: {str(e)}", "color": "red"}]

    def cmd_wget(self, args):
        if not args:
            return [{"text": "usage: wget <url>", "color": "red"}]
        
        url = args.split()[0]
        filename = url.split("/")[-1]
        if not filename:
             filename = "downloaded_file"
             
        try:
            output = [{"text": f"Downloading {filename} from {url}...", "color": "cyan"}]
            # Real download
            urllib.request.urlretrieve(url, filename)
            output.append({"text": f"Saved: {filename}", "color": "green"})
            return output
        except Exception as e:
            return [{"text": f"wget error: {e}", "color": "red"}]

    def cmd_unzip(self, args):
        if not args:
             return [{"text": "usage: unzip <file.zip>", "color": "red"}]
        
        filename = args.split()[0]
        try:
            if not os.path.exists(filename):
                return [{"text": f"File not found: {filename}", "color": "red"}]
            
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(".")
                
            return [{"text": f"Extracted: {filename}", "color": "green"}]
        except Exception as e:
            return [{"text": f"unzip error: {e}", "color": "red"}]

    def cmd_tar(self, args):
        # args usually "-xvf file.tar"
        parts = args.split()
        filename = ""
        for p in parts:
            if not p.startswith("-"):
                filename = p
                break
        
        if not filename:
             return [{"text": "usage: tar -xvf <file>", "color": "red"}]
             
        try:
             if not os.path.exists(filename):
                return [{"text": f"File not found: {filename}", "color": "red"}]
                
             if tarfile.is_tarfile(filename):
                 with tarfile.open(filename) as tar:
                     tar.extractall()
                 return [{"text": f"Extracted: {filename}", "color": "green"}]
             else:
                 return [{"text": "Not a tar file.", "color": "red"}]
        except Exception as e:
             return [{"text": f"tar error: {e}", "color": "red"}]

    def cmd_clear(self, args):
        return [{"text": "", "action": "clear"}]

    def cmd_exit(self, args):
        return [{"text": "Session terminated.", "color": "red"}]

    def cmd_mobile_mode(self, args):
        mode = args.lower() if args else "on"
        if mode == "on":
            return [{"text": "Switching to mobile view...", "color": "cyan", "action": "resize_mobile"}]
        elif mode == "off":
             return [{"text": "Switching to desktop view...", "color": "cyan", "action": "resize_desktop"}]
        return [{"text": "Usage: mobile-mode [on|off]", "color": "red"}]
