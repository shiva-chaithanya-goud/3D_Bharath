#DCT DECODING
%time
from skimage.io import imread
from skimage.color import rgb2ycbcr
import numpy as np
import sys

_quality = 70
input_file = "/content/output1.png"
output_file = "output_file"

img = imread(input_file)
a, b = img.shape[:2]
c = 3 if len(img.shape) == 3 else 1

if c == 3:
    bitstream = []
    newimg = rgb2ycbcr(img)
    Y = dct_process_channel(newimg[..., 0], _quality)
    Cb = dct_process_channel(newimg[..., 1], _quality)
    Cr = dct_process_channel(newimg[..., 2], _quality)
    newimg = np.dstack((Y, Cb, Cr))
    for i in range(0, a, 8):
        for j in range(0, b, 8):
            for k in range(c):
                bitstream.append(str(int(abs(newimg[i + 1, j + 1, k])) % 2))
    bin_to_file(bitstream, output_file)
