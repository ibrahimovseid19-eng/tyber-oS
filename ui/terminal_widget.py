import flet as ft
from kernel.shell import Shell

class TerminalWidget(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.bgcolor = "black" # Deep black
        self.shell = Shell()
        self.shell.print_callback = self.print_output
        
        self.output_view = ft.ListView(
            expand=True,
            spacing=2,
            auto_scroll=True,
            padding=10,
        )
        
        self.input_field = ft.TextField(
            text_style=ft.TextStyle(font_family="Consolas", color="green", size=14),
            cursor_color="green",
            border_width=0,
            color="green",
            prefix_text="root@teybr:~$ ",
            prefix_style=ft.TextStyle(color="cyan", font_family="Consolas", weight=ft.FontWeight.BOLD),
            on_submit=self.handle_input,
            content_padding=10,
            multiline=False,
            dense=True
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.SelectionArea(content=self.output_view),
                    expand=True
                ),
                ft.Container(
                    content=self.input_field,
                    bgcolor="#111111",
                    border=ft.border.only(top=ft.border.BorderSide(1, "#333333")),
                    padding=2
                )
            ],
            spacing=0
        )

        # Boot message
        self.print_output("Teybr oS [Kernel 4.0.1]", color="grey")
        self.print_output("Initializing security protocols...", color="blue")
        self.print_output("...[OK] Memory Integrity", color="green")
        self.print_output("...[OK] Network Interfaces", color="green")
        self.output_view.controls.append(
             ft.Text("System loaded. Type 'help' for commands.", color="cyan")
        )


    def print_output(self, text, color="green"):
        self.output_view.controls.append(
            ft.Text(text, font_family="Consolas", color=color, size=14)
        )
        if self.page:
            self.update()

    def handle_input(self, e):
        cmd = self.input_field.value
        self.input_field.value = ""
        self.print_output(f"root@teybr:~$ {cmd}", color="white")
        
        if cmd.strip():
            try:
                # Basic parsing
                response = self.shell.execute(cmd)
                
                # Check if response is iterable (list or generator)
                if response:
                    for line in response:
                         # Check for clear command
                         if isinstance(line, dict) and line.get('action') == 'clear':
                             self.output_view.controls.clear()
                             self.update()
                             return
                         elif isinstance(line, dict):
                             self.print_output(line.get('text', ''), line.get('color', "green"))
            except Exception as ex:
                self.print_output(f"System Error: {ex}", color="red")
        
        self.update_prompt()
        self.input_field.focus()
        self.update()

    def update_prompt(self):
        prompt = "root@teybr:~$ "
        if self.shell.active_session and hasattr(self.shell.active_session, 'get_prompt'):
            prompt = self.shell.active_session.get_prompt()
        
        self.input_field.prefix_text = prompt
        self.input_field.update()
