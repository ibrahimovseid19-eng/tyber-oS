import flet as ft
from ui.mobile_window import MobileWindow
from ui.intro import IntroAnimation
from ui.auth import AuthScreen
import asyncio
import os

async def main(page: ft.Page):
    print("Initializing Teybr oS...")
    
    # --- Global Page Settings ---
    page.title = "Teybr oS - Penetration Testing Environment"
    page.window.width = 450
    page.window.height = 900
    page.window.resizable = True
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "black"
    page.fonts = {
        "Consolas": "https://fonts.gstatic.com/s/robotomono/v22/L0x5DF4xlVMF-BfR8bXMIhJHg45mwgGEFl0_3v0.woff2"
    }
    
    # --- Transitions ---
    
    async def show_terminal():
        print("[+] Loading Main Kernel Interface...")
        page.clean()
        mobile_os = MobileWindow(page)
        page.add(mobile_os)
        page.update()

    async def show_login():
        print("[+] Initiating Security Protocols...")
        page.clean()
        # Use lambda to schedule the async transition
        auth = AuthScreen(page, on_success=lambda: asyncio.create_task(show_terminal()))
        page.add(auth)
        page.update()

    async def show_intro():
        print("[+] Playing Cinematic Boot Sequence...")
        page.clean()
        
        # Using the Upgraded Python Canvas Matrix Animation
        # This matches the user's "Graphical" request but keeps it native/stable
        intro = IntroAnimation(page, on_complete=lambda: asyncio.create_task(show_login()))
        page.add(intro)
        page.update()

    # --- Start ---
    try:
        await show_intro()
    except Exception as e:
        print(f"Intro Startup Failed: {e}")
        # Emergency UI for mobile debugging
        page.clean()
        page.add(
            ft.Column([
                ft.Icon(ft.Icons.ERROR, color="red", size=50),
                ft.Text(f"BOOT FAILURE:\n{str(e)}", color="red", size=20, selectable=True),
                ft.ElevatedButton("SAFE MODE LOGIN", on_click=lambda _: asyncio.create_task(show_login()))
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()
        return 
    
    print("UI mounted successfully.")

if __name__ == "__main__":
    print("Starting Flet app...")
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"Failed to launch Flet: {e}")
