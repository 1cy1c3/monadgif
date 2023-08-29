import io
import streamlit as st
from PIL import Image

import functions.ascii as _ascii

ss = st.session_state


class ASCIIConverter:

    def __init__(self):
        # 70 levels of gray
        self._gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        # 10 levels of gray
        self._gscale2 = '@%#*+=-:. '
        self.cols = None

    def _convert_to_ascii(self, input_image, scale=1, more_levels=True):
        """Convert a BytesIO image representation or Image object to an ASCII representation."""
        if isinstance(input_image, str):
            image = Image.open(input_image).convert('L')
        elif isinstance(input_image, io.BytesIO):
            input_image.seek(0)  # Ensure we're at the start of the BytesIO object
            image = Image.open(input_image).convert('L')
        else:
            # Assuming it's already an Image object
            image = input_image.convert('L')

        W, H = image.size
        ascii_px = _ascii.get_sign_width()
        ascii_px_w = ascii_px[0]
        ascii_px_h = ascii_px[1]

        ss["width"], ss["height"] = W, H
        self.cols = int(W / ascii_px_w)
        w = W / self.cols
        h = ascii_px_h
        rows = int(H / ascii_px_h)

        if self.cols > W or rows > H:
            raise ValueError("Image too small for specified cols!")

        ascii_image = []
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)
            if j == rows - 1:
                y2 = H
            ascii_image.append("")
            for i in range(self.cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w)
                if i == self.cols - 1:
                    x2 = W
                img = image.crop((x1, y1, x2, y2))
                avg = int(_ascii._get_average_luminance(img))
                # Add a check for pure white and map it to space
                if avg == 255:
                    gs_val = ' '
                elif more_levels:
                    gs_val = self._gscale1[int((avg * 70) / 255)]
                else:
                    gs_val = self._gscale2[int((avg * 10) / 255)]
                ascii_image[j] += gs_val
        return ascii_image

    def generate_ascii_art_from_gif(self, frames_io, scale=1, more_levels=False):
        if isinstance(frames_io, str):
            frames = _ascii._extract_frames_as_bytesio(frames_io)
        else:
            frames = frames_io

        ascii_frames = []
        for frame_io in frames:
            frame_io.seek(0)  # Reset to the beginning of the BytesIO
            ascii_img = self._convert_to_ascii(frame_io, scale, more_levels)
            ascii_frames.append(ascii_img)

        return ascii_frames
