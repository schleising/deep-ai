import sys


# Wrap the api key read in a try except block
try:
    # Read api key from file
    with open('api_key.txt', 'r') as api_key_file:
        # Set api key
        HEADERS = {
            'api-key': api_key_file.read(),
        }
except FileNotFoundError:
    # Print error message
    print("api_key.txt not found")

    # Exit program
    sys.exit()

from .ImageConverter import ImageConverter

__all__ = [
    "ImageConverter",
]
