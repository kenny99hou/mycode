from PIL import Image, ImageDraw

# Create a blank image with white background
width, height = 400, 300
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw a red rectangle
draw.rectangle([50, 50, 350, 250], fill="red", outline="black")

# Draw some text
draw.text((150, 130), "Hello Image!", fill="blue")

# Save the image
image.save("generated_image.png", "PNG")
print("Image generated successfully!")
