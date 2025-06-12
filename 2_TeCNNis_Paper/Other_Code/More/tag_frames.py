import tkinter as tk
from PIL import Image, ImageTk
import os

class LabelTool:
    def __init__(self, root, video_dirs, output_csv, output_dir):
        self.root = root
        self.video_dirs = video_dirs  # List of folders containing frames
        self.current_video_idx = 0
        self.current_frame_idx = 0
        self.hit_frames = {}  # Store video name and hit frame
        self.output_csv = output_csv  # CSV filename
        self.output_dir = output_dir  # Directory to save CSV
        
        # Set up the canvas to display frames
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        
        # Bind keyboard shortcuts
        self.root.bind('<Left>', self.prev_frame)    # Previous frame
        self.root.bind('<Right>', self.next_frame)   # Next frame
        self.root.bind('<space>', self.select_hit_frame)  # Mark hit frame

        # Bind the window close event to save and exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load the first video’s frames after canvas is initialized
        self.load_video()
        
    def load_video(self):
        # Load frames from the current video’s folder
        self.current_video = self.video_dirs[self.current_video_idx]
        self.frames = [os.path.join(self.current_video, f) for f in os.listdir(self.current_video) if f.endswith('.jpg')]
        self.frames.sort()  # Sort frames by name (e.g., frame_0001.jpg)
        self.current_frame_idx = 0
        self.show_frame()

    def show_frame(self):
        # Display the current frame
        frame_path = self.frames[self.current_frame_idx]
        img = Image.open(frame_path)
        img = img.resize((640, 480), Image.LANCZOS)  # Resize for display
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def prev_frame(self, event):
        # Go to the previous frame
        if self.current_frame_idx > 0:
            self.current_frame_idx -= 1
            self.show_frame()

    def next_frame(self, event):
        # Go to the next frame
        if self.current_frame_idx < len(self.frames) - 1:
            self.current_frame_idx += 1
            self.show_frame()

    def select_hit_frame(self, event):
        # Record the hit frame and move to the next video
        hit_frame = self.frames[self.current_frame_idx]
        video_name = os.path.basename(self.current_video)
        self.hit_frames[video_name] = hit_frame
        print(f"Selected hit frame for {video_name}: {hit_frame}")
        
        self.current_video_idx += 1
        if self.current_video_idx < len(self.video_dirs):
            self.load_video()  # Load next video
        else:
            self.save_csv()  # Save results when done
            self.root.quit()

    def save_csv(self):
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        # Full path for the CSV file
        csv_path = os.path.join(self.output_dir, self.output_csv)
        # Save hit frame data to CSV
        with open(csv_path, 'w') as f:
            f.write("video_name,hit_frame\n")
            for video, frame in self.hit_frames.items():
                f.write(f"{video},{frame}\n")
        print(f"CSV saved to {csv_path}")

    def on_closing(self):
        # Save CSV and close the window when "X" is clicked
        self.save_csv()
        self.root.destroy()

# Run the tool
root = tk.Tk()
FRAMES_DIR = "Frames/Outdoor Field/Cross-court Shot/Top-View"  # Your frames folder path
OUTPUT_DIR = "Frames"  # Specify your desired output directory
video_dirs = [os.path.join(FRAMES_DIR, d) for d in os.listdir(FRAMES_DIR) if os.path.isdir(os.path.join(FRAMES_DIR, d))]
tool = LabelTool(root, video_dirs, "hit_frames.csv", OUTPUT_DIR)
root.mainloop()
