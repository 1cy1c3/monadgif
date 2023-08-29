import streamlit as st
import io
from io import BytesIO
import numpy as np
from PIL import ImageSequence, Image, ImageDraw, ImageFont
import pygame
import time
from functions.converter import ASCIIConverter

ss = st.session_state


def _get_average_luminance(image):
    """Return average value of grayscale value."""
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


def extract_frames_as_bytesio(file):
    frames = []

    # Open the image file
    with Image.open(file) as img:
        for frame in ImageSequence.Iterator(img):
            byte_io = io.BytesIO()

            # Convert the frame to RGB mode before saving it
            frame_rgb = frame.convert('RGB')
            frame_rgb.save(byte_io, format='JPEG')

            byte_io.seek(0)
            frames.append(byte_io)

    return frames


def _extract_frames_as_bytesio(gif_path):
    """Extract each frame from a GIF as a BytesIO object and replace transparent pixels with white."""
    with Image.open(gif_path) as im:
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]

    byte_io_frames = []
    for frame_img in frames:
        # If the image has an alpha (transparency) channel
        if frame_img.mode == 'RGBA':
            # Create a white image of the same size as the frame
            white_bg = Image.new('RGBA', frame_img.size, (255, 255, 255))
            # Paste the frame onto the white image
            white_bg.paste(frame_img, (0, 0), frame_img)
            # Convert to RGB (discard alpha)
            frame_rgb = white_bg.convert('RGB')
        else:
            frame_rgb = frame_img.convert('RGB')

        byte_io = io.BytesIO()
        frame_rgb.save(byte_io, format='JPEG')
        byte_io_frames.append(byte_io)

    return byte_io_frames


@st.cache_data()
def generate_ascii_gif(frames_io):
    converter = ASCIIConverter()
    frames = converter.generate_ascii_art_from_gif(frames_io)

    # Initialize pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = ss["width"], ss["height"]
    BACKGROUND_COLOR = (131, 110, 249)
    FONT_COLOR = (38, 0, 31)
    FONT_SIZE = 5
    SPEED = 0.05

    # Set up the display and font
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MONAD ASCII")
    font = pygame.font.Font("assets/fonts/CourierPrime-Italic.ttf", FONT_SIZE)

    ascii_frames = strip_whitespace_from_ascii_frames(frames)

    collected_frames = []

    # Loop through all frames only once
    for current_frame in ascii_frames:
        # Drawing the background
        screen.fill(BACKGROUND_COLOR)

        # Drawing the ASCII art for the current frame
        for idx, line in enumerate(current_frame):
            rendered_line = font.render(line, True, FONT_COLOR)
            screen.blit(rendered_line, (WIDTH // 2 - rendered_line.get_width() // 2,
                                        HEIGHT // 2 + idx * FONT_SIZE - FONT_SIZE * len(current_frame) // 2))

        # Capture the current frame
        pygame_image = pygame.surfarray.array3d(pygame.display.get_surface())
        frame_image = Image.fromarray(pygame_image.transpose([1, 0, 2]))
        collected_frames.append(frame_image)

        # Delay before moving to the next frame
        time.sleep(SPEED)

    pygame.quit()  # Quit pygame after processing all frames

    # Save the frames as a GIF using BytesIO
    gif_io = BytesIO()
    collected_frames[0].save(gif_io, format='GIF', save_all=True, append_images=collected_frames, optimize=False,
                             duration=100, loop=0)
    gif_io.seek(0)
    return gif_io


@st.cache_data(show_spinner=False)
def get_sign_width():
    font_size = 5
    # Load the font and set its size
    font_path = "assets/fonts/CourierPrime-Italic.ttf"  # Replace with the path to your font
    font = ImageFont.truetype(font_path, font_size)

    # Create a blank image and get a drawing context
    img = Image.new('L', (10, 10), color=255)  # Here 10x10 is an arbitrary size
    d = ImageDraw.Draw(img)

    # Get the size of "@" character
    width, height = d.textsize("@", font=font)
    return width, height


def strip_whitespace_from_ascii_frames(ascii_frames):
    stripped_frames = []
    for index, frame in enumerate(ascii_frames):

        stripped_frame = [line for line in frame if line.strip()]

        # Ensure at least one row remains for every frame, especially the first
        if not stripped_frame:
            stripped_frame.append(' ')

        stripped_frames.append(stripped_frame)

    return stripped_frames
