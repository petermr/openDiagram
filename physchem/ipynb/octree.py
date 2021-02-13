#!/usr/bin/env python
# coding: utf-8

# In[1]:


HOME = None
PROJECTS = None
WORKSPACE = None
JUPYTER = None
def global_vars():
    import os
    HOME = os.path.expanduser("~")
    PROJECTS = os.path.join(HOME, "projts")
    WORKSPACE = os.path.join(HOME, "workspace")
    JUPYTER = os.path.join(WORKSPACE, "jupyter")


# In[2]:


PHYSCHEM = None 
PHYSCHEM_IMAGES = None
PHYSCHEM_LIION = None
PHYSCHEM_HTML = None 
def physchem_vars():
    import os

    PHYSCHEM = os.path.join(JUPYTER, "physchem") 
    PHYSCHEM_IMAGES = os.path.join(PHYSCHEM, "images") 
    PHYSCHEM_LIION = os.path.join(PHYSCHEM, "liion") 
    PHYSCHEM_HTML = os.path.join(PHYSCHEM, "html") 


# In[3]:


CAPACITY_CYCLE = "capacity_cycle"
RED_BLACK = "red_black"
GREEN = "green"
PANEL2 = "panel2"
PLOT2 = "panel2b"
PLOT3 = "panel3"
PLOT32 = "panel3*2"

def select_image_file(name):
    import os
    
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
    else:
        print("image file", image_file)
    return image_file


# In[4]:



from PIL import Image
import Octree as oct

def main_sub(name, minpixel=1000):
    from labels import thin_skeleton_gray
    
    print("name ", name)
    image_file = select_image_file(name)
    image = Image.open(image_file)
    image.show()
    pixels = image.load()
    out_image, palette, palette_image = oct.quantize(image, size=4)
    out_pixels = out_image.load()
    print("palette", len(palette))
    width, height = out_image.size
    image_by_color = {}
    for color in palette:
        color_image = Image.new('RGB', image.size, color = 'white')
        color_pixels = color_image.load()
        pixel_count = 0
        image_by_color[color] = color_image
        for i in range(width):
            for j in range(height):
                colorij = out_pixels[i,j]
                if (color.is_equal(colorij)):
                    color_pixels[i,j] = color.as_tuple()
                    pixel_count += 1
        if pixel_count > minpixel:
            color_image.show()
#            thin_image(color_image)

        print("#" + color.to_hex(), "pixels", pixel_count)
    
    palette_image.show()
    out_image.show()
    out_image.save(name + '.png')

def thin_image(image):
    from labels import thin_skeleton_gray
    im_thin = thin_skeleton_gray(image)
    fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, sharey=True)
#    ax = axes.ravel()

    subplot(ax[0], image, 'original')
    subplot(ax[1], im_thin, 'skeleton')


if __name__ == '__main__':
    pass



# In[5]:


import os
HOME = os.path.expanduser("~")
PROJECTS = os.path.join(HOME, "projts")
WORKSPACE = os.path.join(HOME, "workspace")
JUPYTER = os.path.join(WORKSPACE, "jupyter")
PHYSCHEM = os.path.join(JUPYTER, "physchem") 
PHYSCHEM_IMAGES = os.path.join(PHYSCHEM, "images") 
PHYSCHEM_LIION = os.path.join(PHYSCHEM, "liion") 
PHYSCHEM_HTML = os.path.join(PHYSCHEM, "html")
    
name = CAPACITY_CYCLE
name = RED_BLACK
name = GREEN
name = PLOT2
name = PANEL2
name = PLOT32
name = PLOT3


main_sub(name)


# In[ ]:




