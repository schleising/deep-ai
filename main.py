from pathlib import Path

import tkinter as tk
from tkinter import filedialog

from image_converter import ImageConverter

if __name__ == "__main__":
    # Create root window
    root = tk.Tk()
    root.withdraw()

    # Get filename
    filename = filedialog.askopenfilename()

    # Check if filename is not empty
    if filename != '':
        # Create the file path
        file_path = Path(filename)

        # Create the image converter
        image_converter = ImageConverter(file_path)
