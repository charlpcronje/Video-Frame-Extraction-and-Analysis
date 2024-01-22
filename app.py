# app.py
import os
import sys
from flask import Flask, jsonify
from dotenv import load_dotenv
from collage import generate_collage
import argparse
import auth
import shutil
import argparse
import cv2          # pip install opencv-python

# Load environment variables from .env file if it exists
load_dotenv()

# Flask app initialization
app = Flask(__name__)

# Create the parser
parser = argparse.ArgumentParser(description="Video Frame Extraction and Analysis Tool")

# Command-line arguments setup
parser = argparse.ArgumentParser(description="Video Frame Extraction and Analysis")
parser.add_argument("--extract", help="Extract frames from video", action="store_true")
parser.add_argument("--analyze", help="Analyze and move sharp images", action="store_true")
parser.add_argument("--video_path", help="Path to the video file")
parser.add_argument("--output_folder", help="Folder to save extracted frames")
parser.add_argument("--source_folder", help="Folder containing images to analyze")
parser.add_argument("--target_folder", help="Folder to move sharp images to")
parser.add_argument("--sharpness_threshold", help="Sharpness threshold for image analysis", type=int)
parser.add_argument("--generate_collage", help="Generate collage images from extracted frames", action="store_true")
parser.add_argument("--collage_folder", help="Folder to save generated collages")
parser.add_argument("--api_key", help="API key for authentication")
parser.add_argument("--dynamic_threshold", help="Use dynamic thresholding", action="store_true")
parser.add_argument("--sharp_if", help="Image is sharp if value is greater than average", type=int)
parser.add_argument("--total_images_to_extract", help="Indicates the total number of frames that will be extracted", type=int)
args = parser.parse_args()


def calculate_sharpness(image_path: str) -> float:
    """
    Calculate the sharpness of an image.
    Args:
        image_path (str): Path to the image file.

    Returns:
        float: Sharpness score of the image.
    """
    image = cv2.imread(image_path)
    return cv2.Laplacian(image, cv2.CV_64F).var()


def move_sharp_images(source_directory: str, sharp_images_directory: str, sharpness_threshold: int, sharp_if: int = 10, dynamic_threshold: bool = False) -> None:
    """
    Analyzes images for sharpness and moves sharp ones to a designated directory. Can use dynamic or static thresholding.

    Args:
        source_directory (str): Directory containing source images.
        sharp_images_directory (str): Directory to move sharp images.
        sharpness_threshold (int): Threshold for sharpness in static mode.
        sharp_if (int): Value to be added to the average sharpness for dynamic thresholding.
        dynamic_threshold (bool): If True, use dynamic thresholding; otherwise, use static threshold.
    """
    # Ensure sharp images directory exists
    os.makedirs(sharp_images_directory, exist_ok=True)

    # Calculate sharpness for each image and optionally use dynamic thresholding
    if dynamic_threshold:
        sharpness_scores = [calculate_sharpness(os.path.join(source_directory, filename)) 
                            for filename in os.listdir(source_directory) 
                            if filename.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        if sharpness_scores:
            average_sharpness = sum(sharpness_scores) / len(sharpness_scores)
            sharpness_threshold = average_sharpness + sharp_if

    # Move images based on the calculated threshold
    for filename in os.listdir(source_directory):
        if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(source_directory, filename)
            sharpness = calculate_sharpness(image_path)

            if sharpness >= sharpness_threshold:
                shutil.move(image_path, os.path.join(sharp_images_directory, filename))

def extract_frames(video_file_path: str, output_directory: str, frames_to_skip: int = 1, total_images_to_extract: int = 1000000) -> None:
    """
    Extracts frames from a video file and saves them in the output directory.

    Args:
        video_file_path (str): Path to the video file.
        output_directory (str): Directory to save extracted frames.
        frames_to_skip (int): Number of frames to skip between saves.
        total_images_to_extract (int): Total number of frames to extract.
    """
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_file_path}")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_count / total_images_to_extract)

    # Iterate over frames and save as needed
    for i in range(total_images_to_extract):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval * frames_to_skip)
        ret, frame = cap.read()
        if ret:
            frame_file = os.path.join(output_directory, f'frame_{i:04d}.png')
            cv2.imwrite(frame_file, frame)

    cap.release()


# Check for command line arguments
if args.extract:
    # Extract frames functionality
    video_file_path = args.video_path if args.video_path else os.getenv("VIDEO_PATH")
    output_directory = args.output_folder if args.output_folder else os.getenv("OUTPUT_FOLDER")
    if not video_file_path or not output_directory:
        print("Please provide video path and output folder.")
        sys.exit(1)
    extract_frames(video_file_path, output_directory)  # Uncomment when function is implemented

elif args.analyze:
    # Analyze and move sharp images functionality
    source_directory = args.source_folder if args.source_folder else os.getenv("SOURCE_FOLDER")
    sharp_images_directory = args.target_folder if args.target_folder else os.getenv("SHARP_IMAGES_FOLDER")
    sharpness_threshold = args.sharpness_threshold if args.sharpness_threshold else int(os.getenv("SHARPNESS_THRESHOLD", 100))
    dynamic_threshold = args.dynamic_threshold if args.dynamic_threshold else bool(os.getenv("DYNAMIC_THRESHOLD", False))
    sharp_if = sharp_if = args.sharp_if if args.sharp_if else int(os.getenv("SHARP_IF", 10))
    
    if not source_directory or not sharp_images_directory:
        print("Please provide source and target folders for image analysis.")
        sys.exit(1)
    move_sharp_images(source_directory, sharp_images_directory, sharpness_threshold, sharp_if, dynamic_threshold) 
elif args.generate_collage:
    frames_folder = args.frames_folder if args.frames_folder else os.getenv("FRAMES_FOLDER")
    collage_folder = args.collage_folder if args.collage_folder else os.getenv("COLLAGE_FOLDER")

    if not frames_folder or not collage_folder:
        print("Please provide frames folder and collage folder.")
        sys.exit(1)

    generate_collage(frames_folder, collage_folder)
    

@app.before_request
def before_request():
    """
    Global request handler to check for API key authentication.
    """
    if not auth.authenticate_api_key(users):
        return jsonify({"error": "Unauthorized"}), 401


# Flask routes
@app.route('/generate_collage', methods=['POST'])
def generate_collage_route():
    """
    Endpoint to generate a collage from extracted frames.
    """
    frames_folder = request.form.get('frames_folder')
    collage_folder = request.form.get('collage_folder')

    if not frames_folder or not collage_folder:
        return jsonify({"error": "Missing frames folder or collage folder"}), 400

    try:
        collage_count = generate_collage(frames_folder, collage_folder)
        return jsonify({"message": f"Collage generated successfully with {collage_count} collages", "collage_folder": collage_folder})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/extract_frames', methods=['POST'])
def extract_frames_route():
    """
    Extract evenly spaced frames from a video file.
    """
    video_file_path = request.form.get('video_file_path')
    output_directory = request.form.get('output_directory')
    total_images_to_extract = int(request.form.get('total_images_to_extract', 1000000))  # Get total_images_to_extract from the request

    if not video_file_path or not output_directory:
        return jsonify({"error": "Missing video file path or output directory"}), 400

    # Create a unique folder for extracted frames
    unique_folder = str(uuid.uuid4())
    frames_folder = os.path.join(output_directory, unique_folder)
    os.makedirs(frames_folder)

    try:
        # Get the video's duration using FFprobe
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file_path]
        duration = float(subprocess.check_output(ffprobe_cmd))

        # Calculate the frame interval based on the total images requested and duration
        frame_interval = int(duration * 1000 / total_images_to_extract)

        # Use FFmpeg to extract frames with the calculated frame interval
        subprocess.run(['ffmpeg', '-i', video_file_path, '-vf', f'select=not(mod(n\,{frame_interval}))', os.path.join(frames_folder, 'frame_%04d.png')])
        return jsonify({"message": "Frames extracted successfully", "frames_folder": unique_folder})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze_images', methods=['POST'])
def analyze_images_route():
    """
    Analyze images and move sharp images to a target directory.
    """
    source_directory = request.form.get('source_directory')
    sharp_images_directory = request.form.get('sharp_images_directory')
    sharpness_threshold = int(request.form.get('sharpness_threshold', 100))

    if not source_directory or not sharp_images_directory:
        return jsonify({"error": "Missing source or target directory"}), 400

    try:
        # Ensure the target directory exists
        os.makedirs(sharp_images_directory, exist_ok=True)

        # Loop through images in the source directory
        for filename in os.listdir(source_directory):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(source_directory, filename)

                # Calculate image sharpness using OpenCV
                image = cv2.imread(image_path)
                sharpness = cv2.Laplacian(image, cv2.CV_64F).var()

                if sharpness >= sharpness_threshold:
                    # Move sharp images to the target directory
                    shutil.move(image_path, os.path.join(sharp_images_directory, filename))

        return jsonify({"message": "Images analyzed and sharp images moved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main function and build .env if missing
if __name__ == "__main__":
    # Check for required environment variables and prompt if missing
    required_env_vars = ["VIDEO_PATH", "OUTPUT_FOLDER", "SOURCE_FOLDER", "SHARP_IMAGES_FOLDER", "SHARPNESS_THRESHOLD"]
    missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_env_vars:
        print(f"Missing environment variables: {', '.join(missing_env_vars)}")
        for var in missing_env_vars:
            os.environ[var] = input(f"Enter value for {var}: ")

    app.run(debug=True)
