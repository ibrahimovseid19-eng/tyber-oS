import random
import time

class PackageManager:
    def __init__(self):
        # Simulated repository
        self.repo = {
            "git": {"ver": "2.34.1", "desc": "Distributed version control system", "size": "15 MB", "dep": ["libcurl", "zlib"]},
            "python": {"ver": "3.11.4", "desc": "Interactive high-level object-oriented language", "size": "45 MB", "dep": ["libssl", "libffi"]},
            "clang": {"ver": "14.0.0", "desc": "C language family frontend for LLVM", "size": "120 MB", "dep": ["llvm", "libgcc"]},
            "wget": {"ver": "1.21.2", "desc": "Network utility to retrieve files from the Web", "size": "4 MB", "dep": []},
            "nano": {"ver": "6.2", "desc": "Small, friendly text editor inspired by Pico", "size": "2 MB", "dep": ["ncurses"]},
            "curl": {"ver": "7.81.0", "desc": "Command line tool for transferring data with URL syntax", "size": "6 MB", "dep": ["libssl"]},
            "nmap": {"ver": "7.92", "desc": "Network exploration tool and security / port scanner", "size": "25 MB", "dep": ["libpcap"]},
            "openssl": {"ver": "3.0.2", "desc": "Secure Sockets Layer toolkit - cryptographic utility", "size": "8 MB", "dep": []},
            "vim": {"ver": "9.0.0", "desc": "Vi IMproved - enhanced vi editor", "size": "30 MB", "dep": ["libtinfo"]},
            "htop": {"ver": "3.2.1", "desc": "Interactive process viewer", "size": "3 MB", "dep": ["ncurses"]},
            "neofetch": {"ver": "7.1.0", "desc": "CLI system information tool", "size": "0.5 MB", "dep": ["bash"]},
            "libssl": {"ver": "1.1.1", "desc": "SSL simulation lib", "size": "1 MB", "dep": []},
            "libcurl": {"ver": "7.0.0", "desc": "Curl simulation lib", "size": "1 MB", "dep": []},
            "zlib": {"ver": "1.2.11", "desc": "Compression lib", "size": "1 MB", "dep": []},
            "llvm": {"ver": "14.0", "desc": "LLVM core", "size": "50 MB", "dep": []},
            "libgcc": {"ver": "11.2.0", "desc": "GCC support lib", "size": "5 MB", "dep": []},
            "ncurses": {"ver": "6.3", "desc": "Terminal handling lib", "size": "2 MB", "dep": []},
            "libpcap": {"ver": "1.10.1", "desc": "Packet capture lib", "size": "1 MB", "dep": []},
            "bash": {"ver": "5.1.16", "desc": "GNU Bourne Again SHell", "size": "10 MB", "dep": []},
            "libtinfo": {"ver": "6.3", "desc": "Terminfo lib", "size": "1 MB", "dep": []},
            "libffi": {"ver": "3.4.2", "desc": "Foreign Function Interface lib", "size": "1 MB", "dep": []},
        }
        
        # Initial simulated installed packages
        self.installed = {
            "bash": "5.1.16",
            "ncurses": "6.3",
            "libssl": "1.1.1"
        }
        
        self.last_update = 0

    def update(self):
        # Simulate updating list
        output = [
            {"text": "Get:1 https://termux.net/stable/main aarch64 Packages [80.2 kB]", "color": "white"},
            {"text": "Get:2 https://termux.net/stable/main all Packages [12.4 kB]", "color": "white"},
            {"text": "Fetched 92.6 kB in 0s (150 kB/s)", "color": "white"},
            {"text": "Reading package lists... Done", "color": "white"}
        ]
        self.last_update = time.time()
        return output

    def upgrade(self):
        if time.time() - self.last_update > 300: # 5 min check
             return [{"text": "E: The update command has not been run lately.", "color": "red"}]
        
        output = [{"text": "Reading package lists... Done", "color": "white"},
                  {"text": "Building dependency tree... Done", "color": "white"},
                  {"text": "Calculating upgrade... Done", "color": "white"},
                  {"text": "0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.", "color": "white"}]
        return output

    def install(self, pkg_name):
        if pkg_name not in self.repo:
            return [{"text": f"E: Unable to locate package {pkg_name}", "color": "red"}]
        
        if pkg_name in self.installed:
            return [{"text": f"{pkg_name} is already the newest version ({self.repo[pkg_name]['ver']}).", "color": "white"}]

        pkg = self.repo[pkg_name]
        deps = [d for d in pkg['dep'] if d not in self.installed]
        
        output = [
            {"text": "Reading package lists... Done", "color": "white"},
            {"text": "Building dependency tree... Done", "color": "white"},
        ]
        
        if deps:
            output.append({"text": f"The following additional packages will be installed: {' '.join(deps)}", "color": "yellow"})
        
        output.append({"text": f"Suggested packages: {pkg_name}-doc", "color": "grey"})
        output.append({"text": f"The following NEW packages will be installed: {pkg_name} {' '.join(deps)}", "color": "white"})
        total_size = pkg['size'] # Simpler math than parsing "MB" string to float
        output.append({"text": f"Need to get {total_size} of archives.", "color": "white"})
        output.append({"text": "After this operation, additional disk space will be used.", "color": "white"})
        
        # Simulating download
        output.append({"text": f"Get:1 https://termux.net/stable/main {pkg_name} {pkg['ver']} [{pkg['size']}]", "color": "white"})
        for i, d in enumerate(deps, 2):
            output.append({"text": f"Get:{i} https://termux.net/stable/main {d} {self.repo.get(d, {}).get('ver', '1.0')} [1 MB]", "color": "white"})
        
        # output.append({"text": "Fetched archives in 0s.", "color": "white"})
        output.append({"text": "Selecting previously unselected package...", "color": "white"})
        
        # Install logic simulation
        for d in deps:
            self.installed[d] = self.repo[d]['ver']
        self.installed[pkg_name] = pkg['ver']
        
        output.append({"text": f"Setting up {pkg_name} ({pkg['ver']})...", "color": "green"})
        if deps:
             output.append({"text": f"Processing triggers for man-db...", "color": "grey"})
        
        return output

    def remove(self, pkg_name):
        if pkg_name not in self.installed:
            return [{"text": f"E: Package '{pkg_name}' is not installed, so not removed", "color": "red"}]
        
        del self.installed[pkg_name]
        return [
            {"text": "Reading package lists... Done", "color": "white"},
            {"text": "Building dependency tree... Done", "color": "white"},
            {"text": f"The following packages will be REMOVED: {pkg_name}", "color": "white"},
            {"text": f"Removing {pkg_name} ({self.repo[pkg_name]['ver']})...", "color": "white"},
            {"text": "Processing triggers for man-db...", "color": "grey"}
        ]

    def search(self, query):
        output = [{"text": "Sorting... Done", "color": "white"},
                  {"text": "Full Text Search... Done", "color": "white"}]
        
        found = False
        for name, data in self.repo.items():
            if query in name or query in data['desc']:
                status = "[installed]" if name in self.installed else ""
                output.append({"text": f"{name}/{status} {data['ver']} all", "color": "green"})
                output.append({"text": f"  {data['desc']}", "color": "white"})
                found = True
        
        if not found:
             output.append({"text": "No matches found.", "color": "grey"})
             
        return output

    def show(self, pkg_name):
        if pkg_name not in self.repo:
            return [{"text": f"N: Unable to locate package {pkg_name}", "color": "red"}]
            
        data = self.repo[pkg_name]
        return [
            {"text": f"Package: {pkg_name}", "color": "white"},
            {"text": f"Version: {data['ver']}", "color": "white"},
            {"text": "Maintainer: Teybr Maintainers <admin@teybr.os>", "color": "white"},
            {"text": f"Installed-Size: {data['size']}", "color": "white"},
            {"text": f"Depends: {', '.join(data['dep'])}", "color": "white"},
            {"text": f"Description: {data['desc']}", "color": "white"},
            {"text": "Homepage: https://teybr.os", "color": "white"},
        ]
        
    def list_installed(self):
        output = [{"text": "Listing installed packages...", "color": "cyan"}]
        for name, ver in self.installed.items():
            output.append({"text": f"{name}/{ver} [installed]", "color": "green"})
        return output
