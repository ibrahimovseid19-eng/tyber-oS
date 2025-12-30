import time
import threading

class PkgInstaller:
    def __init__(self, shell):
        self.shell = shell

    def install(self, url):
        self.print(f"[*] Cloning into 'nmap'...", "white")
        time.sleep(1)
        self.print(f"remote: Enumerating objects: 4521, done.", "grey")
        self.print(f"remote: Counting objects: 100% (4521/4521), done.", "grey")
        self.print(f"remote: Compressing objects: 100% (1230/1230), done.", "grey")
        self.print(f"Receiving objects: 100% (4521/4521), 15.42 MiB | 2.40 MiB/s, done.", "white")
        self.print(f"Resolving deltas: 100% (2890/2890), done.", "grey")
        
        time.sleep(1)
        self.print(f"[*] Checking build system...", "cyan")
        time.sleep(1)
        self.print(f"[*] Running ./configure...", "cyan")
        
        # Fake configure output
        cfg_lines = [
            "checking for gcc... gcc",
            "checking whether the C compiler works... yes",
            "checking for C compiler default output file name... a.out",
            "checking for library containing strerror... none required",
            "checking for inline... inline",
            "checking for flexible array members... yes",
        ]
        for line in cfg_lines:
            self.print(f"    {line}", "grey")
            time.sleep(0.1)

        self.print(f"[*] Analysis complete. Ready to compile.", "green")
        self.print(f"[*] Running 'make' (this may take a while)...", "cyan")
        
        # Fake make output
        make_lines = [
            "gcc -c -I. -g -O2 -Wall -fno-strict-aliasing main.cc -o main.o",
            "gcc -c -I. -g -O2 -Wall -fno-strict-aliasing nmap.cc -o nmap.o",
            "gcc -c -I. -g -O2 -Wall -fno-strict-aliasing targets.cc -o targets.o",
            "gcc -c -I. -g -O2 -Wall -fno-strict-aliasing tcpip.cc -o tcpip.o",
            "ar rc libnmap.a main.o nmap.o targets.o tcpip.o",
            "ranlib libnmap.a",
            "Linking nmap executable...",
        ]
        
        for line in make_lines:
            self.print(f"    {line}", "grey")
            time.sleep(0.3)
            
        self.print(f"[*] Running 'make install'...", "cyan")
        time.sleep(1)
        self.print(f"/usr/bin/install -c -m 755 nmap /usr/local/bin/nmap", "grey")
        self.print(f"/usr/bin/install -c -m 644 docs/nmap.1 /usr/local/man/man1/nmap.1", "grey")
        
        time.sleep(1)
        self.print(f"[+] Nmap installation successful!", "green")
        self.print(f"[*] Integration with Teybr OS kernel complete.", "green")
        self.print(f"[*] Type 'nmap <target>' to scan.", "white")

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

def register(shell):
    def install_cmd(args):
        if not args:
            return [{"text": "Usage: install <github_url>", "color": "red"}]
        
        url = args[0]
        installer = PkgInstaller(shell)
        
        if "nmap" in url:
            # Run simulation thread
            t = threading.Thread(target=installer.install, args=(url,))
            t.start()
            return [{"text": f"Starting installation from {url}...", "color": "cyan"}]
        else:
            return [{"text": "Currently only Nmap repository is supported for auto-build simulation.", "color": "yellow"}]

    shell.register_command("install", install_cmd)
    shell.register_command("pkg", install_cmd)
