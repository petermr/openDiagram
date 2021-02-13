#!/usr/bin/env python
# coding: utf-8

# # read PDFs, makeproject, extract images and create octrees
# 
# 

# ### variables
# 
# 

# In[23]:


# where is ami3? (assume you have checked out or copied `ami3` distrib).
# set AMI3 to location of LOCAL AMI repository
# EDIT THIS >>>>>>>
HOME = "/Users/pm286/"
WORKSPACE = HOME + "workspace/"
AMI3 = WORKSPACE + "cmdev/ami3/"
# <<<<<<<<<<

# local workspace
# EDIT this >>>>>>>>
WORK = WORKSPACE + "work/"
# <<<<<<<<<<

# specific problem
# EDIT THIS to your project (battery10, thermo at present)
# >>>>>>>
PROJECT = "steffen/llzo"
# <<<<<<<

PROJECT_WORK = WORK + PROJECT + "/"


# specific for projects under ami3/src/test/resources
# PROJECT_DATA = AMI_DATA + PROJECT + ".raw" + "/"
PROJECT_DATA = "/Users/pm286/projects/steffen"


# In[24]:



print ("working in " + PROJECT_WORK)
get_ipython().system(' cd $PROJECT_WORK')
get_ipython().system(' ls')
print ("copying raw project " + PROJECT_DATA + " => " + PROJECT_WORK)
get_ipython().system(' cp -R $PROJECT_DATA $PROJECT_WORK')


# In[32]:


import os 
os.getcwd()
os.listdir()


# In[33]:


## make project
# ! ami -p . makeproject --rawfiletypes pdf
get_ipython().system(' ls */*.pdf')
get_ipython().system(' ls */*.xml')


# In[34]:



get_ipython().system(' ami -vv -p . pdfbox')


# In[35]:


get_ipython().system(' ami -vv -p .  --inputname raw --output octree image --octree 8 --outputfiles binary channels histogram neighbours octree')


# In[36]:


get_ipython().system(' tree .')


# In[ ]:



from IPython.display import display
from PIL import Image
path="PMC3211491/pdfimages/image.3.1.64_532.102_571/raw.png"
display(Image.open(path))

import ipyplot
images_array = [            "PMC3211491/pdfimages/image.3.1.64_532.102_571/raw.png",            "PMC3211491/pdfimages/image.4.1.64_532.102_336/raw.png",            "PMC3211491/pdfimages/image.4.2.313_531.492_708/raw.png",            "PMC3211491/pdfimages/image.5.1.63_533.240_708/raw.png",            "PMC3211491/pdfimages/image.6.1.63_286.483_698/raw.png",            "PMC3211491/pdfimages/image.6.2.311_534.102_322/raw.png"]

ipyplot.plot_images(images_array, max_images=20, img_width=300)


# In[ ]:


get_ipython().system(' pwd')


# In[ ]:


get_ipython().system('ls ')


# In[ ]:


get_ipython().system('ls PMC3211491/pdfimages/image.3.1.64_532.102_571/raw.png')


# In[ ]:


get_ipython().system('tree PMC3211491')


# In[ ]:


images_array = ["PMC3211491/pdfimages/image.4.2.313_531.492_708/raw.png","PMC3463005/pdfimages/image.6.2.86_509.389_714/raw.png","PMC3518813/pdfimages/image.2.2.129_466.69_338/raw.png","PMC3776197/pdfimages/image.4.2.58_538.371_714/raw.png","PMC3776197/pdfimages/image.5.2.107_488.253_704/raw.png","PMC3776197/pdfimages/image.7.2.113_483.69_352/raw.png","PMC3893646/pdfimages/image.5.2.48_547.69_472/raw.png","PMC4062906/pdfimages/image.5.1.66_281.517_691/raw.png","PMC4148673/pdfimages/image.3.2.63_272.69_527/raw.png"]
ipyplot.plot_images(images_array, max_images=20, img_width=300)


# In[ ]:


cd PMC3211491/pdfimages/image.4.2.313_531.492_708/octree


# In[ ]:


ls channel*.png


# In[ ]:


import glob
image_array = glob.glob("channel*.png")
# print (image_array)
image_array2 = ["PMC3211491/pdfimages/image.4.2.313_531.492_708/octree/" + s for s in image_array]
print(image_array2)
# ! cd /Users/pm286/workspace/work/battery10/PMC3211491/pdfimages/image.4.2.313_531.492_708/octree
ipyplot.plot_images(image_array2, max_images=20, img_width=300)


# In[ ]:


import os
get_ipython().system(' cd $PROJECT_WORK')
get_ipython().system(' ls')
get_ipython().system(' pwd')
os.listdir(".")


# In[ ]:




