import flet as ft
import asyncio
import random

class IntroAnimation(ft.Container):
    def __init__(self, page, on_complete):
        super().__init__(expand=True, bgcolor="black", alignment=ft.Alignment(0, 0))
        self.page = page
        self.on_complete = on_complete
        
        # Initial UI State
        self.logo = ft.Text(
            "TEYBR oS", 
            size=60, 
            weight=ft.FontWeight.BOLD, 
            color="#00ff00", # Neon Green
            font_family="Consolas",
            opacity=0, # Start hidden for fade-in effect
            animate_opacity=1000
        )
        
        self.status = ft.Text(
            "SYSTEM HALTED", # Default backup text
            color="green", 
            font_family="Consolas",
            size=16
        )
        
        self.progress = ft.ProgressBar(
            width=300, 
            color="#00ff00", 
            bgcolor="#111111",
            visible=False # Hide initially
        )

        self.content = ft.Column(
            [
                self.logo,
                ft.Container(height=30),
                self.status,
                ft.Container(height=10),
                self.progress
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def did_mount(self):
        # Reliably start the animation task when added to page
        asyncio.create_task(self.animate_sequence())

    async def animate_sequence(self):
        try:
            # 1. Start Up
            await asyncio.sleep(0.5)
            self.status.value = "BOOT SEQUENCE INITIATED..."
            self.status.update()
            
            # 2. Logo Fade In
            await asyncio.sleep(1.0)
            self.logo.opacity = 1
            self.logo.update()
            await asyncio.sleep(1.5)
            
            # 3. Show Progress Bar
            self.progress.visible = True
            self.progress.update()
            
            # 4. Cinematic Boot Lines (Long Sequence ~15-20s)
            boot_log = [
                ("LOADING KERNEL IMAGE...", 1.5),
                ("VERIFYING CHECKSUMS [MD5/SHA256]...", 1.0),
                ("MOUNTING VIRTUAL FILESYSTEM (VFS)...", 1.2),
                ("LOADING DRIVERS: DISK, NET, GPU, HID...", 2.0),
                ("[!] WARNING: UNSECURE NETWORK DETECTED", 0.5),
                ("ACTIVATING STEALTH MODE...", 1.0),
                ("MASKING MAC ADDRESS: DE:AD:BE:EF:00:01", 1.5),
                ("BYPASSING REGIONAL FIREWALLS...", 2.0),
                ("INJECTING ROOTKIT HOOKS...", 1.0),
                ("STARTING SYSTEM SERVICES [SSHD, HTTPD]...", 1.5),
                ("ESTABLISHING ENCRYPTED TUNNEL (TOR)...", 2.0),
                ("USER 'ADMIN' ENVIRONMENT LOADED.", 1.2),
            ]
            
            for msg, delay in boot_log:
                self.status.value = msg
                # Simulate typing/processing glitch
                if random.random() > 0.5:
                     self.status.color = "#aaffaa" # Light green flash
                     self.status.update()
                     await asyncio.sleep(0.1)
                     self.status.color = "green"
                
                self.status.update()
                
                # Progress bar creep
                # We don't have exact % so just visual movement if we want, or indeterminate
                
                await asyncio.sleep(delay)
            
            # 5. Finalize
            self.status.value = "SYSTEM READY."
            self.status.color = "white"
            self.status.weight = ft.FontWeight.BOLD
            self.status.update()
            await asyncio.sleep(2.0)
            
            # 6. Handover
            if self.on_complete:
                self.on_complete()

        except Exception as e:
            print(f"Animation Error: {e}")
            # Fail safe: go to login anyway
            if self.on_complete:
                self.on_complete()
