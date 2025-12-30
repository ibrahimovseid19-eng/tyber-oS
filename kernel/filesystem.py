class FileSystem:
    def __init__(self):
        # Structure: path -> content (if file) or None (if dir)
        # Simplified: We'll store a tree or a flat dict of paths. 
        # For a terminal sim, a flat dict of "absolute path" -> "type" is often easier to manage quickly.
        self.current_path = "/home/user"
        self.files = {
            "/": "dir",
            "/bin": "dir",
            "/etc": "dir",
            "/home": "dir",
            "/home/user": "dir",
            "/home/user/passwords.txt": "file",
            "/home/user/todo.txt": "file",
            "/var": "dir",
            "/var/log": "dir"
        }
        self.file_contents = {
            "/home/user/passwords.txt": "facebook: 123456\ninstagram: admin123",
            "/home/user/todo.txt": "1. Hack NASA\n2. Buy milk"
        }

    def list_dir(self, path=None):
        target_path = path if path else self.current_path
        if not target_path.endswith("/"): 
            target_path += "/"
            
        # Basic normalization for root
        if target_path == "//": target_path = "/"

        items = []
        # Find immediate children
        for p, type_ in self.files.items():
            if p == "/" and target_path == "/":
                 continue # Don't list root inside root
            
            # Check parental relationship
            # If parent of P is target_path
            parent = p.rsplit("/", 1)[0]
            if not parent: parent = "/" 
            
            # Special case for root children
            if parent == "" and target_path == "/":
                pass # logic tricky with flat dict string manipulation, let's simplify logic
                
        # Better logic:
        # Just iterate keys, if key starts with target_path and has no more slashes after the suffix
        results = []
        target_depth = target_path.count("/")
        if target_path == "/": target_depth = 0
        
        for p in self.files:
            if p == "/": continue
            if p.startswith(target_path):
                # Remove prefix
                sub = p[len(target_path):]
                # If sub has no / it is a child
                # If sub has / but it's only at the end (not possible in this store scheme), or ???
                if "/" not in sub:
                     results.append({"name": sub, "type": self.files[p]})
                
        return sorted(results, key=lambda x: x['name'])

    def change_dir(self, path):
        if path == "..":
            if self.current_path == "/": return
            self.current_path = self.current_path.rsplit("/", 1)[0]
            if self.current_path == "": self.current_path = "/"
            return "ok"
            
        # Handle absolute
        if path.startswith("/"):
            target = path
        else:
            # Handle relative
            target = f"{self.current_path}/{path}".replace("//", "/")
            
        target = target.rstrip("/") # normalize
        if target == "": target = "/"

        if target in self.files and self.files[target] == "dir":
            self.current_path = target
            return "ok"
        else:
            return "Directory not found"

    def make_dir(self, name):
        # target = self.current_path + "/" + name
        target = f"{self.current_path}/{name}".replace("//", "/")
        if target in self.files:
            return "File exists"
        self.files[target] = "dir"
        return "created"

    def get_pwd(self):
        return self.current_path
