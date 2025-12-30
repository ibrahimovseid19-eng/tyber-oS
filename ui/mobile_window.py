import flet as ft
from ui.terminal_widget import TerminalWidget
import asyncio
import datetime

class MobileWindow(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = "black"
        
        # Components
        self.status_bar = self.build_status_bar()
        self.terminal = TerminalWidget()
        
        self.content = ft.Column(
            controls=[
                self.status_bar,
                self.terminal,
            ],
            spacing=0,
            expand=True
        )
        
        # Start clock loop
        self.running = True
        # asyncio.create_task(self.update_clock()) # Flet handles async loops if app is async
        # We'll skip complex async for the MVP 'hello world' moment

    def build_status_bar(self):
        self.clock_text = ft.Text("12:00", size=12, color="cyan")
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("TEYBR 5G", size=12, color="cyan", weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    self.clock_text,
                    ft.Container(width=10),
                    ft.Text("100%", size=12, color="green"),
                    ft.Icon(ft.Icons.BATTERY_FULL, size=16, color="green"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            bgcolor="#101010", # Darker status bar
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#333333")),
            height=40
        )
