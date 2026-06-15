import customtkinter as ctk
import database
import encryption

class AddPasswordView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0f172a", corner_radius=0)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.configure(width=500)
        
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            container, text="Store New Credential", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#f8fafc"
        ).grid(row=0, column=0, sticky="w", pady=(0, 40))

        # Website
        self.website_entry = self._create_input(container, "Website Name (e.g. GitHub)", 1)
        
        # Username
        self.username_entry = self._create_input(container, "Username / Email ID", 2)
        
        # Password
        pwd_frame = ctk.CTkFrame(container, fg_color="transparent")
        pwd_frame.grid(row=3, column=0, sticky="ew", pady=(15, 30))
        pwd_frame.grid_columnconfigure(0, weight=1)

        self.pwd_entry = ctk.CTkEntry(
            pwd_frame, placeholder_text="Password", height=50, corner_radius=8, 
            fg_color="#0f172a", border_width=1, border_color="#334155", show="*"
        )
        self.pwd_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        save_btn = ctk.CTkButton(
            container, text="Securely Save Credential", height=55, corner_radius=8, 
            fg_color="#22c55e", hover_color="#16a34a", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            command=self._save_credential
        )
        save_btn.grid(row=4, column=0, sticky="ew", pady=(10, 10))

        self.msg_lbl = ctk.CTkLabel(
            container, text="", font=ctk.CTkFont(size=14), text_color="#22c55e"
        )
        self.msg_lbl.grid(row=5, column=0, pady=10)

    def _create_input(self, parent, placeholder, row):
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder, height=50, width=450,
            corner_radius=8, fg_color="#0f172a", border_width=1, border_color="#334155"
        )
        entry.grid(row=row, column=0, sticky="ew", pady=15)
        return entry

    def _save_credential(self):
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        plain_pwd = self.pwd_entry.get().strip()
        
        if not website or not username or not plain_pwd:
            self._show_message("All fields are required!", "#ef4444")
            return
            
        try:
            # 1. Encrypt password
            encrypted_pwd = encryption.encrypt_password(plain_pwd)
            
            # 2. Save to database
            database.insert_credential(website, username, encrypted_pwd)
            
            # 3. Clear fields
            self.website_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.pwd_entry.delete(0, 'end')
            
            self._show_message("Credential saved successfully!", "#22c55e")
        except Exception as e:
            self._show_message(f"Error saving: {str(e)}", "#ef4444")

    def _show_message(self, text, color):
        self.msg_lbl.configure(text=text, text_color=color)
        # Clear message after 3 seconds
        self.after(3000, lambda: self.msg_lbl.configure(text=""))

    def refresh(self):
        self.website_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.pwd_entry.delete(0, 'end')
        self.msg_lbl.configure(text="")
