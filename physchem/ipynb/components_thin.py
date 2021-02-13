#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')

import os
HOME = os.path.expanduser("~")
JUPYTER = os.path.join(HOME, "workspace", "jupyter")
IMAGES = os.path.join(JUPYTER, "physchem", "images")
PHYSCHEM_LIION = os.path.join(JUPYTER, "physchem", "liion")


# In[ ]:


def find_components_and_thin(image_file):
    print("f", image_file, os.path.exists(image_file))
    label_binary(image_file, img_count=4, thresh=180)

    thin_binary(image_file)


# In[2]:


from labels import label_binary, thin_binary
PHYSCHEM_IMAGES = os.path.join(JUPYTER, "physchem", "images")
imgdict = {"RED_BLACK" : os.path.join(PHYSCHEM_IMAGES, "red_black_cv.png"),
        "CAPACITY" : os.path.join(PHYSCHEM_IMAGES, "capacitycycle.png"),
        "GREEN" : os.path.join(PHYSCHEM_LIION, 'PMC7077619/pdfimages/image.8.3.81_523.164_342/raw.png'),
        "PANEL2" : os.path.join(PHYSCHEM_LIION, 'PMC7075112/pdfimages/image.5.2.98_499.292_449/raw.png'),
        "PLOT2" : os.path.join(PHYSCHEM_LIION, 'PMC7075112/pdfimages/image.4.3.117_479.722_864/raw.png'),
        "PLOT3" : os.path.join(PHYSCHEM_LIION, 'PMC7074852/pdfimages/image.7.3.86_507.385_495/raw.png'),
        "PLOT32" : os.path.join(PHYSCHEM_LIION, 'PMC7067258/pdfimages/image.5.1.52_283.71_339/raw.png'),
          }

# https://note.nkmk.me/en/python-numpy-opencv-image-binarization/
import scipy.ndimage
from PIL import Image
import numpy as np
from collections import Counter

name = "PLOT2"
name = "GREEN"        
name = "RED_BLACK"

for name in imgdict.keys():
    print(name)
    image_file = imgdict[name]
    find_components_and_thin(image_file)


# 
# # Label image regions
# 
# 
# This example shows how to segment an image with image labelling. The following
# steps are applied:
# 
# 1. Thresholding with automatic Otsu method
# 2. Close small holes with binary closing
# 3. Remove artifacts touching image border
# 4. Measure image regions to filter small objects
# 

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb


# image = data.coins()[50:-50, 50:-50]
# requires grayscale
def labels(image):
    print("OTSU not yet implemented")
    return

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
    
JUPYTER = "/Users/pm286/workspace/jupyter"
import os
import numpy as np
from PIL import Image
imagefile = os.path.join(JUPYTER, "physchem", "images", "red_black_cv.png")
image = Image.open(imagefile).convert('LA')
print("image", type(image))
labels = labels(image)
print("labels ", labels)


# In[ ]:



if __name__ == "__main__":
    import sys
    
#    main(sys.argv[1:])        
print("FINISHED")

