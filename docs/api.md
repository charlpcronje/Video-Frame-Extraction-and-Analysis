## API Routes

- `/extract_frames`: Extract frames from a video file with optional frame skipping and total images to extract.
- `/analyze_images`: Analyze images for sharpness and move sharp images to a target directory.
- `/generate_collage`: Generate collage images from extracted frames.


## New API Endpoint: `/generate_collage`

- **POST `/generate_collage`**
  - **Description**: Generates a collage from frames.
  - **Request**:
    - `frames_folder`: Path to the folder containing frames.
    - `collage_folder`: Path where the collage will be saved.
  - **Response**: JSON indicating success and path to the generated collage.
  - **Error Responses**: Appropriate error messages for missing parameters or internal errors.
```

## Authentication

API key authentication is required for all endpoints. Please provide your API key in the request header for authentication.
```
