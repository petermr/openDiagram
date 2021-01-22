#!/usr/bin/env python
# coding: utf-8

# In[1]:


# unit tests


# In[2]:


def make_rgb_vector():
    R = .692
    G = .582
    B = .140

    # why fourth power?
    vector = [R, G, B]
    vector = vector / vector.sum()
    vector = np.pow(vector, 4)
    return vector
        
def save_rgb_as_uint8_file(imgIn, fileout):

    vector = make_rgb_vector()
    imgOut = imgIn * vector
    io.imsave(
      fileout, 
      imgOut.astype(np.uint8))
                       
def more_uint8_stuff(img):
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # make color channels
    red = gray.copy()
    green = gray.copy()
    blue = gray.copy()

    # set weights
    R = .642
    G = .532
    B = .44

    # get sum of weights and normalize them by the sum
                       
    sum = R**4 + G**4 + B**4
    R = R/sum
    G = G/sum
    B = B/sum
    print(R,G,B)

    # combine channels with weights
    red = (R*red)
    green = (G*green)
    blue = (B*blue)
    result = cv2.merge([red,green,blue])

    # scale by ratio of 255/max to increase to fully dynamic range
    max=np.amax(result)
    result = ((255/max)*result).clip(0,255).astype(np.uint8)

    # write result to disk
    cv2.imwrite("car_colored.png", result)

    # display it
    cv2.imshow("RESULT", result)
    cv2.waitKey(0)                       


# In[3]:


def create_grid(rows, cols, drow, dcol, intensity=255):    
    a = np.zeros((rows, cols), dtype=np.int)
    for i in range(rows):
        if i%drow == 0:
            a[::, i:i+1] = intensity
    for j in range(cols):
        if j%dcol == 0:
            a[j:j + 1, ::] = intensity
 
    return a

def box(a, x, y, w, h, intensity):
    a[x : x+w, y : y + 1] = intensity
    a[x : x+w, y + h - 1 : y + h] = intensity
    a[x : x + 1, y : y + h] = intensity
    a[x + w -1: x + w, y : y + h] = intensity
    
def create_boxes(rows, cols, boxdx, boxdy, boxw, boxh, intensity=255):
    a = np.zeros((rows, cols), dtype=np.int)
    for i in range(rows):
        x0 = boxdx * i
        for j in range(cols):
            y0 = boxdy * j
            box(a, boxdx, boxdy, boxw, boxh, intensity)
    return a
        
def create_skeleton(image_file):
    import labels
    binary = labels.thin_skeleton_file(image_file)
    return binary


# In[4]:


def convolve2d(a, kernel):
    """Maybe not used"""
    import scipy.signal.convolve2d as convolve2d
#    convolved = np.asmatrix(convolve2d(a,kernel,'same'))
    convolved = convolve2d(a,kernel,'same')
    
    return convolved


# In[5]:


def convolve_normalize_transpose(grid, kernel, title="title"):
    from scipy import ndimage
    from PIL import Image

#    scipy.ndimage.convolve(input, weights, output=None, mode='reflect', cval=0.0, origin=0)
    convolve_cut = 0.9

    if np.any(grid)==None:
        print("grid missing")
        return
    if np.any(kernel)==None:
        print("kernel missing")
        return
    convolved = ndimage.convolve(grid, kernel)
    max = np.max(convolved)
    # normalize to grayscale
    convolved = np.where(convolved < max * convolve_cut , 0, convolved)
    convolved = convolved.astype(np.uint8)
    img = Image.fromarray(convolved)
    img.save(title+".png")
    convolved_t = np.transpose(convolved)
    return convolved, convolved_t

def convolve_and_plot(grid, kernel, title="title"):
    from PIL import Image
    convolved, convolved_t = convolve_normalize_transpose(grid, kernel, title)
    plot(convolved)
#    img = Image.fromarray(convolved)
#    img.save(title+".png")

#    plot(convolved_t)


# In[6]:


def plot(myarray):
    import matplotlib.pyplot as plt
    plt.imshow(myarray)
    plt.show()
    
def plot_file(file):
    array = Image.open(file, "r")
    plot(array)


# In[7]:


import numpy as np

def normalize_box(box):
    """ adds offset to normalize sum = zero """
    area = box.shape[0] * box.shape[1]
    newbox = box - np.sum(box) / area
    return newbox
        
def create_array_kernel(name, data_array):
    array = normalize_box(data_array)
    return array

def create_kernel(name, width=None, height=None, linewidth=1, intens=1):
    if width==None or height==None:
        raise Exception("must give width and height") 

    def half_points(w, h, lw):
        hw = (w + 1) // 2
        hh = (h + 1) // 2
        hlw = (lw + 1) // 2 
        return hw, hh, hlw

    def rect(w, h, lw, intens):
        box = np.zeros((width, height))
        box[0:lw, ::] = intens
        box[w - lw, ::] = intens
        box[::, 0:lw] = intens
        box[::, h-lw:h] = intens
        return box
        
    def vert(w, h, lw, intens):
        hw, hh, hlw = half_points(w, h, lw)
        box = np.zeros((w, h))
        box[hw - hlw : hw + hlw - 1, ::] = intens
        return box
        
    def horiz(w, h, lw, intens):
        box = np.zeros((w, h))
        hw, hh, hlw = half_points(w, h, lw)
        box[::, hw - hlw : hw + hlw - 1] = intens
        return box
        
    def cross(w, h, lw, intens):
        box = np.zeros((w, h))
        hw, hh, hlw = half_points(w, h, lw)
        box[hw - hlw : hw + hlw - 1, ::] = intens
        box[::, hh - hlw : hh + hlw - 1] = intens
        
        return box
    
    # top left angle
    def nw(w, h, lw, intens):
        box = np.zeros((w, h))
        hw, hh, hlw = half_points(w, h, lw)
        box[hw - 1 : hw,       hh:] = intens
        box[0:hw,       hh - 1: hh] = intens
#        print("nw", w, h, "\n", box)
        return box
    
    # top right angle
    def sw(w, h, lw, intens):
        box = np.zeros((w, h))
        hw, hh, hlw = half_points(w, h, lw)
        box[hw - 1 :,    hh - 1: hh] = intens
        box[hw - 1 : hw, 0: hh] = intens
#        print("sw", w, h, "\n", box)
        return box
    
    # bottom left
    def ne(w, h, lw, intens):
        box = np.zeros((w, h))
        hw, hh, hlw = half_points(w, h, lw)
        box[hw - 1 : hw , hh - 1:] = intens
        box[hw : ,  hh - 1 : hh] = intens
#        print("ne", h, w, "\n", box)
        return box
    
    # bottom right
    def se(w, h, lw, intens):
        box = np.zeros((w, h))
        hw, hh, hlw = half_points(w, h, lw)
        box[0 : hw - 1,   hh - 1: hh] = intens
        box[hw - 1 : hw,     0 : hh] = intens
#        print("se", w, h, "\n", box)
        return box
    
    kernels = {
        "rect" : rect (width, height, linewidth, intens),
        "horiz": horiz(width, height, linewidth, intens),
        "vert" : vert (width, height, linewidth, intens),
        "cross": cross(width, height, linewidth, intens),
        "se"   : se   (width, height, linewidth, intens),
        "ne"   : ne   (width, height, linewidth, intens),
        "sw"   : sw   (width, height, linewidth, intens),
        "nw"   : nw   (width, height, linewidth, intens),
    }
    
    func = kernels[name]
    box = func
    new_box = normalize_box(box)
    return new_box

def create_small_grid():
    grid = np.ones((10,15))*100
    grid[1:4,1:3] = 0
    grid[5:8,1:3] = 0
    grid[1:4,4:6] = 0
    grid[5:8,4:6] = 0
    grid[1:4,7:9] = 0
    grid[5:8,7:9] = 0
    grid[1:4,10:12] = 0
    grid[5:8,10:12] = 0
    grid[1:4,13:15] = 0
    grid[5:8,13:15] = 0
    return
    


# In[8]:


def smalltest():
    halfw = 2
    import os
    import numpy as np
    from scipy import ndimage
    from PIL import Image

    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter})

    gridw = 129
    gridh = 137
    grid = create_grid(gridw, gridh, 7, 3)

    print("rect73")
    rect_kernel = create_kernel("rect", 7,3)
    convolve_and_plot(grid, rect_kernel)
    print("rect37")
    rect_kernel = create_kernel("rect", 3,7)
    convolve_and_plot(grid, rect_kernel)
    print("cross")
    cross_kernel = create_kernel("cross", 5, 7, intens=3)
    convolve_and_plot(grid, cross_kernel)
    print("horiz")
    horiz_kernel = create_kernel("horiz", 5, 5)
    convolve_and_plot(grid, horiz_kernel)
    print("vert")
    vert_kernel = create_kernel("vert", 5, 5)
    convolve_and_plot(grid, vert_kernel)

    mydata = np.array([
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
    ])    

    print("[]")
    kernel = create_array_kernel("[]", mydata)

    convolve_and_plot(grid, kernel)

    print("===FINISHED smalltest===")

smalltest()


# In[9]:


def old_plot():
    """probably abandon"""
    from matplotlib import pyplot as plt
    grid = create_boxes(4, 5, 5, 6, 3, 4)
    print("grid", grid.shape, "\n", grid)
    plt.imshow(grid)
    plt.show()


    convolved = plot_convolve(grid, kernel)

    from matplotlib import pyplot as plt
    # plt.imshow(grid_points, interpolation='nearest')
    plt.imshow(grid)
    plt.show()
    plt.imshow(convolved,cmap='gray', vmin=0, vmax=255)
    plt.show()


# In[10]:


def plot_conv(title, w, h, file):
    import os
    print(title, "-", w, "-", h, "\n", "NOTE x and y may be interchanged")
    kernel = create_kernel(title, w, h)
    plot_pdfimages(kernel, title + str(w)+"-"+str(h)+".png", file)
    return

def plot_pdfimages(kernel, title, file):
    import os
    from PIL import Image
    from matplotlib import pyplot as plt
    
    bits = os.path.split(file)
    print("bits", bits)
    skeleton = create_skeleton(file)
    convolve_and_plot(skeleton, kernel, title);

def explore_hw(file):
    for i in range(3, 9, 2):
        for j in range(3, 9, 2):
            plot_conv("vert", i, j, file)

    for i in range(3, 9, 2):
        for j in range(3, 9, 2):
            plot_conv("horiz", i, j, file)

def plot_pdf_files():
    import os
    HOME = os.path.expanduser("~")
    files = [os.path.join(HOME,
        'workspace/jupyter/physchem/liion/PMC7077619/pdfimages/image.8.3.81_523.164_342/raw.png'),
            os.path.join(HOME, 'workspace/jupyter/physchem/images/capacitycycle.png'),
            os.path.join(HOME, 'workspace/jupyter/physchem/liion/PMC7077619/pdfimages/image.8.3.81_523.164_342/raw.png'),
            os.path.join(HOME, 'workspace/jupyter/physchem/liion/PMC7075112/pdfimages/image.5.2.98_499.292_449/raw.png'),
            os.path.join(HOME, 'workspace/jupyter/physchem/liion/PMC7075112/pdfimages/image.4.3.117_479.722_864/raw.png'),
            os.path.join(HOME, 'workspace/jupyter/physchem/liion/PMC7074852/pdfimages/image.7.3.86_507.385_495/raw.png'),
            os.path.join(HOME, 'workspace/jupyter/physchem/liion/PMC7067258/pdfimages/image.5.1.52_283.71_339/raw.png'),
        ]
    
    for file in files:
        print(file)
        if not os.path.isfile(file):
            print("nonexistent ", file)
            return

        test = False
        if test:    
            # explore best hw values
            explore_hw(file)
        else:
            plot_conv("vert",  3, 3, file)
            plot_conv("horiz", 3, 3, file)
            plot_conv("se",    5, 5, file)
            plot_conv("sw",    9, 9, file)
            plot_conv("nw",    9, 9, file)
            plot_conv("ne",    13, 13, file)
    return
                         
plot_pdf_files()


# In[ ]:




