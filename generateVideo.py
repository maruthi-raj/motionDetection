import os
import cv2 
from PIL import Image 
  
# Checking the current directory path
print(os.getcwd()) 
  
# Folder which contains all the images from which video is to be generated
directory=r"E:\\videos"
os.chdir(directory)

path = r"E:\\videos"

# Video Generating function
def generate_video():
    image_folder="."
    video_name = 'mygeneratedvideo.avi'
    os.chdir(path)
    start='14-11-2021_22-08-43.JPG'
    end='2-12-2021_22-42-46.JPG'
    images = [img for img in os.listdir(image_folder) if(img>=start and img<=end)]

    # Array images should only consider the image files ignoring others if any
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
  
    frame = cv2.imread(os.path.join(image_folder, images[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MJPG'), 2, (width, height))
    # Appending the images to the video one by one
    for image in images: 
        video.write(cv2.imread(os.path.join(image_folder, image))) 
    
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated

generate_video()