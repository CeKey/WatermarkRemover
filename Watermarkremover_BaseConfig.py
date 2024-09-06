import cv2
import numpy as np
import subprocess

# Path to the input video
input_video_path = 'inputVideo.mp4'
output_video_path = 'tempVideo.mp4'
audio_path = 'audio.mp3'
output_video_with_audio_path = 'FinalVersionVideo.mp4'

# Open the video
cap = cv2.VideoCapture(input_video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Define the region to be masked (top right corner)
# Adjust the values according to the position and size of the text
top_right_corner_start = (frame_width - 405, 20)  # (x, y)
top_right_corner_end = (frame_width, 100)  # (x, y)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Create a mask for the text area
    mask = np.zeros(frame.shape, dtype=np.uint8)
    cv2.rectangle(mask, top_right_corner_start, top_right_corner_end, (255, 255, 255), -1)
    
    # Apply inpainting to remove text
    inpainted_frame = cv2.inpaint(frame, cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), 3, cv2.INPAINT_TELEA)
    
    # Write the frame to the output video
    out.write(inpainted_frame)

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()

# Extract audio from the input video
def run_ffmpeg_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("Output:\n", result.stdout)
        print("Error:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print("An error occurred:\n", e.output)
        print("Error details:\n", e.stderr)
        raise

# Extract audio from the input video
run_ffmpeg_command(['C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', input_video_path, '-q:a', '0', '-map', 'a', audio_path])

# Combine the audio with the edited video
run_ffmpeg_command(['C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', output_video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_video_with_audio_path])

print("The final video with audio is available at:", output_video_with_audio_path)
