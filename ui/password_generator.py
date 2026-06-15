import customtkinter as ctk
import pyperclip
from password_generator import generate_strong_password

class GeneratorView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0f172a", corner_radius=0)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.configure(width=600)
        
        # Display Area
        disp_frame = ctk.CTkFrame(container, fg_color="#1e293b", corner_radius=12, height=120)
        disp_frame.pack(fill="x", pady=(0, 40))
        disp_frame.pack_propagate(False)

        self.display_lbl = ctk.CTkLabel(
            disp_frame, text="", 
            font=ctk.CTkFont(family="Courier", size=36, weight="bold"), 
            text_color="#3b82f6"
        )
        self.display_lbl.pack(expand=True)

        # Length Slider
        len_frame = ctk.CTkFrame(container, fg_color="transparent")
        len_frame.pack(fill="x", pady=10)
        
        self.len_lbl = ctk.CTkLabel(
            len_frame, text="Password Length: 16", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#f8fafc"
        )
        self.len_lbl.pack(anchor="w", pady=(0, 15))
        
        self.slider = ctk.CTkSlider(
            len_frame, from_=8, to=32, number_of_steps=24,
            progress_color="#3b82f6", button_color="#3b82f6", 
            button_hover_color="#2563eb", height=20, 
            command=self._on_slide
        )
        self.slider.set(16)
        self.slider.pack(fill="x")

        # Actions
        act_frame = ctk.CTkFrame(container, fg_color="transparent")
        act_frame.pack(fill="x", pady=40)
        act_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            act_frame, text="🔄 Generate New", height=50, corner_radius=8, 
            fg_color="#3b82f6", hover_color="#2563eb", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            command=self._generate
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.copy_btn = ctk.CTkButton(
            act_frame, text="📋 Copy Password", height=50, corner_radius=8, 
            fg_color="#334155", hover_color="#22c55e", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            command=self._copy_pwd
        )
        self.copy_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Warning Label
        self.info_lbl = ctk.CTkLabel(
            container, text="Includes A-Z, a-z, 0-9, and symbols.",
            text_color="#94a3b8", font=ctk.CTkFont(size=13)
        )
        self.info_lbl.pack(pady=10)

        # Initial Gen
        self._generate()

    def _on_slide(self, val):
        self.len_lbl.configure(text=f"Password Length: {int(val)}")
        self._generate()

    def _generate(self):
        length = int(self.slider.get())
        pwd = generate_strong_password(length)
        self.display_lbl.configure(text=pwd)
        self.copy_btn.configure(text="📋 Copy Password", fg_color="#334155")

    def _copy_pwd(self):
        pwd = self.display_lbl.cget("text")
        if pwd:
            pyperclip.copy(pwd)
            self.copy_btn.configure(text="✅ Copied!", fg_color="#22c55e")

    def refresh(self):
        self._generate()
