import customtkinter as ctk
import database
import encryption
import pyperclip

class PasswordListView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1e293b", corner_radius=16)
        
        # Header / Search bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Search by website name...", 
            height=45, corner_radius=8, fg_color="#0f172a", border_width=1, border_color="#334155",
            font=ctk.CTkFont(size=15)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self._on_search)

        refresh_btn = ctk.CTkButton(
            search_frame, text="🔄 Refresh", width=100, height=45,
            fg_color="#334155", hover_color="#3b82f6", corner_radius=8,
            command=self.refresh
        )
        refresh_btn.pack(side="right")

        # Table Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        header_frame.pack(fill="x", padx=40)
        header_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        headers = ["Website", "Username / Email", "Password", "Actions"]
        for i, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                header_frame, text=text, text_color="#94a3b8", 
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            )
            lbl.grid(row=0, column=i, sticky="w")
            if i == 3:
                lbl.grid_configure(sticky="e", padx=20)
            
        # Scrollable list
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.rows = []

    def _on_search(self, event):
        query = self.search_entry.get().strip()
        if query:
            results = database.search_credentials(query)
            self._render_rows(results)
        else:
            self.refresh()

    def refresh(self):
        self.search_entry.delete(0, 'end')
        results = database.get_all_credentials()
        self._render_rows(results)

    def _render_rows(self, data):
        # Clear existing rows
        for w in self.scroll.winfo_children():
            w.destroy()
            
        self.rows = []
        for item in data:
            self._create_row(item)

    def _create_row(self, item):
        cred_id = item['id']
        website = item['website']
        username = item['username']
        encrypted_pwd = item['encrypted_password']

        row = ctk.CTkFrame(self.scroll, fg_color="#0f172a", corner_radius=10, height=65)
        row.pack(fill="x", pady=6, padx=10)
        row.grid_propagate(False)
        row.grid_columnconfigure((0,1,2), weight=1)
        row.grid_columnconfigure(3, weight=0)

        # Hover Effect logic
        row.bind("<Enter>", lambda e, r=row: r.configure(fg_color="#334155"))
        row.bind("<Leave>", lambda e, r=row: r.configure(fg_color="#0f172a"))

        ctk.CTkLabel(
            row, text=website, text_color="#f8fafc", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=18)
        
        ctk.CTkLabel(
            row, text=username, text_color="#94a3b8", font=ctk.CTkFont(size=14)
        ).grid(row=0, column=1, sticky="w", padx=10, pady=18)
        
        # Hidden Password Label
        pwd_lbl = ctk.CTkLabel(
            row, text="••••••••••••", text_color="#94a3b8", 
            font=ctk.CTkFont(family="Courier", size=16)
        )
        pwd_lbl.grid(row=0, column=2, sticky="w", padx=10, pady=18)

        act_frame = ctk.CTkFrame(row, fg_color="transparent")
        act_frame.grid(row=0, column=3, sticky="e", padx=15, pady=12)
        
        is_revealed = [False]  # Mutable state for the specific row

        def toggle_reveal():
            if is_revealed[0]:
                pwd_lbl.configure(text="••••••••••••")
                reveal_btn.configure(text="👁")
                is_revealed[0] = False
            else:
                decrypted = encryption.decrypt_password(encrypted_pwd)
                pwd_lbl.configure(text=decrypted)
                reveal_btn.configure(text="🙈") # Hide icon
                is_revealed[0] = True

        def copy_pwd():
            decrypted = encryption.decrypt_password(encrypted_pwd)
            if decrypted and decrypted != "DECRYPTION_FAILED":
                pyperclip.copy(decrypted)
                
                # Visual feedback on copy
                orig_color = copy_btn.cget("fg_color")
                copy_btn.configure(fg_color="#22c55e")
                self.after(1000, lambda: copy_btn.configure(fg_color=orig_color))

        def delete_entry():
            database.delete_credential(cred_id)
            self.refresh() # Reload list

        # Action Buttons
        copy_btn = ctk.CTkButton(
            act_frame, text="📋", width=38, height=38, fg_color="transparent", 
            hover_color="#3b82f6", corner_radius=8, font=ctk.CTkFont(size=16),
            command=copy_pwd
        )
        copy_btn.pack(side="left", padx=4)
        
        reveal_btn = ctk.CTkButton(
            act_frame, text="👁", width=38, height=38, fg_color="transparent", 
            hover_color="#334155", corner_radius=8, font=ctk.CTkFont(size=16),
            command=toggle_reveal
        )
        reveal_btn.pack(side="left", padx=4)
        
        del_btn = ctk.CTkButton(
            act_frame, text="🗑️", width=38, height=38, fg_color="transparent", 
            hover_color="#ef4444", corner_radius=8, text_color="#ef4444", font=ctk.CTkFont(size=16),
            command=delete_entry
        )
        del_btn.pack(side="left", padx=4)
