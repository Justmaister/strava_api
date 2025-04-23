import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any, Callable

class ThinkerPopup(tk.Toplevel):
    """
    A customizable popup window that supports various input types and configurations.

    Features:
    - Multiple input types (text entry, checkboxes, radio buttons)
    - Customizable styling and layout
    - Multiple buttons with custom callbacks
    - Flexible geometry and positioning
    - Theme support
    """
    def __init__(
            self,
            parent,
            title : str,
            geometry: str,
            theme: Dict[str, Any] = None,
            center_on_parent: bool = True
    ):
        """
        Initialize the popup window with basic configuration.

        Args:
            parent: Parent window
            title: Window title
            geometry: Window size in format "WxH"
            theme: Dictionary with styling options
            center_on_parent: Whether to center the window on parent
        """

        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)

        self.theme = {
            'bg_color': "#f0f0f0",
            'fg_color': "#000000",
            'button_color': "#e1e1e1",
            'font_family': "Arial",
            'title_size': 14,
            'text_size': 12,
            'button_size': 12,
            'padding': 10
        }
        if theme:
            self.theme.update(theme)

        self.resizable(False, False)
        self.configure(bg=self.theme['bg_color'])

        if center_on_parent:
            self.center_window()

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=self.theme['padding'],
                           pady=self.theme['padding'],
                           fill=tk.BOTH,
                           expand=True)

        self.widgets = {}
        self.results = {}

    def center_window(self):
        """Center the popup window."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"+{x}+{y}")

    def add_label(self, text: str, row: int = None) -> None:
        """Add a label to the popup."""
        label = ttk.Label(
            self.main_frame,
            text=text,
            font=(self.theme['font_family'], self.theme['title_size'])
        )
        if row is not None:
            label.grid(row=row, column=0, sticky="w", pady=self.theme['padding'])
        else:
            label.pack(pady=self.theme['padding'])

    def add_entry(self, name: str, placeholder: str = "", row: int = None) -> None:
        """Add a text entry field."""
        entry = ttk.Entry(
            self.main_frame,
            font=(self.theme['font_family'], self.theme['text_size']),
            width=40
        )
        if placeholder:
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e: self._clear_placeholder(entry, placeholder))
            entry.bind('<FocusOut>', lambda e: self._restore_placeholder(entry, placeholder))

        if row is not None:
            entry.grid(row=row, column=0, sticky="w", pady=self.theme['padding'])
        else:
            entry.pack(pady=self.theme['padding'])

        self.widgets[name] = entry

    def add_checkbutton(self, name: str, text: str, row: int = None) -> None:
        """Add a checkbox."""
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(
            self.main_frame,
            text=text,
            variable=var,
            style='Custom.TCheckbutton'
        )
        if row is not None:
            checkbox.grid(row=row, column=0, sticky="w", pady=self.theme['padding'])
        else:
            checkbox.pack(pady=self.theme['padding'])

        self.widgets[name] = (checkbox, var)

    def add_button(self, text: str, command: Callable, row: int = None) -> None:
        """Add a button with custom command."""
        button = ttk.Button(
            self.main_frame,
            text=text,
            command=command,
            style='Custom.TButton'
        )
        if row is not None:
            button.grid(row=row, column=0, sticky="w", pady=self.theme['padding'])
        else:
            button.pack(pady=self.theme['padding'])

    def get_results(self) -> Dict[str, Any]:
        """Collect all input values."""
        for name, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry):
                self.results[name] = widget.get()
            elif isinstance(widget, tuple):
                self.results[name] = widget[1].get()
        return self.results

    def _clear_placeholder(self, entry: ttk.Entry, placeholder: str) -> None:
        """Clear placeholder text on focus."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def _restore_placeholder(self, entry: ttk.Entry, placeholder: str) -> None:
        """Restore placeholder text if field is empty."""
        if entry.get() == "":
            entry.insert(0, placeholder)

def create_strava_code_popup() -> Optional[str]:
    """
    Create and show a popup window to ask for Strava authorization code.

    Returns:
        Optional[str]: The entered Strava code or None if cancelled
    """
    root = tk.Tk()
    root.withdraw()

    popup = ThinkerPopup(
        root,
        title="Enter Strava Code",
        geometry="500x180"
    )

    result = None

    def on_submit():
        nonlocal result
        entry = popup.widgets.get("strava_code")
        if entry:
            code = entry.get().strip()
            if not code:
                return
            result = code
            popup.destroy()

    popup.add_label("Please enter your Strava authorization code:")
    popup.add_entry("strava_code", placeholder="Enter code here")
    popup.add_button("Submit", on_submit)

    root.wait_window(popup)
    return result

def create_strava_data_sections_popup() -> Dict[str, Any]:
    """
    Create a popup for Strava data download configuration.
    Allows users to select which types of Strava data they want to download.

    Returns:
        Dict[str, Any]: Dictionary containing the selected data types and rate limit
    """
    root = tk.Tk()
    root.withdraw()

    popup = ThinkerPopup(
        root,
        title="Strava Data Download Settings",
        geometry="500x320"
    )

    popup.add_label("Select the sections to Download:", row=0)
    popup.add_checkbutton("download_athlete_section", "Download Athlete Section", row=1)
    popup.add_checkbutton("download_activities_section", "Download Athlete Section", row=2)
    popup.add_checkbutton("download_segment_section", "Download Athlete Section", row=3)
    popup.add_checkbutton("download_routes_section", "Download Athlete Section", row=4)
    popup.add_checkbutton("download_club_section", "Download Athlete Section", row=5)
    popup.add_button("Save Settings", lambda: popup.destroy(), row=6)

    root.wait_window(popup)
    return popup.get_results()

