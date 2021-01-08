from scipy.ndimage import label, generate_binary_structure

def filter_less_than(arr, k):
    return arr[np.nonzero(arr < k)]

def filter_equals(arr, k):
    print("arr", type(arr), arr.shape)
    foo = arr[np.nonzero(arr == k)]
    foo.reshape(arr.shape)
    print("foo", type(foo), foo.shape)
    return foo

def test1(image):
    s = ndimage.generate_binary_structure(2,1)
    labeled_array, numpatches = ndimage.label(image, s)
    sizes = ndimage.sum(image, labeled_array, range(1, numpatches + 1))
    max_label = np.where(sizes == sizes.max())[0] + 1
    output = np.asarray(labeled_array == max_label, np.uint8)

def label_binary(image_file, img_count=5, thresh=128):
    import os
    import numpy as np
    from PIL import Image
    from scipy.ndimage import label
    im_gray =np.array(Image.open(image_file).convert("L"))

    im_bool = im_gray > thresh
    maxval = 255

    im_bin = (im_gray > thresh) * maxval
    im_invert = (255 - im_bin)

    # https://stackoverflow.com/questions/52078231/get-a-quanity-of-pixels-with-specific-color-at-image-python-opencv

    Image.fromarray(np.uint8(im_bin)).save('numpy_binarization.png')

#    labeled, nr_objects = scipy.ndimage.label(im_bin, output=np.uint8)
#    im_bin_shaped= np.ndarray(shape=im_bin.shape, dtype=np.uint8)

#    labeled, nr_objects = scipy.ndimage.label(im_invert, output=np.uint8)
    labeled, nr_objects = label(im_invert)
    # index regions by size => index
    labels_by_size = {}
    for label in range(nr_objects):
        labels_by_size[np.count_nonzero(labeled == label)] = label;

# still learning this
#    sorted_regions_by_size = {k: v for k, v in sorted(regions_by_size.items(), key=lambda item: (item[0], item[1]), reverse=True)}
    sorted_regions_by_size = []
    labels_by_size_sorted = sorted(labels_by_size.items(), key=lambda item: item[0], reverse=True)
    count = 0
    ncol = 3
    nrow = (img_count - 1) // ncol + 1
    fig, axes = plt.subplots(ncol, nrow, figsize=(12, 12), sharex=True, sharey=True)
    ax = axes.ravel()
    row = 0
    for labels_by_size in labels_by_size_sorted[:img_count]:
        label = labels_by_size[1]

        filtered_image = create_filtered_image(labeled, label, im_gray.shape)
        filtered_image = ensure_white_bg_binary(filtered_image)
        subplot(ax[count], filtered_image, 'img' + str(count))
        ff8 = filtered_image.astype(np.uint8)
#        Image.fromarray(ff8).show()
        count += 1
        row += 1

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb

def create_filtered_image(labeled, label, shape):
    import numpy as np

    #this reduces the size of the image - strips all zeros; can't yet make it work
    # filtered_image = labeled[labeled != label]
    # take the simple route - much slower but works
    filtered_image = np.full(shape, 255)

    # maybe use np.where?
    for r in range(shape[0]):
        for c in range(shape[1]):
            val = labeled[r,c]
            if val == label:
                filtered_image[r,c] = 0

    return filtered_image

def ensure_white_bg_binary(image):
    import numpy as np
    white = np.sum(image > 0)
    black = np.sum(image == 0)
    return image if white > black else np.where(image > 0, 0, 1)

def thin_binary(image_file, thresh=180):
    from skimage.morphology import skeletonize, thin
    import os
    import numpy as np
    from PIL import Image
    from scipy.ndimage import label


    skeleton = thin_skeleton_file(image_file, thresh=180, mode="skeleton")
    thinned = thin_skeleton_file(image_file, max_iter=25, thresh=180, mode="thin")
    fig, axes = plt.subplots(1, 3, figsize=(12, 12), sharex=True, sharey=True)
    ax = axes.ravel()

    image = Image.open(image_file)
    subplot(ax[0], image, 'original')
    subplot(ax[1], ensure_white_bg_binary(skeleton), 'skeleton')
    subplot(ax[2], ensure_white_bg_binary(thinned), 'thinned')
#    subplot(ax[3], thinned_partial, 'thinned_partial')

    fig.tight_layout()
    plt.show()

def thin_skeleton_file(image_file, max_iter=25, thresh=180, mode="skeleton"):
    # mode = skeleton or thin
    import numpy as np
    from PIL import Image

    im_gray =np.array(Image.open(image_file).convert("L"))
    return thin_skeleton_gray(im_gray, max_iter, thresh, mode=mode)

def thin_skeleton_gray(im_gray, max_iter=25, thresh=180, mode="skeleton"):
    import numpy as np
    from skimage.morphology import skeletonize, thin
    maxval = 255
    im_bin = (im_gray > thresh) * maxval
    im_invert = (255 - im_bin)
    image = im_invert
    # binarize; this is white on black which skeletonize wants
    image = np.where(image > 0, 1, 0)

    thinned_image = skeletonize(image) if mode=="skeleton" else thin(image, max_iter)
    return thinned_image


def subplot(axi, image, title):
        axi.imshow(image, cmap=plt.cm.gray)
        axi.set_title(title)
        axi.axis('off')


def segments():
    """ NOT YET USED """

    # apply threshold
    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(3))

    # remove artifacts connected to image border
    cleared = clear_border(bw)

    # label image regions
    label_image = label(cleared)
    # to make the background transparent, pass the value of `bg_label`,
    # and leave `bg_color` as `None` and `kind` as `overlay`
    image_label_overlay = label2rgb(label_image, image=image, bg_label=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)

    for region in regionprops(label_image):
        # take regions with large enough areas
        if region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
