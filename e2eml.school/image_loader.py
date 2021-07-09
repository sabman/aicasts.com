import os
from PIL import Image
import numpy as np
import lodgepole.image_tools as lit


def load_image(path, imagename, patch_size):
    img = np.asarray(Image.open(os.path.join(path, imagename))) / 255

    # Convert color images to grayscale
    if len(img.shape) == 3:
        img = lit.rgb2gray_approx(img)

    n_rows, n_cols = img.shape
    assert len(img.shape) == 2
    assert n_rows > patch_size
    assert n_cols > patch_size

    # Pad out to a multiple of patch_size
    n_rows_pad = int(np.ceil(n_rows / patch_size)) * patch_size
    n_cols_pad = int(np.ceil(n_cols / patch_size)) * patch_size

    padded = np.pad(img, ((0, n_rows_pad - n_rows), (0, n_cols_pad - n_cols)))

    assert np.sum(np.isnan(padded)) == 0

    return padded


