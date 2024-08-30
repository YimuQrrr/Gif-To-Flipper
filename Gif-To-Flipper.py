import os
import sys
from PIL import Image

def convert_frame_to_2color(frame, threshold=128):
    # Convert to grayscale
    grayscale_frame = frame.convert("L")
    # Apply threshold
    return grayscale_frame.point(lambda x: 0 if x < threshold else 255, "1")


def save_frames_and_manifest(frames, folder_name):
    # Create the folder
    os.makedirs(folder_name, exist_ok=True)
    # Save frames as PNG
    frame_filenames = []
    for i, frame in enumerate(frames):
        frame_path = os.path.join(folder_name, f"frame_{i}.png")
        frame.save(frame_path, format="PNG")
        frame_filenames.append(str(i))
    # Create meta.txt
    manifest_path = os.path.join(folder_name, "meta.txt")
    with open(manifest_path, "w") as manifest_file:
        manifest_file.write(
            f"""Filetype: Flipper Animation
Version: 1

Width: 128
Height: 64
Passive frames: {len(frames)}
Active frames: 0
Frames order: {" ".join(frame_filenames)}
Active cycles: 0
Frame rate: 6
Duration: 28800
Active cooldown: 0

Bubble slots: 0
""")

# Convert GIF file to two-color and adjust resolution
def process_gif(input_path):
    folder_name = os.path.splitext(os.path.basename(input_path))[0]
    image = Image.open(input_path)
    frames = []
    try:
        while True:
            frame = convert_frame_to_2color(image)
            frame = frame.resize((128, 64))
            frames.append(frame)
            image.seek(image.tell() + 1)
    except EOFError:
        pass
    save_frames_and_manifest(frames, folder_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please drag and drop a GIF file onto this script.")
    else:
        process_gif(sys.argv[1])
