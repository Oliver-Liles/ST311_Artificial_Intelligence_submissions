import cv2
import os

def extract_frames(video_path, output_dir):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    # Create output directory if it doesn’t exist
    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0
    
    # Read frames until the video ends
    while True:
        ret, frame = cap.read()
        if not ret:  # Break when no more frames are available
            break
        # Save each frame as a JPEG file
        frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    # Release the video capture object
    cap.release()

# Set directories
VIDEO_DIR = "Videos/Tests"  # Replace with your video folder path
FRAMES_DIR = "Frames/Tests"      # Replace with where you want frames saved

# Process all MP4 videos
for video_file in os.listdir(VIDEO_DIR):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(VIDEO_DIR, video_file)
        output_dir = os.path.join(FRAMES_DIR, video_file.replace('.mp4', ''))
        extract_frames(video_path, output_dir)
