import tkinter as tk
from PIL import Image, ImageTk
import os
import csv
from pathlib import Path

class LabelTool:
    def __init__(self, root, frames_dir_list, output_csv, output_dir):
        self.root = root
        self.frames_dir_list = frames_dir_list  # List of frame directories
        self.current_dir_idx = 0  # Index for current directory in frames_dir_list
        self.current_video_idx = 0
        self.current_frame_idx = 0
        self.hit_frames = {}
        self.output_csv = output_csv
        self.output_dir = output_dir
        self.selected_frames = set()  # Track selected frames for current video
        
        # Load existing CSV data
        self.existing_videos = self.load_existing_csv()
        
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        
        # Status label
        self.status_label = tk.Label(root, text="No frames selected")
        self.status_label.pack()
        
        # Bind keyboard shortcuts
        self.root.bind('<Left>', self.prev_frame)
        self.root.bind('<Right>', self.next_frame)
        self.root.bind('<space>', self.toggle_frame_selection)
        self.root.bind('<Return>', self.finish_current_video)  # Enter key to move to next video
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load video directories from the current frames directory
        self.load_current_dir_videos()
        
    def load_existing_csv(self):
        csv_path = os.path.join(self.output_dir, self.output_csv)
        existing_videos = set()
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_videos.add(row['video_name'])
        return existing_videos

    def load_current_dir_videos(self):
        """Load video directories from the current frames directory"""
        current_frames_dir = self.frames_dir_list[self.current_dir_idx]
        self.video_dirs = [os.path.join(current_frames_dir, d) for d in os.listdir(current_frames_dir) 
                         if os.path.isdir(os.path.join(current_frames_dir, d))]
        
        # Reset video index and skip processed videos
        self.current_video_idx = 0
        while (self.current_video_idx < len(self.video_dirs) and 
               os.path.basename(self.video_dirs[self.current_video_idx]) in self.existing_videos):
            self.current_video_idx += 1
            
        if self.current_video_idx < len(self.video_dirs):
            self.load_video()
        else:
            self.move_to_next_dir()

    def load_video(self):
        self.current_video = self.video_dirs[self.current_video_idx]
        self.frames = [os.path.join(self.current_video, f) for f in os.listdir(self.current_video) if f.endswith('.jpg')]
        self.frames.sort()
        self.current_frame_idx = 0
        self.selected_frames = set()  # Reset selected frames for new video
        self.update_status_label()
        self.show_frame()

    def show_frame(self):
        frame_path = self.frames[self.current_frame_idx]
        img = Image.open(frame_path)
        img = img.resize((640, 480), Image.LANCZOS)
        
        # Add visual indicator if frame is selected
        if frame_path in self.selected_frames:
            # Draw a green border around selected frames
            img_draw = ImageTk.PhotoImage(img)
            self.img_tk = img_draw
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
            self.canvas.create_rectangle(0, 0, 640, 480, outline='green', width=5)
        else:
            self.img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
            
        # Display frame number
        frame_info = f"Frame {self.current_frame_idx + 1}/{len(self.frames)}"
        self.canvas.create_text(320, 20, text=frame_info, fill="white", font=("Arial", 14))

    def prev_frame(self, event):
        if self.current_frame_idx > 0:
            self.current_frame_idx -= 1
            self.show_frame()

    def next_frame(self, event):
        if self.current_frame_idx < len(self.frames) - 1:
            self.current_frame_idx += 1
            self.show_frame()

    def toggle_frame_selection(self, event):
        current_frame = self.frames[self.current_frame_idx]
        
        if current_frame in self.selected_frames:
            self.selected_frames.remove(current_frame)
        else:
            self.selected_frames.add(current_frame)
            
        self.update_status_label()
        self.show_frame()  # Refresh to show selection status

    def update_status_label(self):
        video_name = os.path.basename(self.current_video)
        self.status_label.config(text=f"Video: {video_name} - Selected {len(self.selected_frames)} frames. Press Enter when done.")

    def finish_current_video(self, event):
        if not self.selected_frames:
            # If no frames selected, ask for confirmation
            if not tk.messagebox.askyesno("Confirm", "No frames selected. Move to next video anyway?"):
                return
        
        video_name = os.path.basename(self.current_video)
        self.hit_frames[video_name] = list(self.selected_frames)
        
        print(f"Selected {len(self.selected_frames)} frames for {video_name}:")
        for frame in self.selected_frames:
            print(f" - {frame}")
        
        self.current_video_idx += 1
        while (self.current_video_idx < len(self.video_dirs) and 
               os.path.basename(self.video_dirs[self.current_video_idx]) in self.existing_videos):
            self.current_video_idx += 1
            
        if self.current_video_idx < len(self.video_dirs):
            self.load_video()
        else:
            self.move_to_next_dir()

    def move_to_next_dir(self):
        """Move to the next directory in the list"""
        self.current_dir_idx += 1
        if self.current_dir_idx < len(self.frames_dir_list):
            print(f"Moving to next directory: {self.frames_dir_list[self.current_dir_idx]}")
            self.load_current_dir_videos()
        else:
            print("All directories processed!")
            self.save_csv()
            self.root.quit()

    def save_csv(self):
        os.makedirs(self.output_dir, exist_ok=True)
        csv_path = os.path.join(self.output_dir, self.output_csv)
        file_exists = Path(csv_path).is_file()
        
        with open(csv_path, 'a' if file_exists else 'w', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["video_name", "frame_path", "is_hit_frame"])
            
            for video_name, frame_paths in self.hit_frames.items():
                if video_name in self.existing_videos:
                    continue
                    
                video_dir = os.path.dirname(frame_paths[0]) if frame_paths else None
                if video_dir:
                    all_frames = [os.path.join(video_dir, frame) 
                                for frame in os.listdir(video_dir) 
                                if frame.endswith('.jpg')]
                    all_frames.sort()
                    
                    for frame_path in frame_paths:
                        writer.writerow([video_name, frame_path, 1])
                    non_hit_frames = [f for f in all_frames if f not in frame_paths]
                    for frame_path in non_hit_frames:
                        writer.writerow([video_name, frame_path, 0])
                    
            print(f"Data appended to {csv_path}")

    def on_closing(self):
        self.save_csv()
        self.root.destroy()

# Run the tool
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Multi-Frame Label Tool")
    
    # Import messagebox for confirmations
    import tkinter.messagebox
    
    FRAMES_DIR_LIST = [
        "Frames/Outdoor Field/Cross-court Shot/Top-View",
        "Frames/Outdoor Field/Straight Shot/Top-View",
        "Frames/Indoor Field/Cross-court Shot/Top-View",
        "Frames/Indoor Field/Straight Shot/Top-View",
        "Frames/Misc"    
    ]  # List of frame directories to cycle through
    OUTPUT_DIR = "Frames"
    tool = LabelTool(root, FRAMES_DIR_LIST, "hit_frames.csv", OUTPUT_DIR)
    root.mainloop()
