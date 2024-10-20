import cv2
import numpy as np
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
import tkinter as tk
from tkinter import filedialog
from controlnet_aux import OpenposeDetector
import matplotlib.pyplot as plt
from PIL import Image
import os

def choose_input_image():
    root = tk.Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title="Choose an image", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    return file_path

# Load OpenPose ControlNet model
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-openpose", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
)

# Move the model to GPU
pipe.to("cuda")

# Initialize OpenPose detector
openpose = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')

# Choose input image
input_image_path = choose_input_image()
if not input_image_path:
    print("Didn't choose an image, exiting.")
    exit()

# Load input image
input_image = load_image(input_image_path)

# Apply OpenPose detection
openpose_image = openpose(input_image)

# Get user input for prompts
prompt = input("Please enter your prompt: ")
if not prompt:
    print("Prompt cannot be empty, exiting.")
    exit()

negative_prompt = input("Please enter a negative prompt (optional): ")

# Generate new image
output_image = pipe(
    prompt=prompt,
    image=openpose_image,
    negative_prompt=negative_prompt,
    num_inference_steps=30,
    guidance_scale=7.5,
).images[0]

# Save output image
output_path = os.path.splitext(input_image_path)[0] + "_generated.png"
output_image.save(output_path)
print(f"Image saved to: {output_path}")

# Display images
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(input_image)
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(openpose_image)
plt.title("OpenPose Result")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(output_image)
plt.title("Generated Image")
plt.axis('off')

plt.tight_layout()
plt.show()