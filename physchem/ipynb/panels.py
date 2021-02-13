#!/usr/bin/env python
# coding: utf-8

# In[1]:


# figures and captions
# get_ipython().run_line_magic('matplotlib', 'inline')
# http://kba.cloud/hocr-spec/1.2/
from pathlib import Path
import os
# https://pypi.org/project/pytesseract/
# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'/#usr/local/bin/tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
try:
    from PIL import Image
except ImportError:
    import Image
import Tesseract as tt
import pytesseract36 as pytesseract
# https://nanonets.com/blog/ocr-with-tesseract/
import matplotlib
import xml.etree.ElementTree as ET
from skimage import data, img_as_float
from skimage import exposure
from skimage.viewer import ImageViewer


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

import time
import html2text
import nltk
# get_ipython().run_line_magic('matplotlib', 'inline')



HOME = str(Path.home())
PROJECTS = os.path.join(HOME, "projects")
WORKSPACE = os.path.join(HOME, "workspace")
JUPYTER = os.path.join(WORKSPACE, "jupyter")

get_ipython().system('date')


# In[2]:


PHYSCHEM = os.path.join(JUPYTER, "physchem") 
PHYSCHEM_IMAGES = os.path.join(PHYSCHEM, "images") 
PHYSCHEM_LIION = os.path.join(PHYSCHEM, "liion") 
PHYSCHEM_HTML = os.path.join(PHYSCHEM, "html") 


# In[3]:


PROJECT_DIR = os.path.join(PHYSCHEM, "liion")


# In[4]:


debug = True
ml = False


# In[5]:


image = None
IMAGE = "image"
IMAGE_ARRAY = "image_array"

XMIN = "xmin"
XMAX = "xmax"
YMIN = "ymin"
YMAX = "ymax"

plot_dict = {}

BOT_AXIS_TITLE = "bot_axis_title"
BOT_AXIS_SCALE = "bot_axis_scale"
BOT_AXIS_TICKS = "bot_axis_ticks"
BOT_AXIS_LINE =  "bot_axis_line"

LEFT_AXIS_TITLE = "left_axis_title"
LEFT_AXIS_SCALE = "left_axis_scale"
LEFT_AXIS_TICKS = "left_axis_ticks"
LEFT_AXIS_LINE =  "left_axis_line"

TOP_AXIS_TITLE = "top_axis_title"
TOP_AXIS_SCALE = "top_axis_scale"
TOP_AXIS_TICKS = "top_axis_ticks"
TOP_AXIS_LINE =  "top_axis_line"

RIGHT_AXIS_TITLE = "right_axis_title"
RIGHT_AXIS_SCALE = "right_axis_scale"
RIGHT_AXIS_TICKS = "right_axis_ticks"
RIGHT_AXIS_LINE  = "right_axis_line"

WHOLE_AREA     = "whole_area"
BOTTOM_TRIMMED = "bottom_trimmed"

PLOT_AREA = "plot_area"
OSD = "osd"
DATA = "data"


# In[6]:


import os
CAPACITY_CYCLE = "capacity_cycle"
RED_BLACK = "red_black"
GREEN = "green"
PANEL2 = "panel2"
PLOT2 = "panel2b"
PLOT3 = "panel3"
PLOT32 = "panel3*2"

def get_test_image(name=CAPACITY_CYCLE):
    images = {
        CAPACITY_CYCLE : os.path.join(PHYSCHEM_IMAGES, 'capacitycycle.png'),
        RED_BLACK : os.path.join(PHYSCHEM_IMAGES, 'red_black_cv.png'),
        GREEN : os.path.join(PHYSCHEM_LIION, 'PMC7077619/pdfimages/image.8.3.81_523.164_342/raw.png'),
        PANEL2 : os.path.join(PHYSCHEM_LIION, 'PMC7075112/pdfimages/image.5.2.98_499.292_449/raw.png'),
        PLOT2 : os.path.join(PHYSCHEM_LIION, 'PMC7075112/pdfimages/image.4.3.117_479.722_864/raw.png'),
        PLOT3 : os.path.join(PHYSCHEM_LIION, 'PMC7074852/pdfimages/image.7.3.86_507.385_495/raw.png'),
        PLOT32 : os.path.join(PHYSCHEM_LIION, 'PMC7067258/pdfimages/image.5.1.52_283.71_339/raw.png'),
    }
    image_file = images.get(name)
    if image_file == None:
        print("no test image", name)
        return
    image = Image.open(image_file, 'r')
    if debug:
        image.show()
    print("image file", type(image), type(image_file))
    return (image, image_file)


# In[7]:


if __name__ == '__main__':
    pass


# In[8]:


import sys
sys.path.append('/Users/pm286/workspace/jupyter/classes')
import labels
from Tesseract import *
from plot import create_baselines, create_sections,     draw_boxes_round_tesseract_chars, plot_sections, plot_box

plot = False
image_array = []
image, image_file = get_test_image(
#   CAPACITY_CYCLE
#    RED_BLACK
#   GREEN
#    PANEL2
    PLOT2
#    PLOT3
#    PLOT32
)

# findlines(image)
print(type(image), image, type(image_file), image_file)
draw_boxes_round_tesseract_chars(image, image_file)
if debug:
    print("image", image, "image_file", image_file)
print("\n===========A==========\n")
debug = False    
textboxes = Tesseract.get_tesseract_textboxes(image_file)
print("\n===========B==========\n")
create_baselines(textboxes)
print("\n===========C==========\n")
create_sections(image)
print("\n===========D==========\n")
if plot:
    plot_sections()

#plot_box(WHOLE_AREA)
#plot_box(BOTTOM_TRIMMED)


# In[9]:


print("FINISHED")


# In[ ]:




