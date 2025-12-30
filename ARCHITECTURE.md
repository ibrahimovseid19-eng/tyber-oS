# Teybr oS - Advanced Mobile Terminal OS
## System Architecture

### 1. Core Concept
A Python-based simulation of a mobile terminal operating system.
- **Frontend**: Flet (Python wrapper for Flutter) for high-performance, cross-platform UI with mobile aesthetics.
- **Backend**: Python-based virtual kernel.

### 2. Architecture Modules

#### `main.py`
The entry point. Configures the window to mimic a mobile device (portrait mode, small width) on Desktop, or full screen on mobile. Handles the Boot Sequence.

#### `kernel/`
- **`shell.py`**: The command interpreter. Parses input, arguments, and flags.
- **`filesystem.py`**: A virtual file system mimicking Linux (root /, home ~, bin, etc.). It does NOT touch the host OS file system directly for security (Sandbox).
- **`process_manager.py`**: Simulates running processes (PID, User, CPU usage).

#### `ui/`
- **`mobile_window.py`**: The main container. Contains the Status Bar and the Terminal View.
- **`terminal_widget.py`**: A custom Flet UserControl that mimics a terminal output (scrollable, monospace, colored text).
- **`virtual_keyboard.py`**: (Optional) On-screen extra keys (ESC, CTRL, ALT, TAB, ARROWS).

#### `commands/`
A modular plugin system. Each command is a separate Python script or Class.
- **Standard**: `ls`, `cd`, `pwd`, `mkdir`, `clear`, `echo`, `cat`
- **Advanced**: `net-scan`, `wifi-visualization`, `port-check` (Simulated with animations)
- **PowerShell**: `Get-Process`, `Clear-Host` (Mapped to internal logic)

### 3. UI Concept
- **Theme**: AMOLED Black (#000000) background.
- **Accent**: Neon Green (#00FF00) and Cyan (#00FFFF).
- **Font**: "JetBrains Mono" or "Courier New", glowing effect.
- **Layout**:
    - **Top**: Status Bar (Time, Battery, Wifi).
    - **Middle**: Terminal Output (Stream of text/components).
    - **Bottom**: Input Field + Virtual Key Accessories.

### 4. Boot Animation simulation
1.  **Stage 1**: Glitch effect logo "TEYBR OS".
2.  **Stage 2**: Kernel load imitation text (scrolling fast).
3.  **Stage 3**: Prompt `user@mobile:~$` appears.

### 5. Features to Implement
- **Artificial Intelligence**: Command suggestions.
- **Gamification**: "Hack" simulations.
