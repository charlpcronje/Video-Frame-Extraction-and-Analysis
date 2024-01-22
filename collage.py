import numpy as np
import cv2

def generate_collage(frames_folder, collage_folder):
    """
    Generate collage images from extracted frames.
    """
    os.makedirs(collage_folder, exist_ok=True)

    frames = sorted(os.listdir(frames_folder))
    collage_count = 0
    frames_per_collage = 50

    for i in range(0, len(frames), frames_per_collage):
        collage = np.zeros((720, 1280, 3), dtype=np.uint8)  # Adjust dimensions as needed
        frame_subset = frames[i:i + frames_per_collage]

        for idx, frame_name in enumerate(frame_subset):
            frame_path = os.path.join(frames_folder, frame_name)
            frame = cv2.imread(frame_path)
            
            # Resize frames if needed
            frame = cv2.resize(frame, (160, 90))

            row = idx // 10
            col = idx % 10
            x_offset = col * frame.shape[1]
            y_offset = row * frame.shape[0]

            collage[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame

            # Add frame number and resolution to the collage
            text = f"Frame {i + idx + 1} - {frame.shape[1]}x{frame.shape[0]}"
            cv2.putText(collage, text, (x_offset + 5, y_offset + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        collage_path = os.path.join(collage_folder, f'collage_{collage_count}.png')
        cv2.imwrite(collage_path, collage)
        collage_count += 1

    return collage_count
