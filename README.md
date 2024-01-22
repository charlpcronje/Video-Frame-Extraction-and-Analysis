# Video Frame Extraction and Analysis

## Overview
This Flask application provides functionalities for extracting frames from an MP4 file and analyzing these frames to find and move the least blurry (sharpest) images to a designated folder. It's designed to be both a web service and a command-line tool, offering flexibility in usage.

## Features
- **Frame Extraction**: Extract every frame from an MP4 file as high-quality PNG images.
- **Image Analysis**: Analyze extracted frames to determine sharpness, moving the sharpest images to a specified folder.
- **Command-Line Interface**: Run functionalities via command-line arguments.
- **Flask Endpoints**: Access functionalities through web API endpoints.
- **Environment Variable Configuration**: Configure paths and settings via a `.env` file.
- **Generate Collage**: Create a collage from a specified folder of frames.

## Usage and Auth

- [Command-Line Interface](./docs/cli.md)
- [Authentication](./docs/auth.md)
- [Environment Variable](./env.example.md)
- [Code Explained](./docs/explain.md)
- [API Documentation](./docs/api.md)
- OpenAI Schema [JSON](./openai.schema.json), [YML](./openAI_schema.yml)

## Changelog
- **v1.0.0**
  - Initial release with frame extraction and image analysis capabilities.
  - Added functionality to generate collages from extracted frames.

## Usage Examples for `move_sharp_images` Function

This function is designed to analyze and classify images based on their sharpness. It can operate in two modes: static and dynamic thresholding. Below are examples of how to use each mode:

### Static Sharpness Threshold

In static mode, images are classified as sharp based on a fixed threshold value. This mode is straightforward and best used when you have a consistent expectation of image sharpness across different datasets.

**Example**:

```python
# Using the static sharpness threshold
from move_sharp_images import move_sharp_images

# Set your source and destination directories
source_directory = "path/to/source/images"
sharp_images_directory = "path/to/sharp/images"

# Define a fixed sharpness threshold
sharpness_threshold = 100

# Call the function with static thresholding
move_sharp_images(source_directory, sharp_images_directory, sharpness_threshold, dynamic_threshold=False)
```

In this example, any image with a sharpness score of 100 or more will be considered sharp and moved to the `sharp_images_directory`.

### Dynamic Sharpness Threshold

Dynamic mode calculates the average sharpness of all images and then sets the threshold to this average plus a defined increment. This mode is useful when dealing with varied image qualities, as it adapts to the overall sharpness level of the dataset.

**Example**:

```python
# Using the dynamic sharpness threshold
from move_sharp_images import move_sharp_images

# Set your source and destination directories
source_directory = "path/to/source/images"
sharp_images_directory = "path/to/sharp/images"

# The static threshold is overridden in dynamic mode
sharpness_threshold = 100
sharp_if = 10  # Increment added to the average sharpness

# Call the function with dynamic thresholding
move_sharp_images(source_directory, sharp_images_directory, sharpness_threshold, sharp_if, dynamic_threshold=True)
```

Here, the function first calculates the average sharpness of all images in `source_directory`. It then classifies an image as sharp if its sharpness score exceeds this average by at least `sharp_if` (in this case, 10). This method ensures that the best images relative to your specific dataset are selected.

## Environment Variables
- `VIDEO_PATH`: Path to the video file
- `OUTPUT_FOLDER`: Output folder for extracted frames
- `SOURCE_FOLDER`: Source folder for image analysis
- `SHARP_IMAGES_FOLDER`: Folder for sharp images
- `SHARPNESS_THRESHOLD`: Sharpness threshold
- `FRAMES_TO_SKIP`: Number of frames to skip between frames to save
- `TOTAL_IMAGES_TO_EXTRACT`: Total number of images to extract
- `COLLAGE_FOLDER`: Folder to save generated collages
- `FRAMES_FOLDER`: Folder containing frames for collage generation
- `API_KEY`: API key for authentication (if applicable)
- `COLLAGE_FOLDER`: Folder to save generated collages.
- `FRAMES_FOLDER`: Folder containing frames for collage generation.

### Installation Guide

#### Prerequisites
- Python 3.6 or higher.
- pip (Python package installer).
- Virtual environment (recommended but optional).

#### Steps

1. **Clone the Project Repository (if applicable)**
   - If your project is hosted on a version control system like GitHub, clone the repository to your local machine. 
   ```shell
   git clone [URL to your repository]
   cd [repository name]
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   - It's a good practice to create a virtual environment for your Python projects to avoid dependency conflicts.
   ```shell
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**
   - Your project's dependencies should be listed in `requirements.txt`. Install them using pip.
   ```shell
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in your project's root directory and populate it with necessary environment variables as per your project needs. Example:
     ```env
     FLASK_APP=app.py
     FLASK_ENV=development
     # Add other variables like API keys, database URLs, etc.
     ```

5. **Run the Flask Application**
   - Once all dependencies are installed and environment variables are set, you can start your Flask application.
   ```shell
   flask run
   ```

6. **Additional Steps**
   - If your project requires a database or any other external service, set them up and ensure they are running.
   - Make sure any paths (like for file storage) specified in your `.env` file or elsewhere in your project are correctly set up and accessible.

#### Notes
- Always refer to the project's README.md for any specific instructions.
- If there are any post-installation steps (like database migrations), make sure to run them.
- For production deployment, additional steps will be required, including proper server setup, environment configuration, security considerations, etc.

This guide provides a general setup process for Python projects with similar dependencies. Adjust the instructions as necessary to fit your specific project requirements.

## Dependencies

The `requirements.txt` file should list all the Python packages that your project depends on. Given the imports in your project, here's what the `requirements.txt` should likely include:

```plaintext
Flask
python-dotenv
opencv-python-headless
numpy
```

Explanation for each package:

1. **Flask**: Since you're using `from flask import Flask, jsonify`, your project is a Flask web application.

2. **python-dotenv**: This package is used to load environment variables from a `.env` file, as indicated by your import of `from dotenv import load_dotenv`.

3. **opencv-python-headless**: This is the headless version of OpenCV, suitable for server environments where you don't need GUI functionality. It's included because of your `import cv2` statements. The headless version avoids unnecessary dependencies on GUI packages.

4. **numpy**: It's a dependency for OpenCV and also widely used in image processing (your `import numpy as np` statement).

Note:
- If your `auth` module is a custom module or part of a package not included in this list, you'll need to add that package to the list as well.
- Make sure to specify versions if your project requires specific versions of these packages to function correctly. For example, `Flask==2.0.1`.
- This list assumes that standard libraries like `os`, `sys`, and `shutil` are not listed, as they are part of the Python Standard Library and do not need to be installed via pip.


## Contributions
Contributions to this project are welcome. Please follow the standard fork-pull request workflow. Ensure that your code adheres to the existing style and that all tests pass.

## Contact
For any queries or assistance, please reach out to:

- **Name**: Charl Cronje
- **Email**: [charl@cronje.me](mailto:charl@cronje.me)
- **LinkedIn**: [https://www.linkedin.com/in/charlpcronje](https://www.linkedin.com/in/charlpcronje)

## Additional Documentation
For a comprehensive explanation of the application code, logic blocks, and usage examples, please refer to the [Explain.md](./explain.md) file.