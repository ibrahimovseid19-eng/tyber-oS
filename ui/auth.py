import flet as ft
import asyncio

class AuthScreen(ft.Container):
    def __init__(self, page, on_success):
        super().__init__()
        self.page = page
        self.on_success = on_success
        self.expand = True
        self.bgcolor = "black"
        self.alignment = ft.alignment.center
        
        self.password_field = ft.TextField(
            password=True,
            can_reveal_password=True,
            text_align=ft.TextAlign.CENTER,
            width=300,
            text_style=ft.TextStyle(color="green", font_family="Consolas", size=18),
            cursor_color="green",
            border_color="green",
            focused_border_color="cyan",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            prefix_style=ft.TextStyle(color="green"),
            hint_text="ENTER PASSPHRASE -> 'toor'",
            hint_style=ft.TextStyle(color="#333333"),
            on_submit=self.verify_password
        )
        
        self.status = ft.Text("SECURE LOGIN REQUIRED", color="green", font_family="Consolas", size=14)
        
        self.content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SECURITY, color="green", size=60),
                ft.Container(height=20),
                self.status,
                ft.Container(height=20),
                self.password_field,
                ft.Container(height=20),
                ft.ElevatedButton(
                    "AUTHENTICATE",
                    style=ft.ButtonStyle(
                        color="black",
                        bgcolor="green",
                        shape=ft.RoundedRectangleBorder(radius=2)
                    ),
                    on_click=self.verify_password
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            border=ft.border.all(1, "green"),
            border_radius=10,
            bgcolor="#050505",
            width=400
        )

    async def verify_password(self, e):
        # Default password is 'toor' (Kali style)
        if self.password_field.value == "toor":
            self.status.value = "IDENTITY CONFIRMED"
            self.status.color = "cyan"
            self.password_field.border_color = "cyan"
            self.update()
            
            # Transition
            await self.do_success()
        else:
            self.status.value = "ACCESS DENIED"
            self.status.color = "red"
            self.password_field.border_color = "red"
            self.password_field.value = ""
            self.update()
            self.page.snack_bar = ft.SnackBar(ft.Text("Authentication Failed"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()

    async def do_success(self):
        await asyncio.sleep(1)
        if self.on_success:
            self.on_success()
