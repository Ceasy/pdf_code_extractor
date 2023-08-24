import tkinter as tk
import os

from pdf_extractor import PDFExtractor
from gui_app import GuiApp
from settings import MainSettings


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(MainSettings.Window.title)
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ico", "32px.ico"))
        self.root.iconbitmap(icon_path)
        self.root.minsize(*MainSettings.Window.min_size)
        self.root.maxsize(*MainSettings.Window.max_size)
        self.extractor = PDFExtractor()
        self.gui = GuiApp(self.root, self.extractor)
        self.center_window()

    def center_window(self):
        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get window size
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # Calc coordinates for placing the window in the center of the screen
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Setup pos and size of the window
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
