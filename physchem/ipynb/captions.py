#!/usr/bin/env python
# coding: utf-8

# In[1]:


# figures and captions
get_ipython().run_line_magic('matplotlib', 'inline')

from pathlib import Path
import os

HOME = str(Path.home())
PROJECTS = os.path.join(HOME, "projects")
WORKSPACE = os.path.join(HOME, "workspace")
JUPYTER = os.path.join(WORKSPACE, "jupyter")


get_ipython().system('date')
print("projects")


# In[2]:


PHYSCHEM = os.path.join(JUPYTER, "physchem") 
PHYSCHEM_IMAGES = os.path.join(PHYSCHEM, "images") 
PHYSCHEM_HTML = os.path.join(PHYSCHEM, "html") 


# In[3]:


# BATTERY = os.path.join(PROJECTS, "open-battery")
PROJECT_DIR = os.path.join(PHYSCHEM, "liion")
# os.chdir(PROJECT_DIR)
# os.listdir()


# In[4]:


debug = True
ml = False


# In[5]:


import Tesseract as tt
# print(tt.pytesseract.version)
import pytesseract36 as pytesseract


# In[6]:


tesseract = tt.Tesseract()
osd =tesseract.get_osd()
dict = pytesseract.osd_to_dict(osd)
print("dict ", dict)
#xx = tesseract.test()


# In[7]:


import glob
os.chdir(PROJECT_DIR)
figures = glob.glob("PMC*/sections/fig*/*.xml")
# print(len(figures))


# In[8]:


# https://pypi.org/project/pytesseract/
try:
    from PIL import Image
except ImportError:
    import Image


print("begin tesseract")

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'/#usr/local/bin/tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
print("end tesseract")


# In[9]:


if __name__ == '__main__':
    pass

os.chdir(PHYSCHEM)
from PIL import Image

print(os.getcwd())
test_png = os.path.join('images', 'capacitycycle.png')
test_image = Image.open(test_png, 'r')

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

from skimage import data, img_as_float
from skimage import exposure
from skimage.viewer import ImageViewer

"""
if debug:
    image = Image.open(test_png, 'r')

    # viewer = ImageViewer(image)
    # viewer.show()
    tesseract_strings = pytesseract.image_to_string(Image.open(test_png))
    print(tesseract_strings)
"""


# In[10]:


# In order to bypass the image conversions of pytesseract, just use relative or absolute image path
# NOTE: In this case you should provide tesseract supported images or tesseract will return error
# print(pytesseract.image_to_string('test.png'))

# Batch processing with a single file containing the list of multiple image file paths
# print(pytesseract.image_to_string('images.txt'))

# Timeout/terminate the tesseract job after a period of time
"""
try:
    print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
    print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
except RuntimeError as timeout_error:
    # Tesseract processing is terminated
    pass
"""
# Get bounding box estimates
if debug:
    bboxes = pytesseract.image_to_boxes(Image.open(test_png))
    print(bboxes[:100], "\n...\n", bboxes[-100:])


# In[11]:


if debug:
# Get verbose data including boxes, confidences, line and page numbers
    data = pytesseract.image_to_data(test_image)
    print(type(data),"\n", data[:200], "\n...\n", data[-200:])
    
    


# In[12]:


def get_test_image():
    test_image = Image.open(test_png)


# In[13]:


if debug:
# Get information about orientation and script detection
    osd = pytesseract.image_to_osd(Image.open(test_png))
    print(osd)


# In[14]:


if debug:
    # Get a searchable PDF
    pdf = pytesseract.image_to_pdf_or_hocr(test_png, extension='pdf')
    hocr = pytesseract.image_to_pdf_or_hocr(test_png, extension='hocr')
    os.chdir(PHYSCHEM)
    with open('test.pdf', 'w+b') as f:
        f.write(pdf) # pdf type is bytes by default
    with open('test.hocr.html', 'w+b') as f:
        f.write(hocr) # hocr
    os.getcwd()
    os.listdir()


# In[15]:


if debug:
    import xml.etree.ElementTree as ET
# Get HOCR output
    hocr = pytesseract.image_to_pdf_or_hocr(test_png, extension='hocr')
#    print("hocr ", type(hocr), len(hocr), hocr[:2000])
    hocr_html = hocr.decode('utf-8')
    root = ET.fromstring(hocr_html)
    print("root", type(root))
    hocrlines = hocr_html.split("\n")
    for hocrline in hocrlines[:25]:
        print(">>", hocrline)
    HTMLNS = "{http://www.w3.org/1999/xhtml}"
    xpath = ".//" + HTMLNS + "span"
    words = root.findall(xpath)
    print("spans", len(words))
    # namespaces...
    words = root.findall(".//*[@class='ocrx_word']")
    print("ocrx_words", len(words))
    textboxes = []
    for word in words:
        bbox = [int(xy) for xy in word.attrib["title"].split(";")[0].split("bbox")[1].split()]
        print(str(bbox) + " {" + word.text +"}")
        textboxes.append((word.text, bbox))
    print(">>", textboxes[:2])


# In[16]:


im = np.array(Image.open(test_png))

print("Before trimming:",im.shape)
ymax = im.shape[1]
print("ymax", ymax)
xlo = 0
xhi = im.shape[0]
ylo = 0 
yhi = im.shape[1]

# xlo = 100
# xhi -= 100

print(xlo, xhi, ylo, yhi)
# runs in other direction?
# im_trim = im[ylo:yhi, xlo:xhi]
# im_trim = im[xlo:xhi, ylo:yhi]
im_trim = im[ylo:yhi, xlo:xhi]
print("After trimming:",im_trim.shape)

Image.fromarray(im_trim).show()              
Image.fromarray(im_trim).save('trim_image.png')


# In[17]:


# to/from image
from PIL import Image
from numpy import asarray
# load the image
image = Image.open('kolala.jpeg')
# convert image to numpy array
data = asarray(image)
print(type(data))
# summarize shape
print(data.shape)

# create Pillow image
image2 = Image.fromarray(data)
print(type(image2))

# summarize image details
print(image2.mode)
print(image2.size)


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

# Number of data points
n = 5

# Dummy data
np.random.seed(19680801)
x = np.arange(0, n, 1)
y = np.random.rand(n) * 5.

# Dummy errors (above and below)
xerr = np.random.rand(2, n) + 0.1
yerr = np.random.rand(2, n) + 0.2


def make_boxes(textboxes, facecolor='r',
                     edgecolor='None', alpha=0.5):

    # Create list for all the error patches
    boxes = []

    # Loop over data points; create box from errors at each point
    x = []
    y = []
    ymax = 1000
    texts = []
    for textbox in textboxes:
        text = textbox[0]
        box = textbox[1]
        x0 = box[0]
        y0 = ymax - box[1]
        x1 = box[2]
        y1 = ymax - box[3]
        x.append(x0)
        y.append(y0)
        rect = Rectangle((x0, y0), x1 - x0 , y1 - y0)
        texts.append((x0, y0, text))
        print(rect)
        boxes.append(rect)

    return x,y,boxes, texts


# Create figure and axes


# Call function to create error boxes
x, y, boxes, texts = make_boxes(textboxes)

plt.plot(x, y, '.')
plt.xlabel("x label")
plt.ylabel("y label")
for text in texts:
    plt.text(text[0], text[1], text[2])

plt.show()


# In[ ]:


liion = os.path.join(PHYSCHEM, 'liion')
os.chdir(liion)
liions = glob.glob("**/sections/*/fig*.xml")
print("liions ", len(liions))

liionpngs = glob.glob("**/pdfimages/**/raw.png")
print("liions pngs", len(liionpngs)) 

import matplotlib.pyplot as plt
# %matplotlib inline

import time
import html2text
import numpy as np
import nltk
get_ipython().run_line_magic('matplotlib', 'inline')


# print(liionpngs)
maxcount = 20
minlen = 2
corpus =[]
wordzz = []
stopwords = set(['oo'])
for count, liionpng in enumerate(liionpngs[:maxcount]):
    if count % 10 == 0:
        print ("img ", count, liionpng)
#    img = Image.open(liionpng)
#    plt.figure()
#    plt.imshow(np.asarray(img))
#    plt.imshow(img)

    hocr_file = os.path.join(os.path.split(liionpng)[0], 'hocr.html')
    hocr = pytesseract.image_to_pdf_or_hocr(liionpng, extension='hocr')
    with open(hocr_file, 'w+b') as f:
        f.write(hocr) # hocr
    html = open(hocr_file).read()
    htmltext = html2text.html2text(html)
    words = nltk.word_tokenize(htmltext)
    words = [word for word in words if len(word) >= minlen and not word.isnumeric()            and not word.lower() in stopwords]
    if len(words) > 0:
        text = " ".join(words)
    #    print("words", np.array(words))
        corpus.append(text)
        for word in words:
            wordzz.append(word)
            
from collections import Counter
c = Counter(wordzz) 
print(len(c))
print(c.most_common(20))
print("text list", len(corpus))
normalize_corpus = np.vectorize(corpus)
# print(corpus)
        


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

vectorizer = TfidfVectorizer(smooth_idf=True,use_idf=True)
X = vectorizer.fit_transform(corpus)
vocab = vectorizer.get_feature_names()
print(X.shape)
foo_list = vectorizer.inverse_transform(X)
print("\n=====", len(foo_list), foo_list)
for foo in foo_list:
    print(">>>", foo)

# pd.DataFrame(np.round(X, 2), columns=vocab)

"""
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True) 
tfidf_transformer.fit(word_count_vector)
# print idf values 
df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"]) 
 
# sort ascending 
df_idf.sort_values(by=['idf_weights'])

tv_matrix = tv.fit_transform(textlist)
tv_matrix = tv_matrix.toarray()
vocab = tv.get_feature_names()
pd.DataFrame(np.round(tv_matrix, 2), columns=vocab)
"""


# In[ ]:


print("FINISHED")

