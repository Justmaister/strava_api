import tkinter as tk

class ThinkerPopup(tk.Toplevel):
    def __init__(self, parent, title : str, geometry: str, label_text: str):
        super().__init__(parent)

        self.title = title
        self.geometry = geometry
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.label = tk.Label(self, text=label_text, font=("Arial", 14), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, font=("Arial", 14), width=30)
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Submit", font=("Arial", 12), command=self.get_input)
        self.submit_button.pack(pady=10)

        self.result = None

    def get_input(self):
        """Retrieve input and close the popup."""
        self.result = self.entry.get()
        self.destroy()

def ask_for_code():
    root = tk.Tk()
    root.withdraw()

    popup = ThinkerPopup(
        root,
        title="Enter Strava Code",
        geometry="400x200", # "400x200"
        label_text="Please enter the Strava code."
    )
    root.wait_window(popup)

    return popup.result

