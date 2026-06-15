import customtkinter as ctk
import database

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        # Clean, minimal dark theme
        super().__init__(parent, fg_color="#0f172a", corner_radius=0)
        
        # Configure layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self._render_cards()

    def _render_cards(self):
        # Clear existing
        for w in self.winfo_children():
            w.destroy()

        # Fetch live stats
        total_pws = database.get_total_count()

        self._create_card(
            0, 0, "Security Vault", "Active", 
            "#22c55e", "🛡️"
        )
        
        self._create_card(
            0, 1, "Total Passwords Saved", str(total_pws), 
            "#3b82f6", "🔐"
        )
        
        self._create_card(
            1, 0, "Encryption Status", "AES-128 (Fernet)", 
            "#94a3b8", "🔒"
        )

        self._create_card(
            1, 1, "System Health", "Optimal", 
            "#94a3b8", "⚡"
        )

    def _create_card(self, row, col, title, value, color, icon):
        card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=16)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 10))
        
        ctk.CTkLabel(header, text=icon, font=ctk.CTkFont(size=24)).pack(side="left")
        ctk.CTkLabel(
            header, text=title, font=ctk.CTkFont(family="Segoe UI", size=18), 
            text_color="#94a3b8"
        ).pack(side="left", padx=15)
        
        val_lbl = ctk.CTkLabel(
            card, text=value, 
            font=ctk.CTkFont(family="Segoe UI", size=42, weight="bold"), 
            text_color=color
        )
        val_lbl.pack(anchor="w", padx=30, pady=(0, 30))

    def refresh(self):
        """Called by the main app router when this tab is selected to load fresh data."""
        self._render_cards()
