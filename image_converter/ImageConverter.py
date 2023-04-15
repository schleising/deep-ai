from pathlib import Path
import shutil
import subprocess

import requests

from . import HEADERS

class ImageConverter:
    def __init__(self, input_file_path: Path):
        # Set input and output file paths
        self.input_file_path = input_file_path
        output_file_name = self.input_file_path.stem + '_converted' + self.input_file_path.suffix
        self.output_file_path = Path.home() / 'Downloads' / 'Deep_AI' / output_file_name

        # Create output directory if it doesn't exist
        self.output_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Iniialise download url
        self.download_url: str | None = None

        # Run the conversion
        send_success = self.send_image()

        if send_success:
            # Download the image
            self.download_image()

    def send_image(self) -> bool:
        # Send image to Deep AI
        print("Sending image to Deep AI...")

        # Open image
        with self.input_file_path.open('rb') as image_file:
            # Send image to Deep AI
            r = requests.post(
                "https://api.deepai.org/api/torch-srgan",
                files={
                    'image': image_file,
                },
                headers=HEADERS,
            )

        # Check if request was successful
        if r.status_code == requests.codes.ok:
            # Print success message
            print("Image sent successfully")

            # Get download url
            self.download_url = r.json()['output_url']

            # Return True
            return True
        else:
            # Print error message
            print("Error sending image to Deep AI")

            # Print response
            print(r.json())

            # Set the download url to None
            self.download_url = None

            # Return False
            return False

    def download_image(self):
        # Print download message
        print("Downloading image...")

        # Check if download url is not None
        if self.download_url is not None:
            # Download image from Deep AI
            r = requests.get(self.download_url, stream=True)

            # Write image to file
            with self.output_file_path.open('wb') as output_file:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        output_file.write(chunk)

            # Print success message
            print("Image downloaded successfully")

            # Copy the original image to the output directory
            shutil.copy(self.input_file_path, self.output_file_path.parent)

            # Open the image
            subprocess.Popen(['open', self.output_file_path])
