import hashlib
import time
import random

def register(shell):
    shell.register_command("hashgen", cmd_hashgen)
    shell.register_command("whois", cmd_whois)
    shell.register_command("sqlmap", cmd_sqlmap)

def cmd_hashgen(args):
    """
    Generates MD5 and SHA256 hashes for a given string.
    Usage: hashgen <text>
    """
    if not args:
        return [{"text": "Usage: hashgen <text>", "color": "red"}]
    
    text = args.strip()
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    
    return [
        {"text": f"String: {text}", "color": "white"},
        {"text": f"MD5:    {md5_hash}", "color": "cyan"},
        {"text": f"SHA256: {sha256_hash}", "color": "green"}
    ]

def cmd_whois(args):
    """
    Simulates a WHOIS lookup.
    """
    if not args:
        return [{"text": "Usage: whois <domain>", "color": "red"}]
    
    domain = args.strip()
    output = []
    output.append({"text": f"[*] Querying WHOIS server for {domain}...", "color": "blue"})
    output.append({"text": "   Domain Name: " + domain.upper(), "color": "white"})
    output.append({"text": "   Registry Domain ID: 2319283_DOMAIN_COM-VRSN", "color": "grey"})
    output.append({"text": "   Registrar WHOIS Server: whois.godaddy.com", "color": "grey"})
    output.append({"text": "   Registrar URL: http://www.godaddy.com", "color": "grey"})
    output.append({"text": "   Updated Date: 2024-11-15T10:22:11Z", "color": "grey"})
    output.append({"text": "   Creation Date: 2019-03-20T14:44:00Z", "color": "grey"})
    output.append({"text": "   Registrar Registration Expiration Date: 2026-03-20T14:44:00Z", "color": "grey"})
    output.append({"text": "   Registrar: GoDaddy.com, LLC", "color": "white"})
    output.append({"text": "   Registrant State/Province: Arizona", "color": "grey"})
    output.append({"text": "   Registrant Country: US", "color": "grey"})
    output.append({"text": "   Name Server: NS1.CLOUDFLARE.COM", "color": "cyan"})
    output.append({"text": "   Name Server: NS2.CLOUDFLARE.COM", "color": "cyan"})
    output.append({"text": "[*] Query complete.", "color": "green"})
    return output

def cmd_sqlmap(args):
    """
    Tries to run the REAL sqlmap if installed on the system.
    Otherwise falls back to the simulation.
    """
    # 1. Check if 'sqlmap' is in the system PATH
    system_sqlmap = shutil.which("sqlmap")
    
    # 2. If valid args and tool exists, try running it
    if system_sqlmap and args:
        try:
            # Running real command
            # Note: This runs in the console, capturing output might be tricky with interactive tools
            # We will run it and capture standard output
            output = [{"text": f"[*] Executing generic system SQLMap: {system_sqlmap}", "color": "blue"}]
            
            cmd_line = f"sqlmap {args} --batch" # --batch to avoid interactive questions blocking the UI
            
            process = subprocess.Popen(
                cmd_line, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if stdout:
                for line in stdout.splitlines():
                    output.append({"text": line, "color": "white"})
            if stderr:
                for line in stderr.splitlines():
                    output.append({"text": line, "color": "red"})
                    
            return output
        except Exception as e:
             return [{"text": f"System SQLMap Error: {e}", "color": "red"}]

    # 3. Fallback: Simulation (if not installed or no args)
    target = args.strip() if args else "http://target-site.com/php?id=1"
    
    # ASCII Art from sqlmap
    yield {"text": "        ___", "color": "yellow"}
    yield {"text": "       __H__", "color": "yellow"}
    yield {"text": " ___ ___[.]_____ ___ ___  {1.5.2#stable}", "color": "yellow"}
    yield {"text": "|_ -| . [.]     | .'| . |", "color": "yellow"}
    yield {"text": "|___|_  [.]_|_|_|__,|  _|", "color": "yellow"}
    yield {"text": "      |_|V...       |_|   http://sqlmap.org", "color": "yellow"}
    yield {"text": "", "color": "white"}
    
    if not system_sqlmap:
        yield {"text": "[!] REAL SQLMAP NOT FOUND IN SYSTEM PATH.", "color": "red", "weight": "bold"}
        yield {"text": "[!] Running in SIMULATION MODE.", "color": "orange"}
        yield {"text": "[!] Install sqlmap and add to PATH to use real features.", "color": "grey"}
    
    yield {"text": f"[*] starting at {time.strftime('%H:%M:%S')}", "color": "cyan", "delay": 0.2}
    yield {"text": f"[*] checking connection to the target URL", "color": "white", "delay": 0.5}
    yield {"text": f"[*] checking if the target is protected by some WAF/IPS", "color": "white", "delay": 0.7}
    yield {"text": f"[!] heuristics detected that the target is protected by some WAF/IPS", "color": "amber", "delay": 0.3}
    yield {"text": f"[*] testing if the target URL content is stable", "color": "white", "delay": 0.4}
    yield {"text": f"[*] target URL content is stable", "color": "white", "delay": 0.2}
    
    # Fake processing
    param = "id" 
    
    yield {"text": f"[*] testing for SQL injection on GET parameter '{param}'", "color": "white", "delay": 0.3}
    yield {"text": f"[*] testing 'AND boolean-based blind - WHERE or HAVING clause'", "color": "white", "delay": 0.8}
    yield {"text": f"[*] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'", "color": "white", "delay": 1.0}
    yield {"text": f"[+] GET parameter '{param}' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable", "color": "green", "weight": "bold", "delay": 0.2}
    
    yield {"text": "---", "color": "white"}
    yield {"text": f"Parameter: {param} (GET)", "color": "white"}
    yield {"text": "    Type: error-based", "color": "white"}
    yield {"text": "    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)", "color": "white"}
    yield {"text": "    Payload: id=1 AND (SELECT 8295 FROM(SELECT COUNT(*),CONCAT(0x7171627671,(SELECT (ELT(8295=8295,1))),0x716a707671,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)", "color": "white"}
    yield {"text": "---", "color": "white"}

    yield {"text": "[*] the back-end DBMS is MySQL", "color": "cyan", "delay": 0.4}
    yield {"text": "[*] fetching current database", "color": "cyan", "delay": 0.5}
    yield {"text": "current database: 'production_db'", "color": "green", "weight": "bold"}
    
    yield {"text": "[*] fetching tables for database: 'production_db'", "color": "cyan", "delay": 0.6}
    yield {"text": "Database: production_db", "color": "white"}
    yield {"text": "[3 tables]", "color": "white"}
    yield {"text": "+-------------+", "color": "white"}
    yield {"text": "| users       |", "color": "white"}
    yield {"text": "| products    |", "color": "white"}
    yield {"text": "| orders      |", "color": "white"}
    yield {"text": "+-------------+", "color": "white"}
    
    yield {"text": "[*] dumping table 'users'...", "color": "cyan", "delay": 1.2}
    yield {"text": "+----+----------+----------------------------------+-----------------+", "color": "white"}
    yield {"text": "| id | username | password_hash                    | email           |", "color": "white"}
    yield {"text": "+----+----------+----------------------------------+-----------------+", "color": "white"}
    yield {"text": "| 1  | admin    | 5f4dcc3b5aa765d61d8327deb882cf99 | admin@site.com  |", "color": "white"}
    yield {"text": "| 2  | user     | 098f6bcd4621d373cade4e832627b4f6 | user@site.com   |", "color": "white"}
    yield {"text": "| 3  | guest    | 098f6bcd4621d373cade4e832627b4f6 | guest@site.com  |", "color": "white"}
    yield {"text": "+----+----------+----------------------------------+-----------------+", "color": "white"}
    
    yield {"text": "[*] fetched data logged to text files under '/home/user/.sqlmap/output'", "color": "white"}

