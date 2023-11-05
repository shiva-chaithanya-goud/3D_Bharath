#DCT ENCODING
%time
from skimage.io import imread, imsave
from skimage.color import rgb2ycbcr, ycbcr2rgb
from skimage import img_as_float, img_as_ubyte
import numpy as np
from PIL import PngImagePlugin

PngImagePlugin.MAX_TEXT_CHUNK = 500 * (1024**2)
_quality = 70
img_path = '/content/drive/MyDrive/colab/pdc/parrot_big.png'
secret_file_path = '/content/drive/MyDrive/colab/pdc/text_512.txt'
stego_img_path = 'output1'

def dct_hide(img, filename, out_name='output', N=8, difference=False):
    original = img.copy()
    a, b = img.shape[:2]
    c = 3 if len(img.shape) == 3 else 1
    data = file_to_bin(filename)

    if len(data) > (a // 8) * (b // 8) * 3:
        print("File is too large")
        return
    
    index = 0
    if c == 3:
        newimg = rgb2ycbcr(img)
        Y =  dct_process_channel(newimg[..., 0], _quality)
        Cb = dct_process_channel(newimg[..., 1], _quality)
        Cr = dct_process_channel(newimg[..., 2], _quality)
        newimg = np.dstack((Y, Cb, Cr))
        for i in range(0, a, 8):
            for j in range(0, b, 8):
                for k in range(c):
                    if index + 1 < len(data):
                        newimg[i + 1, j + 1, k] += -(int(newimg[i + 1, j + 1, k]) % 2) + int(data[index])
                        index += 1
        Y =  idct_process_channel(newimg[..., 0], _quality)
        Cb = idct_process_channel(newimg[..., 1], _quality)
        Cr = idct_process_channel(newimg[..., 2], _quality)
        newimg = np.dstack((Y, Cb, Cr))
        img = np.clip(0, 1.0, ycbcr2rgb(newimg))
        img = img_as_ubyte(img)
        if difference:
            generate_difference(original, img)
        imsave(out_name + '.png', img)

try:
    img = imread(img_path)
    file = open(secret_file_path)
except FileNotFoundError:
    print("This file does not exist.")
    exit()

dct_hide(img, secret_file_path, stego_img_path, difference=True)

