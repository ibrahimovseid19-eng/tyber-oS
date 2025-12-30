
import urllib.request
import urllib.error
import threading
import time

class DirBuster:
    def __init__(self, shell):
        self.shell = shell
        self.common_paths = [
            "admin", "login", "robots.txt", "dashboard", "config",
            "backup", "images", "static", "css", "js", "api",
            "uploads", "secret", "test", "wp-admin", "wp-login.php",
            "shell.php", "db.sql", ".env", "server-status"
        ]
        self.found = []
        self.lock = threading.Lock()
        self.running = False

    def print(self, text, color="white"):
        if hasattr(self.shell, 'print_callback') and self.shell.print_callback:
             self.shell.print_callback(text, color)

    def check_path(self, base_url, path):
        if not self.running: return
        
        url = f"{base_url}/{path}"
        try:
            # Use HEAD request for speed if possible, effectively checks existence
            req = urllib.request.Request(url, method="HEAD")
            # Set a generic user agent
            req.add_header('User-Agent', 'Mozilla/5.0 (TeybrOS)')
            
            with urllib.request.urlopen(req, timeout=3) as response:
                code = response.getcode()
                if code in [200, 301, 302, 403]:
                    with self.lock:
                        status_color = "green" if code == 200 else "yellow"
                        if code == 403: status_color = "red"
                        
                        self.print(f"[+] Found: /{path:<15} (Status: {code})", status_color)
                        self.found.append((path, code))
        except urllib.error.HTTPError as e:
            if e.code in [403]:
                with self.lock:
                     self.print(f"[!] Forbidden: /{path:<12} (Status: {e.code})", "red")
            # 404 is ignored
        except Exception:
            pass

    def run(self, url):
        self.running = True
        self.found = []
        
        if not url.startswith("http"):
            url = "http://" + url
            
        self.print(f"[*] Starting DirBust on {url}", "cyan")
        self.print(f"[*] Wordlist size: {len(self.common_paths)} paths", "grey")
        self.print("-" * 40, "grey")
        
        threads = []
        for path in self.common_paths:
            if not self.running: break
            t = threading.Thread(target=self.check_path, args=(url, path))
            threads.append(t)
            t.start()
            # Stagger slightly
            time.sleep(0.05)
            
        for t in threads:
            t.join()
            
        self.running = False
        self.print("-" * 40, "grey")
        self.print(f"[*] Scan Complete. Found {len(self.found)} paths.", "white")

def register(shell):
    def cmd_dirbust(args):
        # usage: dirbust <url>
        if not args:
            return [{"text": "Usage: dirbust <url>\nExample: dirbust google.com", "color": "yellow"}]
        
        url = args.split()[0]
        buster = DirBuster(shell)
        
        # Run in thread
        def run_thread():
            buster.run(url)
            
        t = threading.Thread(target=run_thread)
        t.start()
        
        return [{"text": f"Initializing Directory Buster against {url}...", "color": "cyan"}]

    shell.register_command("dirbust", cmd_dirbust)
