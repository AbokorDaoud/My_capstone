import os

# Create directories if they don't exist
directories = [
    'static',
    'static/images',
    'media',
    'media/profile_pics',
    'media/post_images',
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f'Created directory: {directory}')
