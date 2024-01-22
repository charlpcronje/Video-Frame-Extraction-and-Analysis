**Using the CLI Application**

1. **Install Required Packages**:
   Before using the CLI application, make sure you have the necessary packages installed. Open a terminal and run the following command to install the required packages:

   ```shell
   pip install python-dotenv opencv-python-headless
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory of the application. You can specify all the configuration settings in this file. Here's an example of how the `.env` file should look:

   ```plaintext
   # .env configuration settings
   VIDEO_PATH=/path/to/video.mp4
   OUTPUT_FOLDER=/output/frames
   SOURCE_FOLDER=/source/images
   SHARP_IMAGES_FOLDER=/sharp/images
   SHARPNESS_THRESHOLD=100
   FRAMES_TO_SKIP=1
   TOTAL_IMAGES_TO_EXTRACT=100
   ```

   Replace the placeholders with your specific paths and values.

3. **Running the CLI Application**:
   To run the CLI application, open a terminal and navigate to the root directory of the application where `app.py` is located. Then, use the following command:

   ```shell
   python app.py
   ```

   This will start the CLI application.

4. **Using the CLI Commands**:
   The CLI application provides the following commands:

   - `extract_frames`: Extract frames from a video file with optional frame skipping and total images to extract.
   - `analyze_images`: Analyze images for sharpness and move sharp images to a target directory.
   - `generate_collage`: Generate collage images from extracted frames.

   To use a command, simply run it in the terminal with the desired options. For example:

   ```shell
   python app.py extract_frames --frames_to_skip 2 --total_images_to_extract 50
   ```

   This command will extract frames with a frame skipping factor of 2 and a total of 50 images.

5. **Authentication**:
   API key authentication is required when using the CLI application. You need to provide your API key in the command line as follows:

   ```shell
   python app.py extract_frames --api_key your_api_key
   ```

   Replace `your_api_key` with your actual API key.

6. **Review the Output**:
   The CLI application will generate output based on the commands you run. Review the terminal output for any messages or results.

That's it! You can now use the CLI application with the specified functionality. Make sure to set up the `.env` file with your configuration settings and provide the API key for authentication when running commands.

7. **New CLI Command: `generate_collage`**

- **Command**: `python app.py --generate_collage --collage_folder path/to/collage/folder`
- **Description**: Generates a collage from the frames in the specified folder.
- **Example**:
  ```shell
  python app.py --generate_collage --frames_folder path/to/frames --collage_folder path/to/collage
  ```
- **Prerequisites**: Ensure that the frames folder contains the images to be used for the collage.
```