from PIL import Image, ImageFilter
import random
import os
import numpy as np
import scipy
import scipy.misc

PIX_2_PIX_CROP = True
SIGMA = 12

SLICE_SIZE_X = 8
SLICE_SIZE_Y = 12
NUM_OF_CROPS = 16
RESIZE_MAX_X = SLICE_SIZE_X*NUM_OF_CROPS
RESIZE_MAX_Y = SLICE_SIZE_Y*NUM_OF_CROPS
import os.path

row_size = 16
margin = 0

def crop(infile, height, width):
    if isinstance(infile, str):
        im = Image.open(infile)
    else:
        im = Image.fromarray(infile)

    imgwidth, imgheight = im.size

    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def crop(infile, height, width):
    im = Image.open(infile)

    imgwidth, imgheight = im.size

    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def slice_img(
        infile,
        folder_dir='./img',
        height=SLICE_SIZE_Y,
        width=SLICE_SIZE_X,
        save=True,
        montage_n=1):
    imgs = []
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    for k, piece in enumerate(crop(infile, height, width), 0):
        img = Image.new('RGB', (width, height), 255)
        img.paste(piece)
        path = os.path.join(
               folder_dir, "s{}_{}_{}.png".format(SIGMA, montage_n, k))
        img = np.asarray(img)
        img = img.astype('uint8')
        imgs.append(img)
        scipy.misc.imsave(path, img)

    return imgs

def generate_montage(filenames, output_fn):
    images = [Image.open(filename) for filename in filenames]

    width = max(image.size[0] + margin for image in images)*row_size
    height = sum(image.size[1] + margin for image in images)
    montage = Image.new(mode='RGBA', size=(width, height), color=(0,0,0,0))

    max_x = 0
    max_y = 0
    offset_x = 0
    offset_y = 0
    for i,image in enumerate(images):
        montage.paste(image, (offset_x, offset_y))

        max_x = max(max_x, offset_x + image.size[0])
        max_y = max(max_y, offset_y + image.size[1])

        if i % row_size == row_size-1:
            offset_y = max_y + margin
            offset_x = 0
        else:
            offset_x += margin + image.size[0]

    montage = montage.crop((0, 0, max_x, max_y))
    montage.save(output_fn)


def get_images(folder_dir):
    imgs = [
        np.array(Image.open(os.path.join(folder_dir, fname)))
        for fname in os.listdir(folder_dir)
        if fname.endswith('.png')]
    imgs = np.array(imgs).astype(np.float32)
    imgs = imgs / 255.0
    return imgs

def get_filenames(folder_dir):
    return [
        os.path.join(folder_dir, fname)
        for fname in os.listdir(folder_dir)
            if fname.endswith('.png')]



# print(infile)

# im = Image.open(infile)

fnames = get_filenames("./img_single")
# print(len(fnames))
lst = [None] * 256;
fnames = list(map(lambda fname: random.choice(fnames), lst))


# print(images)

# infile = "./in/Plac1d_640x300tileset.png"
# slice_img(infile, montage_n=3)

# montage(images)
generate_montage(fnames, "curses_640x300.png")
