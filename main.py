import customtkinter as ctk
import database

# Import all view modules
from ui.dashboard import DashboardView
from ui.add_password import AddPasswordView
from ui.password_list import PasswordListView
from ui.password_generator import GeneratorView

ctk.set_appearance_mode("dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SecurePass - Clean Password Manager")
        self.geometry("1000x650")
        self.minsize(900, 600)
        self.configure(fg_color="#0f172a") # Primary Dark BG
        
        # Ensure DB is ready
        database.create_tables()

        # Grid Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)

        self._build_sidebar()
        self._build_main_container()
        
        # Build Pages
        self.views = {
            "Dashboard": DashboardView(self.main_container),
            "Add Password": AddPasswordView(self.main_container),
            "Password Manager": PasswordListView(self.main_container),
            "Password Generator": GeneratorView(self.main_container),
        }

        for view in self.views.values():
            view.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 30))

        # Start with Dashboard
        self.select_nav(0, self.show_dashboard)

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=0, width=240)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Brand Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🔐 SECUREPASS", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), 
            text_color="#f8fafc"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 45), sticky="w")

        # Nav Buttons
        self.nav_buttons = []
        nav_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Add Password", self.show_add_pwd),
            ("🗝️ Password Manager", self.show_manager),
            ("🎲 Password Generator", self.show_generator)
        ]

        for i, (text, command) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar_frame, 
                text=text, 
                fg_color="transparent",
                text_color="#94a3b8",
                hover_color="#334155",
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="normal"),
                command=lambda cmd=command, idx=i-1: self.select_nav(idx, cmd),
                height=45,
                corner_radius=8
            )
            btn.grid(row=i, column=0, padx=15, pady=5, sticky="ew")
            self.nav_buttons.append(btn)

    def _build_main_container(self):
        self.main_container = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Header Bar
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="#0f172a", corner_radius=0, height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Dashboard", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), 
            text_color="#f8fafc"
        )
        self.title_label.grid(row=0, column=0, sticky="w")

    def select_nav(self, index, command):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(
                    fg_color="#3b82f6", text_color="#f8fafc", 
                    font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                    hover_color="#2563eb"
                )
            else:
                btn.configure(
                    fg_color="transparent", text_color="#94a3b8", 
                    font=ctk.CTkFont(family="Segoe UI", size=15, weight="normal"),
                    hover_color="#334155"
                )
        command()

    def show_view(self, name):
        self.title_label.configure(text=name)
        for view_name, view_frame in self.views.items():
            if view_name == name:
                view_frame.tkraise()
                # Trigger a refresh on load to ensure data is current
                if hasattr(view_frame, 'refresh'):
                    view_frame.refresh()

    def show_dashboard(self):
        self.show_view("Dashboard")

    def show_add_pwd(self):
        self.show_view("Add Password")

    def show_manager(self):
        self.show_view("Password Manager")

    def show_generator(self):
        self.show_view("Password Generator")


if __name__ == "__main__":
    app = App()
    app.mainloop()
