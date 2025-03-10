import tkinter as tk

class ThinkerPopup(tk.Toplevel):
    """"
    Class to create a Pop Up and ask for User to sumbit information needed to run the Application

    It inherits from the class Toplevel in tkinter package
    """
    def __init__(self, parent, title : str, geometry: str, label_text: str):
        super().__init__(parent)
        """"
        Initialize the ThinkerPopup class with the given configuration

        Initialize the parent class tk.Toplevel
        """

        self.title(title)  # Set the title of the popup window
        self.geometry(geometry)  # Set the size of the popup window
        self.resizable(False, False)  # Prevent resizing of the popup window
        self.configure(bg="#f0f0f0")  # Set the background color of the popup

        # Create a label to display the prompt text
        self.label = tk.Label(self, text=label_text, font=("Arial", 14), bg="#f0f0f0")
        self.label.pack(pady=10) # Add the label to the popup with padding

        # Create an entry widget for user input
        self.entry = tk.Entry(self, font=("Arial", 14), width=30)
        self.entry.pack(pady=10) # Add the entry widget to the popup with padding

        # Create a submit button that retrieves input when clicked
        self.submit_button = tk.Button(self, text="Submit", font=("Arial", 12), command=self.get_input)
        self.submit_button.pack(pady=10) # Add the button to the popup with padding

        self.result = None # Initialize a variable to store the user input

    def get_input(self):
        """Retrieve input and close the popup."""
        self.result = self.entry.get() # Get the text from the entry widget
        self.destroy()  # Close the popup window

def ask_for_code():
    root = tk.Tk() # Create the main application window
    root.withdraw() # Hide the main window

    popup = ThinkerPopup(
        root,
        title="Enter Strava Code",
        geometry="360x160", # "400x200"
        label_text="Please enter the Strava code."
    )
    root.wait_window(popup) # Wait for the popup to close before continuing

    return popup.result # Return the user input from the popup

