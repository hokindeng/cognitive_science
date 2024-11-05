import os
import cv2

def extract_10th_frame(root_dir):
    # Walk through the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file is a .mov file
            if filename.lower().endswith('.mov'):
                mov_path = os.path.join(dirpath, filename)

                # Create the output .png file path
                base_name = os.path.splitext(filename)[0]
                png_filename = f"{base_name}_frame10.png"
                png_path = os.path.join(dirpath, png_filename)

                # Open the video file using OpenCV
                cap = cv2.VideoCapture(mov_path)

                if not cap.isOpened():
                    print(f"Failed to open {mov_path}")
                    continue

                frame_number = 9  # Frame numbers start from 0
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()

                if ret:
                    # Save the frame as a PNG file
                    cv2.imwrite(png_path, frame)
                    print(f"Extracted frame {frame_number + 1} from {mov_path} to {png_path}")
                else:
                    print(f"Failed to read frame {frame_number + 1} from {mov_path}")

                cap.release()


if __name__ == "__main__":
    # Replace '.' with the path to your target directory if needed
    root_directory = os.getcwd()
    extract_10th_frame(root_directory)